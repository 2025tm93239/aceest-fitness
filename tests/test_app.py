def test_health(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_list_programs(client):
    response = client.get("/programs")
    body = response.get_json()
    assert response.status_code == 200
    assert "Fat Loss (FL)" in body["programs"]


def test_program_detail_not_found(client):
    assert client.get("/programs/Unknown").status_code == 404


def test_create_and_fetch_client(client):
    payload = {
        "name": "Anita",
        "age": 32,
        "weight_kg": 65,
        "program": "Beginner (BG)",
        "adherence_pct": 90,
    }
    create = client.post("/clients", json=payload)
    assert create.status_code == 201
    assert create.get_json()["calories"] == 1690

    listed = client.get("/clients")
    assert len(listed.get_json()["clients"]) == 1

    detail = client.get("/clients/Anita")
    assert detail.status_code == 200


def test_calories_endpoint(client):
    response = client.post(
        "/calories",
        json={"weight_kg": 80, "program": "Fat Loss (FL)"},
    )
    assert response.status_code == 200
    assert response.get_json()["calories"] == 1760
