#!/usr/bin/env python3
import hashlib
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

DREAM_DIR = Path(__file__).resolve().parent.parent
STATE_DIR = DREAM_DIR / "state"
TEMPLATE_DIR = DREAM_DIR / "templates"

SEED_JSON = STATE_DIR / "session_seed.json"

COMBINED_JSON = STATE_DIR / "turbulence_profile.json"
COMBINED_MD = STATE_DIR / "turbulence_profile.md"
WORLD_JSON = STATE_DIR / "world_turbulence_profile.json"
WORLD_MD = STATE_DIR / "world_turbulence_profile.md"
OBSERVER_JSON = STATE_DIR / "observer_turbulence_profile.json"
OBSERVER_MD = STATE_DIR / "observer_turbulence_profile.md"

BASE_SLOTS = [
    "world_shift_pressure",
    "memory_fuzz_pressure",
    "phrase_rebinding_pressure",
    "event_instability",
    "scene_morph_pressure",
    "banal_intrusion_allowance",
    "translation_density",
    "continuity_loosening",
    "contradiction_tolerance",
    "micro_texture_distortion",
    "observer_agency_damping",
    "observer_detachment",
    "interpretation_latency",
    "witness_intensity",
    "lucidity_softness",
    "self_boundary_softening",
]

PHASES = ["01_enter", "02_dissolve", "03_dream", "04_distill", "05_finalize"]
PHASE_PREFIX_TO_KEY = {
    "01-enter": "01_enter",
    "02-dissolve": "02_dissolve",
    "03-dream": "03_dream",
    "04-distill": "04_distill",
    "05-finalize": "05_finalize",
}

PHASE_TRANSFORMS = {
    "01_enter": {
        "world": {
            "world_shift_pressure": (2, 10, 0),
            "memory_fuzz_pressure": (3, 10, 0),
            "phrase_rebinding_pressure": (2, 10, 0),
            "event_instability": (1, 10, 0),
            "scene_morph_pressure": (2, 10, 0),
            "banal_intrusion_allowance": (2, 10, 0),
            "translation_density": (3, 10, 0),
            "continuity_loosening": (2, 10, 0),
            "contradiction_tolerance": (2, 10, 0),
            "micro_texture_distortion": (2, 10, 0),
        },
        "observer": {
            "observer_agency_damping": (8, 10, 1),
            "observer_detachment": (5, 10, 0),
            "interpretation_latency": (9, 10, 1),
            "witness_intensity": (6, 10, 0),
            "lucidity_softness": (3, 10, 0),
            "self_boundary_softening": (4, 10, 0),
        },
    },
    "02_dissolve": {
        "world": {
            "world_shift_pressure": (4, 10, 0),
            "memory_fuzz_pressure": (5, 10, 0),
            "phrase_rebinding_pressure": (6, 10, 0),
            "event_instability": (3, 10, 0),
            "scene_morph_pressure": (4, 10, 0),
            "banal_intrusion_allowance": (3, 10, 0),
            "translation_density": (8, 10, 1),
            "continuity_loosening": (4, 10, 0),
            "contradiction_tolerance": (5, 10, 0),
            "micro_texture_distortion": (3, 10, 0),
        },
        "observer": {
            "observer_agency_damping": (8, 10, 1),
            "observer_detachment": (7, 10, 0),
            "interpretation_latency": (9, 10, 1),
            "witness_intensity": (7, 10, 0),
            "lucidity_softness": (3, 10, 0),
            "self_boundary_softening": (6, 10, 0),
        },
    },
    "03_dream": {
        "world": {
            "world_shift_pressure": (10, 10, 0),
            "memory_fuzz_pressure": (10, 10, 0),
            "phrase_rebinding_pressure": (9, 10, 0),
            "event_instability": (9, 10, 0),
            "scene_morph_pressure": (10, 10, 0),
            "banal_intrusion_allowance": (7, 10, 1),
            "translation_density": (10, 10, 0),
            "continuity_loosening": (8, 10, 1),
            "contradiction_tolerance": (9, 10, 0),
            "micro_texture_distortion": (6, 10, 1),
        },
        "observer": {
            "observer_agency_damping": (9, 10, 1),
            "observer_detachment": (8, 10, 0),
            "interpretation_latency": (8, 10, 0),
            "witness_intensity": (8, 10, 0),
            "lucidity_softness": (2, 10, 0),
            "self_boundary_softening": (8, 10, 0),
        },
    },
    "04_distill": {
        "world": {
            "world_shift_pressure": (3, 10, 0),
            "memory_fuzz_pressure": (4, 10, 0),
            "phrase_rebinding_pressure": (3, 10, 0),
            "event_instability": (2, 10, 0),
            "scene_morph_pressure": (2, 10, 0),
            "banal_intrusion_allowance": (4, 10, 0),
            "translation_density": (6, 10, 0),
            "continuity_loosening": (3, 10, 0),
            "contradiction_tolerance": (5, 10, 0),
            "micro_texture_distortion": (2, 10, 0),
        },
        "observer": {
            "observer_agency_damping": (3, 10, 0),
            "observer_detachment": (4, 10, 0),
            "interpretation_latency": (5, 10, 0),
            "witness_intensity": (9, 10, 0),
            "lucidity_softness": (5, 10, 0),
            "self_boundary_softening": (4, 10, 0),
        },
    },
    "05_finalize": {
        "world": {
            "world_shift_pressure": (1, 10, 0),
            "memory_fuzz_pressure": (1, 10, 0),
            "phrase_rebinding_pressure": (1, 10, 0),
            "event_instability": (1, 10, 0),
            "scene_morph_pressure": (1, 10, 0),
            "banal_intrusion_allowance": (3, 10, 0),
            "translation_density": (2, 10, 0),
            "continuity_loosening": (1, 10, 0),
            "contradiction_tolerance": (3, 10, 0),
            "micro_texture_distortion": (2, 10, 0),
        },
        "observer": {
            "observer_agency_damping": (1, 10, 0),
            "observer_detachment": (2, 10, 0),
            "interpretation_latency": (2, 10, 0),
            "witness_intensity": (10, 10, 0),
            "lucidity_softness": (6, 10, 0),
            "self_boundary_softening": (2, 10, 0),
        },
    },
}


