
import pytest

from server.app import create_app
from server.models import db


@pytest.fixture
def client():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite://",
        "SQLALCHEMY_ENGINE_OPTIONS": {
            "poolclass": __import__(
                "sqlalchemy.pool", fromlist=["StaticPool"]
            ).StaticPool,
            "connect_args": {"check_same_thread": False},
        },
    })

    with app.app_context():
        db.create_all()

    with app.test_client() as client:
        yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()


def create_exercise(client, name="Push-ups"):
    return client.post("/exercises", json={
        "name": name,
        "category": "Strength",
        "equipment_needed": False,
    })


def create_workout(client):
    return client.post("/workouts", json={
        "date": "2026-10-25",
        "duration_minutes": 30,
        "notes": "Morning workout",
    })


def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["status"] == "success"


def test_create_and_list_exercises(client):
    response = create_exercise(client)
    assert response.status_code == 201
    assert response.get_json()["name"] == "Push-ups"

    response = client.get("/exercises")
    assert response.status_code == 200
    assert len(response.get_json()) == 1


def test_duplicate_exercise_name_is_rejected(client):
    create_exercise(client)
    response = create_exercise(client)

    assert response.status_code == 400


def test_invalid_exercise_is_rejected(client):
    response = client.post("/exercises", json={
        "name": "",
        "category": "Strength",
    })

    assert response.status_code == 400


def test_create_and_get_workout(client):
    response = create_workout(client)
    assert response.status_code == 201

    workout_id = response.get_json()["id"]
    response = client.get(f"/workouts/{workout_id}")

    assert response.status_code == 200
    assert response.get_json()["duration_minutes"] == 30


def test_invalid_workout_duration_is_rejected(client):
    response = client.post("/workouts", json={
        "date": "2026-10-25",
        "duration_minutes": 0,
    })

    assert response.status_code == 400


def test_missing_workout_returns_404(client):
    response = client.get("/workouts/9999")
    assert response.status_code == 404


def test_add_exercise_to_workout(client):
    exercise = create_exercise(client).get_json()
    workout = create_workout(client).get_json()

    response = client.post(
        f"/workouts/{workout['id']}/exercises/"
        f"{exercise['id']}/workout_exercises",
        json={"reps": 12, "sets": 3},
    )

    assert response.status_code == 201
    assert response.get_json()["reps"] == 12
    assert response.get_json()["sets"] == 3


def test_workout_exercise_requires_activity_details(client):
    exercise = create_exercise(client).get_json()
    workout = create_workout(client).get_json()

    response = client.post(
        f"/workouts/{workout['id']}/exercises/"
        f"{exercise['id']}/workout_exercises",
        json={},
    )

    assert response.status_code == 400


def test_delete_workout(client):
    workout = create_workout(client).get_json()

    response = client.delete(f"/workouts/{workout['id']}")
    assert response.status_code == 200

    response = client.get(f"/workouts/{workout['id']}")
    assert response.status_code == 404


def test_delete_exercise(client):
    exercise = create_exercise(client).get_json()

    response = client.delete(f"/exercises/{exercise['id']}")
    assert response.status_code == 200

    response = client.get(f"/exercises/{exercise['id']}")
    assert response.status_code == 404
