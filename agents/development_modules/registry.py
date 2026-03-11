from typing import Any, Dict, List

from agents.development_modules.body_parts import (
    build_arms_module,
    build_legs_module,
    build_sensors_module,
    build_waist_module,
)


def build_body_part_plan(spec: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Build development plan entries grouped by robot body part."""
    return [
        build_legs_module(spec),
        build_arms_module(spec),
        build_waist_module(spec),
        build_sensors_module(spec),
    ]