def clamp_digit(n: int) -> int:
    return max(0, min(9, int(n)))


def expand_bytes(seed_material: bytes, minimum_digits: int) -> List[int]:
    digits: List[int] = []
    counter = 0
    while len(digits) < minimum_digits:
        block = hashlib.sha256(seed_material + counter.to_bytes(4, "big")).digest()
        for b in block:
            if b < 250:
                digits.append(b % 10)
                if len(digits) >= minimum_digits:
                    break
        counter += 1
    return digits


def digit_label(slot: str, d: int) -> str:
    tables = {
        "world_shift_pressure": [
            "almost fixed world",
            "faint drift only",
            "slight instability",
            "low morph pressure",
            "occasional shift tendency",
            "moderate world drift",
            "active morph pressure",
            "strong shifting field",
            "high reality slippage",
            "dominant world mutation",
        ],
        "memory_fuzz_pressure": [
            "memory nearly literal",
            "very light softening",
            "light fuzz",
            "mild recombination",
            "noticeable drift",
            "moderate fuzzing",
            "strong recombination",
            "heavy memory mutation",
            "aggressive memory blur",
            "dominant memory destabilization",
        ],
        "phrase_rebinding_pressure": [
            "relations stay fixed",
            "tiny relation wobble",
            "light rebinding",
            "mild relational drift",
            "noticeable rebinding",
            "moderate phrase remap",
            "strong relation shift",
            "aggressive rebinding",
            "near-constant relation remap",
            "dominant structural rebinding",
        ],
        "event_instability": [
            "event logic stays stable",
            "very light event wobble",
            "small event drift",
            "mild causal slippage",
            "noticeable event mutation",
            "moderate sequence drift",
            "strong causal displacement",
            "high event instability",
            "severe event folding",
            "dominant event mutation",
        ],
        "scene_morph_pressure": [
            "scene nearly fixed",
            "faint morphing",
            "light scene drift",
            "mild environmental shift",
            "noticeable scene mutation",
            "moderate morphing",
            "strong scene warp",
            "high environmental instability",
            "severe scene replacement",
            "dominant scene metamorphosis",
        ],
        "banal_intrusion_allowance": [
            "no banal intrusion",
            "almost none",
            "rare small intrusions",
            "occasional minor banalities",
            "noticeable everyday leakage",
            "moderate banal presence",
            "strong banal interruption",
            "high low-status intrusion",
            "persistent mundane disruption",
            "dominant banal contamination",
        ],
        "translation_density": [
            "inner pressure stays hidden",
            "very faint symbols",
            "light outerization",
            "mild symbol emergence",
            "noticeable translation",
            "moderate symbolic embodiment",
            "strong translation",
            "dense symbolization",
            "very dense symbolic worlding",
            "dominant translation field",
        ],
        "continuity_loosening": [
            "continuity almost fixed",
            "very light loosening",
            "small continuity wobble",
            "mild looseness",
            "noticeable drift",
            "moderate continuity slippage",
            "strong local/global split",
            "high continuity fracture",
            "severe continuity looseness",
            "dominant continuity instability",
        ],
        "contradiction_tolerance": [
            "contradiction rejected",
            "very low tolerance",
            "low tolerance",
            "mild tolerance",
            "noticeable tolerance",
            "moderate tolerance",
            "strong tolerance",
            "high tolerance",
            "very high tolerance",
            "contradiction fully lived",
        ],
        "micro_texture_distortion": [
            "surface almost clean",
            "very light texture noise",
            "light micro drift",
            "mild edge shimmer",
            "noticeable texture distortion",
            "moderate micro instability",
            "strong texture corruption",
            "high edge warping",
            "severe micro weirdness",
            "dominant micro distortion",
        ],
        "observer_agency_damping": [
            "observer mostly active",
            "very light damping",
            "light damping",
            "somewhat reduced control",
            "partial loss of control",
            "observer mostly reactive",
            "observer carried by events",
            "strong passivity",
            "very low authorship",
            "near-total carried witness",
        ],
        "observer_detachment": [
            "fully identified self",
            "very slight detachment",
            "light detachment",
            "partial distancing",
            "noticeable self-observing gap",
            "moderate detachment",
            "strong witness split",
            "high self-distance",
            "very strong detachment",
            "near-total observer distance",
        ],
        "interpretation_latency": [
            "instant explanation",
            "very quick interpretation",
            "quick interpretation",
            "slightly delayed meaning",
            "noticeable delay",
            "moderate interpretation lag",
            "strong delay",
            "high latency",
            "very high latency",
            "meaning arrives last",
        ],
        "witness_intensity": [
            "barely witnessing",
            "very faint witness",
            "light witness presence",
            "partial witness",
            "noticeable witness",
            "moderate witness strength",
            "strong witness",
            "high witness intensity",
            "very high witness intensity",
            "dominant witness field",
        ],
        "lucidity_softness": [
            "hard non-lucid",
            "deeply veiled",
            "low soft lucidity",
            "faint reflective edge",
            "mild soft lucidity",
            "semi-lucid softness",
            "clear reflective edge",
            "strong soft lucidity",
            "very high soft lucidity",
            "lucid but still porous",
        ],
        "self_boundary_softening": [
            "self boundary rigid",
            "very slight softening",
            "light softening",
            "mild permeability",
            "noticeable boundary drift",
            "moderate permeability",
            "strong self/world leakage",
            "high self-boundary softness",
            "very porous self-boundary",
            "self/world highly permeable",
        ],
    }
    return tables[slot][d]


