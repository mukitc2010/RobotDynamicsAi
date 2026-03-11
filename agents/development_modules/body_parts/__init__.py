"""Body-part implementations used by DevelopmentAgent."""

from agents.development_modules.body_parts.legs import build_legs_module
from agents.development_modules.body_parts.arms import build_arms_module
from agents.development_modules.body_parts.waist import build_waist_module
from agents.development_modules.body_parts.sensors import build_sensors_module

__all__ = [
    "build_legs_module",
    "build_arms_module",
    "build_waist_module",
    "build_sensors_module",
]
