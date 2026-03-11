# Development Agent Body-Part Submodule

This document explains how `DevelopmentAgent` organizes generated implementation code by robot body part.

## Where The Code Lives

- `agents/development_modules/body_parts/legs.py`
- `agents/development_modules/body_parts/arms.py`
- `agents/development_modules/body_parts/waist.py`
- `agents/development_modules/body_parts/sensors.py`
- `agents/development_modules/registry.py`

## Body Part: Legs

Code entry: `build_legs_module(spec)`

What it does:
- Uses leg-related robot specs such as per-leg DOF, leg length, and knee torque limits.
- Maps implementation to locomotion pipeline code (`envs/reward.py`, `envs/humanoid_env.py`, `training/train_ppo.py`).
- Defines functional goals for gait learning: forward motion, efficiency, and stability.

How it functions:
- Produces a structured dict that describes purpose, code references, and behavior expectations.
- The returned dict is consumed by `DevelopmentAgent` to expose development scope in shared state.

## Body Part: Arms

Code entry: `build_arms_module(spec)`

What it does:
- Uses arm DOF, arm span, and payload constraints.
- Associates arm behavior with development/evaluation scripts.
- Documents how arm posture contributes to balance and future manipulation.

How it functions:
- Returns a body-part plan block used for architecture visibility and implementation tracking.

## Body Part: Waist

Code entry: `build_waist_module(spec)`

What it does:
- Uses waist DOF and waist ROM limits.
- Links torso control behavior to reward wrapper and training callback code.
- Clarifies heading stabilization and core-orientation tuning responsibilities.

How it functions:
- Creates a spec-aware module description for core stabilization responsibilities.

## Body Part: Sensors

Code entry: `build_sensors_module(spec)`

What it does:
- Uses perception and encoder settings.
- Ties observation handling to environment creation, evaluation, and testing agents.
- Keeps integration points ready for future real sensor adapters.

How it functions:
- Produces a structured module block for observation pipeline responsibilities.

## Orchestration: Registry

Code entry: `build_body_part_plan(spec)` in `agents/development_modules/registry.py`

What it does:
- Calls each body-part builder.
- Returns an ordered list of module definitions.
- Serves as one integration point used by `DevelopmentAgent`.

## DevelopmentAgent Integration

`DevelopmentAgent` imports `build_body_part_plan(spec)` and writes its output to state key:

- `body_part_modules`

This makes all body-part implementation details visible to:
- pipeline state
- documentation flow
- future UI rendering
