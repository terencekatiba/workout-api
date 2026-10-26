# Workout API

A RESTful backend API for managing workouts and exercises, built with Flask, Flask-SQLAlchemy, Flask-Migrate, and Marshmallow.

## Features

- Create, retrieve, list, and delete workouts.
- Create, retrieve, list, and delete exercises.
- Associate exercises with workouts.
- Record repetitions, sets, and exercise duration.
- Validate incoming JSON data using Marshmallow.
- Enforce database constraints using SQLAlchemy.
- Manage database schema changes with Flask-Migrate.
- Run automated API tests with pytest.

## Technologies

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Marshmallow
- SQLite
- pytest

## Installation

Clone the repository and enter the project directory.

Install dependencies using Pipenv:

```bash
pipenv install --dev
```

If Pipenv does not automatically find the project's Pipfile, use:

```bash
PIPENV_PIPFILE="$HOME/workout-api/Pipfile" pipenv install --dev
```

## Database Setup

The application uses SQLite and stores its database in the Flask instance directory.

To apply database migrations on a fresh database:

```bash
PIPENV_PIPFILE="$HOME/workout-api/Pipfile" pipenv run flask --app server.app db upgrade
```

To initialize a migration repository for future schema changes, if needed:

```bash
PIPENV_PIPFILE="$HOME/workout-api/Pipfile" pipenv run flask --app server.app db init
```

The migration repository is already included in this project, so do not run `db init` again in the existing project.

## Seed Sample Data

Run:

```bash
PIPENV_PIPFILE="$HOME/workout-api/Pipfile" pipenv run python -m server.seed
```

The seed script adds sample exercises and a workout with associated exercises.

## Start the Server

```bash
PIPENV_PIPFILE="$HOME/workout-api/Pipfile" pipenv run flask --app server.app run --debug
```

By default, the development server is available at `http://127.0.0.1:5000`.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API health check |
| GET | `/workouts` | List workouts |
| GET | `/workouts/<workout_id>` | Retrieve one workout |
| POST | `/workouts` | Create a workout |
| DELETE | `/workouts/<workout_id>` | Delete a workout |
| GET | `/exercises` | List exercises |
| GET | `/exercises/<exercise_id>` | Retrieve one exercise |
| POST | `/exercises` | Create an exercise |
| DELETE | `/exercises/<exercise_id>` | Delete an exercise |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout |

## Example Requests

### Create an Exercise

`POST /exercises`

```json
{
  "name": "Push-ups",
  "category": "Strength",
  "equipment_needed": false
}
```

### Create a Workout

`POST /workouts`

```json
{
  "date": "2026-10-26",
  "duration_minutes": 30,
  "notes": "Morning workout"
}
```

### Add an Exercise to a Workout

`POST /workouts/1/exercises/1/workout_exercises`

```json
{
  "reps": 12,
  "sets": 3
}
```

Use existing workout and exercise IDs in the URL.

## Validation and Error Handling

- Workout duration must be greater than zero.
- Exercise names and categories are required and length-limited.
- Exercise names must be unique.
- Repetitions, sets, and exercise duration must be positive when provided.
- At least one activity detail must be provided when associating an exercise with a workout.
- Invalid input returns a `400` response.
- Requests for missing workouts or exercises return `404`.

## Run Tests

Execute the test suite:

```bash
PIPENV_PIPFILE="$HOME/workout-api/Pipfile" pipenv run pytest -v
```

The tests cover health checks, CRUD operations, validation, missing records, and workout-exercise associations.

## Project Structure

```text
workout-api/
├── migrations/
├── server/
│   ├── __init__.py
│   ├── app.py
│   ├── models.py
│   ├── schemas.py
│   └── seed.py
├── tests/
│   └── test_api.py
├── Pipfile
├── Pipfile.lock
└── README.md
```

## Development Notes

This project is intended for learning and development. Before production use, add authentication, more comprehensive integration tests, production configuration, and deployment settings.
