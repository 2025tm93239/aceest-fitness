from aceest.programs import PROGRAMS


def list_program_names():
    return sorted(PROGRAMS.keys())


def get_program(name: str) -> dict:
    if name not in PROGRAMS:
        raise KeyError(name)
    return PROGRAMS[name]


def estimate_calories(weight_kg: float, program_name: str) -> int:
    if weight_kg <= 0:
        raise ValueError("weight_kg must be positive")
    program = get_program(program_name)
    return int(weight_kg * program["calorie_factor"])


def validate_client_payload(payload: dict) -> dict:
    required = ("name", "age", "weight_kg", "program", "adherence_pct")
    missing = [field for field in required if field not in payload]
    if missing:
        raise ValueError(f"Missing fields: {', '.join(missing)}")

    name = str(payload["name"]).strip()
    if not name:
        raise ValueError("name cannot be empty")

    age = int(payload["age"])
    if age <= 0:
        raise ValueError("age must be positive")

    weight_kg = float(payload["weight_kg"])
    program = str(payload["program"])
    adherence_pct = int(payload["adherence_pct"])

    if program not in PROGRAMS:
        raise ValueError("invalid program")
    if not 0 <= adherence_pct <= 100:
        raise ValueError("adherence_pct must be between 0 and 100")

    calories = estimate_calories(weight_kg, program)

    return {
        "name": name,
        "age": age,
        "weight_kg": weight_kg,
        "program": program,
        "adherence_pct": adherence_pct,
        "calories": calories,
    }
