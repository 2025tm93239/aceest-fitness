from flask import Flask, jsonify

from aceest.programs import GYM_METRICS, PROGRAMS, list_program_names


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def health():
        return jsonify({"service": "ACEest Fitness & Gym", "status": "ok"})

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
            }
        )

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