def transform_digit(base_digit: int, triple: Tuple[int, int, int]) -> int:
    mul_num, mul_den, offset = triple
    return clamp_digit(round(base_digit * mul_num / mul_den) + offset)


def world_hard_constraints(phase: str, digits: Dict[str, int]) -> List[str]:
    rules: List[str] = []
    if digits["world_shift_pressure"] <= 2 and digits["scene_morph_pressure"] <= 2:
        rules.append("Reject large scene replacement, full environment flips, or dominant world mutation.")
    elif digits["world_shift_pressure"] >= 6 or digits["scene_morph_pressure"] >= 6:
        rules.append("Allow strong world shifts, scene replacement, and reality-version slippage when local conviction survives.")
    if digits["memory_fuzz_pressure"] <= 2:
        rules.append("Keep memory mutation light; preserve more literal continuity of remembered structures.")
    elif digits["memory_fuzz_pressure"] >= 6:
        rules.append("Permit strong memory fuzzing, cousin-memory substitution, and affect-preserving factual drift.")
    if digits["translation_density"] <= 2:
        rules.append("Keep translation sparse and indirect.")
    elif digits["translation_density"] >= 6:
        rules.append("Translate inner pressure outwardly through environments, objects, and events rather than commentary.")
    if digits["banal_intrusion_allowance"] <= 2:
        rules.append("Keep banal intrusion rare and small.")
    elif digits["banal_intrusion_allowance"] >= 6:
        rules.append("Permit low-status mundane intrusions when they increase dream-truth.")
    return rules


