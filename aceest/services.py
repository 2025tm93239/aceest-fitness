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
