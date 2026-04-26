#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple


DREAM_DIR = Path(__file__).resolve().parent.parent
STATE_DIR = DREAM_DIR / "state"
TEMPLATE_DIR = DREAM_DIR / "templates"

WORLD_JSON = STATE_DIR / "world_turbulence_profile.json"
OBSERVER_JSON = STATE_DIR / "observer_turbulence_profile.json"

PHASE_PREFIX_TO_KEY = {
    "01-enter": "01_enter",
    "02-dissolve": "02_dissolve",
    "03-dream": "03_dream",
    "04-distill": "04_distill",
    "05-finalize": "05_finalize",
}


def load_json(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"Missing JSON file: {path}")

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def constraints_block(items: List[str]) -> str:
    if not items:
        return "- none"
    return "\n".join(f"- {item}" for item in items)


def infer_phase_and_side(template_path: Path) -> Tuple[str, str]:
    resolved_template = template_path.resolve()
    resolved_templates_root = TEMPLATE_DIR.resolve()

    try:
        rel = resolved_template.relative_to(resolved_templates_root)
    except ValueError as exc:
        raise SystemExit(
            f"Template must be inside {TEMPLATE_DIR}. Got: {template_path}"
        ) from exc

    if len(rel.parts) < 2:
        raise SystemExit(
            f"Template must be inside a phase-side folder under {TEMPLATE_DIR}. Got: {template_path}"
        )

    folder = rel.parts[0]

    phase_prefix = None
    for prefix in PHASE_PREFIX_TO_KEY:
        if folder.startswith(prefix + "-"):
            phase_prefix = prefix
            break

    if phase_prefix is None:
        raise SystemExit(f"Cannot infer phase from template folder: {folder}")

    if folder.endswith("-world"):
        side = "world"
    elif folder.endswith("-observe"):
        side = "observe"
    else:
        raise SystemExit(f"Cannot infer side from template folder: {folder}")

    return PHASE_PREFIX_TO_KEY[phase_prefix], side


def get_phase_profile(phase_key: str, side: str) -> dict:
    json_path = WORLD_JSON if side == "world" else OBSERVER_JSON
    payload = load_json(json_path)

    profiles = payload.get("profiles")
    if not isinstance(profiles, dict):
        raise SystemExit(f"Missing 'profiles' object in {json_path}")

    profile = profiles.get(phase_key)
    if not isinstance(profile, dict):
        raise SystemExit(f"Missing profile for phase '{phase_key}' in {json_path}")

    labels = profile.get("labels")
    if not isinstance(labels, dict):
        raise SystemExit(f"Missing labels for phase '{phase_key}' in {json_path}")

    hard_constraints = profile.get("hard_constraints", [])
    if hard_constraints is None:
        hard_constraints = []

    if not isinstance(hard_constraints, list):
        raise SystemExit(
            f"hard_constraints must be a list for phase '{phase_key}' in {json_path}"
        )

    return profile


def build_mapping(template_path: Path) -> Dict[str, str]:
    phase_key, side = infer_phase_and_side(template_path)
    profile = get_phase_profile(phase_key, side)

    mapping: Dict[str, str] = {}

    for slot, label in profile["labels"].items():
        mapping[f"{slot}_label"] = str(label)

    mapping["hard_constraints_block"] = constraints_block(
        [str(item) for item in profile.get("hard_constraints", [])]
    )

    return mapping


def render_template_text(template_path: Path, mapping: Dict[str, str]) -> str:
    if not template_path.exists():
        raise SystemExit(f"Missing template file: {template_path}")

    text = template_path.read_text(encoding="utf-8")

    for key, value in mapping.items():
        text = text.replace("{{" + key + "}}", value)

    unresolved = sorted(set(re.findall(r"\{\{(.*?)\}\}", text)))
    if unresolved:
        raise SystemExit(
            f"Unresolved placeholders in {template_path}: {', '.join(unresolved)}"
        )

    return text


def default_output_path(template_path: Path) -> Path:
    output_name = template_path.name.replace(".tpl", "")

    if output_name == template_path.name:
        raise SystemExit(f"Template name must contain '.tpl': {template_path.name}")

    return DREAM_DIR / output_name


def compile_one_template(
    template_path: Path,
    output_path: Path | None,
    dry_run: bool,
) -> Path:
    template_path = template_path.resolve()
    mapping = build_mapping(template_path)
    rendered = render_template_text(template_path, mapping)

    target = output_path.resolve() if output_path else default_output_path(template_path)

    if dry_run:
        print(rendered)
        return target

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(rendered, encoding="utf-8")

    print(f"Compiled template:")
    print(f"  input : {template_path}")
    print(f"  output: {target}")

    return target


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compile one Dream Machine template using the existing generated JSON profiles."
    )

    parser.add_argument(
        "template",
        type=Path,
        help="Path to one .tpl.md template inside dream/templates/",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Optional output path. Defaults to dream/<template-name-without-.tpl>.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print rendered output instead of writing the file.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    compile_one_template(
        template_path=args.template,
        output_path=args.output,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()