def observer_hard_constraints(phase: str, digits: Dict[str, int]) -> List[str]:
    rules: List[str] = []
    if digits["observer_agency_damping"] >= 5:
        rules.append("Do not take control too early.")
    if digits["observer_detachment"] >= 4:
        rules.append("Allow detached participation without commentary.")
    if digits["interpretation_latency"] >= 4:
        rules.append("Delay explanation; let noticing arrive before understanding.")
    if digits["witness_intensity"] >= 4:
        rules.append("Preserve witness continuity even when action occurs.")
    if digits["lucidity_softness"] >= 6:
        rules.append("Permit a soft reflective edge without restoring waking control.")
    return rules


def build_profiles(base_digits: Dict[str, int]):
    world_profiles: Dict[str, dict] = {}
    observer_profiles: Dict[str, dict] = {}

    for phase in PHASES:
        world_values = {
            slot: transform_digit(base_digits[slot], triple)
            for slot, triple in PHASE_TRANSFORMS[phase]["world"].items()
        }
        observer_values = {
            slot: transform_digit(base_digits[slot], triple)
            for slot, triple in PHASE_TRANSFORMS[phase]["observer"].items()
        }

        if phase == "03_dream":
            world_values["world_shift_pressure"] = max(world_values["world_shift_pressure"], 4)
            world_values["scene_morph_pressure"] = max(world_values["scene_morph_pressure"], 4)
            world_values["memory_fuzz_pressure"] = max(world_values["memory_fuzz_pressure"], 4)
            world_values["translation_density"] = max(world_values["translation_density"], 4)
            observer_values["observer_agency_damping"] = max(observer_values["observer_agency_damping"], 5)
            observer_values["observer_detachment"] = max(observer_values["observer_detachment"], 4)
            observer_values["interpretation_latency"] = max(observer_values["interpretation_latency"], 4)
            observer_values["witness_intensity"] = max(observer_values["witness_intensity"], 4)
            observer_values["self_boundary_softening"] = max(observer_values["self_boundary_softening"], 4)
        elif phase == "04_distill":
            observer_values["witness_intensity"] = max(observer_values["witness_intensity"], 5)
        elif phase == "05_finalize":
            observer_values["witness_intensity"] = max(observer_values["witness_intensity"], 7)

        world_profiles[phase] = {
            "digits": world_values,
            "labels": {k: digit_label(k, v) for k, v in world_values.items()},
            "hard_constraints": world_hard_constraints(phase, world_values),
        }
        observer_profiles[phase] = {
            "digits": observer_values,
            "labels": {k: digit_label(k, v) for k, v in observer_values.items()},
            "hard_constraints": observer_hard_constraints(phase, observer_values),
        }

    return world_profiles, observer_profiles


def write_json(path: Path, payload: dict):
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def constraints_block(items: List[str]) -> str:
    if not items:
        return "- none"
    return "\n".join(f"- {x}" for x in items)


def write_profiles_md(source: str, round_value, sig_prefix: str, world_profiles: dict, observer_profiles: dict, base_digits: dict):
    combined_lines = [
        "# Turbulence Profile",
        f"seed source: {source}",
        f"round: {round_value}",
        f"signature prefix: {sig_prefix}",
        "",
        "## Base slot digits",
    ]
    for slot in BASE_SLOTS:
        combined_lines.append(f"- {slot}: {base_digits[slot]} — {digit_label(slot, base_digits[slot])}")
    combined_lines.extend(["", "See also:", "- world_turbulence_profile.md", "- observer_turbulence_profile.md", ""])
    COMBINED_MD.write_text("\n".join(combined_lines) + "\n", encoding="utf-8")

    world_lines = [
        "# World Turbulence Profile",
        f"seed source: {source}",
        f"round: {round_value}",
        f"signature prefix: {sig_prefix}",
        "",
    ]
    for phase in PHASES:
        world_lines.append(f"## Phase {phase}")
        for slot, digit in world_profiles[phase]["digits"].items():
            world_lines.append(f"- {slot}: {digit} — {world_profiles[phase]['labels'][slot]}")
        if world_profiles[phase]["hard_constraints"]:
            world_lines.append("")
            world_lines.append("### Hard constraints")
            for rule in world_profiles[phase]["hard_constraints"]:
                world_lines.append(f"- {rule}")
        world_lines.append("")
    WORLD_MD.write_text("\n".join(world_lines) + "\n", encoding="utf-8")

    observer_lines = [
        "# Observer Turbulence Profile",
        f"seed source: {source}",
        f"round: {round_value}",
        f"signature prefix: {sig_prefix}",
        "",
    ]
    for phase in PHASES:
        observer_lines.append(f"## Phase {phase}")
        for slot, digit in observer_profiles[phase]["digits"].items():
            observer_lines.append(f"- {slot}: {digit} — {observer_profiles[phase]['labels'][slot]}")
        if observer_profiles[phase]["hard_constraints"]:
            observer_lines.append("")
            observer_lines.append("### Hard constraints")
            for rule in observer_profiles[phase]["hard_constraints"]:
                observer_lines.append(f"- {rule}")
        observer_lines.append("")
    OBSERVER_MD.write_text("\n".join(observer_lines) + "\n", encoding="utf-8")


