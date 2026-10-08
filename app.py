from flask import Flask, jsonify, request

from aceest.programs import GYM_METRICS, PROGRAMS
from aceest.services import estimate_calories, list_program_names, validate_client_payload
from aceest.storage import get_client, list_clients, save_client


def create_app(testing: bool = False) -> Flask:
    app = Flask(__name__)
    app.config["TESTING"] = testing

    @app.get("/")
    def health():
        return jsonify({"service": "ACEest Fitness & Gym", "status": "ok", "version": "1.0.0"})

    @app.get("/metrics")
    def metrics():
        return jsonify(GYM_METRICS)

    @app.get("/programs")
    def programs():
        return jsonify({"programs": list_program_names()})

    @app.get("/programs/<path:program_name>")
    def program_detail(program_name: str):
        if program_name not in PROGRAMS:
            return jsonify({"error": "program not found"}), 404
        data = PROGRAMS[program_name]
        return jsonify(
            {
                "name": program_name,
                "workout": data["workout"],
                "diet": data["diet"],
                "color": data["color"],
                "calorie_factor": data["calorie_factor"],
            }
        )

    @app.post("/calories")
    def calories():
        body = request.get_json(silent=True) or {}
        try:
            weight = float(body.get("weight_kg", 0))
            program = str(body.get("program", ""))
            value = estimate_calories(weight, program)
        except (TypeError, ValueError, KeyError) as exc:
            return jsonify({"error": str(exc)}), 400
        return jsonify({"weight_kg": weight, "program": program, "calories": value})

    @app.get("/clients")
    def clients():
        return jsonify({"clients": list_clients()})

    @app.post("/clients")
    def create_client():
        body = request.get_json(silent=True) or {}
        try:
            client = validate_client_payload(body)
        except (TypeError, ValueError) as exc:
            return jsonify({"error": str(exc)}), 400
        saved = save_client(client)
        return jsonify(saved), 201

    @app.get("/clients/<name>")
    def client_detail(name: str):
        client = get_client(name)
        if not client:
            return jsonify({"error": "client not found"}), 404
        return jsonify(client)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
