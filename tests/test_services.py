import pytest

from aceest.services import estimate_calories, validate_client_payload


def test_estimate_calories_fat_loss():
    assert estimate_calories(70, "Fat Loss (FL)") == 1540


def test_estimate_calories_rejects_invalid_weight():
    with pytest.raises(ValueError):
        estimate_calories(0, "Fat Loss (FL)")


def test_validate_client_payload_success():
    client = validate_client_payload(
        {
            "name": "Ravi",
            "age": 28,
            "weight_kg": 72,
            "program": "Muscle Gain (MG)",
            "adherence_pct": 85,
        }
    )
    assert client["calories"] == 2520