def infer_phase_and_side(template_path: Path) -> Tuple[str, str]:
    rel = template_path.relative_to(TEMPLATE_DIR)
    folder = rel.parts[0]
    phase_prefix = None
    for prefix in PHASE_PREFIX_TO_KEY:
        if folder.startswith(prefix + "-"):
            phase_prefix = prefix
            break
    if phase_prefix is None:
        raise ValueError(f"Cannot infer phase from template folder: {folder}")
    phase_key = PHASE_PREFIX_TO_KEY[phase_prefix]
    side = "world" if folder.endswith("-world") else "observe"
    return phase_key, side


def build_mapping(template_path: Path, world_profiles: dict, observer_profiles: dict) -> Dict[str, str]:
    phase_key, side = infer_phase_and_side(template_path)
    profile = world_profiles[phase_key] if side == "world" else observer_profiles[phase_key]

    mapping: Dict[str, str] = {}
    for slot, label in profile["labels"].items():
        mapping[f"{slot}_label"] = label
    mapping["hard_constraints_block"] = constraints_block(profile["hard_constraints"])
    return mapping


def render_template_text(template_path: Path, mapping: Dict[str, str]) -> str:
    text = template_path.read_text(encoding="utf-8")
    for key, value in mapping.items():
        text = text.replace("{{" + key + "}}", value)
    unresolved = sorted(set(re.findall(r"\{\{(.*?)\}\}", text)))
    if unresolved:
        raise ValueError(f"Unresolved placeholders in {template_path.name}: {', '.join(unresolved)}")
    return text


def compile_templates(world_profiles: dict, observer_profiles: dict):
    if not TEMPLATE_DIR.exists():
        raise SystemExit(f"Missing template directory: {TEMPLATE_DIR}")

    for template_path in sorted(TEMPLATE_DIR.rglob("*.tpl.md")):
        mapping = build_mapping(template_path, world_profiles, observer_profiles)
        rendered = render_template_text(template_path, mapping)
        output_name = template_path.name.replace(".tpl", "")
        output_path = DREAM_DIR / output_name
        output_path.write_text(rendered, encoding="utf-8")


def main():
    if not SEED_JSON.exists():
        raise SystemExit(f"Missing seed file: {SEED_JSON}")

    seed = json.loads(SEED_JSON.read_text(encoding="utf-8"))
    round_value = seed.get("round")
    signature = str(seed.get("signature", ""))
    previous_signature = str(seed.get("previous_signature", ""))

    if not signature:
        raise SystemExit("session_seed.json has no signature field")

    seed_material = f"{round_value}:{signature}:{previous_signature}".encode("utf-8")
    digits = expand_bytes(seed_material, len(BASE_SLOTS))
    base_digits = {slot: digits[i] for i, slot in enumerate(BASE_SLOTS)}

    world_profiles, observer_profiles = build_profiles(base_digits)

    combined_payload = {
        "seed_source": "drand default beacon",
        "round": round_value,
        "signature_prefix": signature[:24],
        "base_digits": base_digits,
        "world_profiles": world_profiles,
        "observer_profiles": observer_profiles,
    }
    world_payload = {
        "seed_source": "drand default beacon",
        "round": round_value,
        "signature_prefix": signature[:24],
        "profiles": world_profiles,
    }
    observer_payload = {
        "seed_source": "drand default beacon",
        "round": round_value,
        "signature_prefix": signature[:24],
        "profiles": observer_profiles,
    }

    write_json(COMBINED_JSON, combined_payload)
    write_json(WORLD_JSON, world_payload)
    write_json(OBSERVER_JSON, observer_payload)
    write_profiles_md("drand default beacon", round_value, signature[:24], world_profiles, observer_profiles, base_digits)
    compile_templates(world_profiles, observer_profiles)


if __name__ == "__main__":
    main()
