
from flask import Flask, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from server.models import db, Workout, Exercise, WorkoutExercise
from server.schemas import (
    WorkoutSchema,
    ExerciseSchema,
    WorkoutExerciseSchema,
)

migrate = Migrate()

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()


def create_app(test_config=None):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///workout.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return {"errors": error.messages}, 400

    @app.get("/")
    def index():
        return {"message": "Workout API is running", "status": "success"}

    # ---------------- WORKOUTS ----------------

    @app.get("/workouts")
    def get_workouts():
        workouts = Workout.query.order_by(Workout.id).all()
        return workouts_schema.dump(workouts), 200

    @app.get("/workouts/<int:workout_id>")
    def get_workout(workout_id):
        workout = db.session.get(Workout, workout_id)
        if workout is None:
            return {"error": "Workout not found"}, 404
        return workout_schema.dump(workout), 200

    @app.post("/workouts")
    def create_workout():
        data = workout_schema.load(request.get_json() or {})
        workout = Workout(**data)
        db.session.add(workout)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {"error": "Invalid workout data"}, 400

        return workout_schema.dump(workout), 201

    @app.delete("/workouts/<int:workout_id>")
    def delete_workout(workout_id):
        workout = db.session.get(Workout, workout_id)
        if workout is None:
            return {"error": "Workout not found"}, 404

        db.session.delete(workout)
        db.session.commit()
        return {"message": "Workout deleted successfully"}, 200

    # ---------------- EXERCISES ----------------

    @app.get("/exercises")
    def get_exercises():
        exercises = Exercise.query.order_by(Exercise.id).all()
        return exercises_schema.dump(exercises), 200

    @app.get("/exercises/<int:exercise_id>")
    def get_exercise(exercise_id):
        exercise = db.session.get(Exercise, exercise_id)
        if exercise is None:
            return {"error": "Exercise not found"}, 404
        return exercise_schema.dump(exercise), 200

    @app.post("/exercises")
    def create_exercise():
        data = exercise_schema.load(request.get_json() or {})
        exercise = Exercise(**data)
        db.session.add(exercise)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {"error": "Exercise may already exist or data is invalid"}, 400

        return exercise_schema.dump(exercise), 201

    @app.delete("/exercises/<int:exercise_id>")
    def delete_exercise(exercise_id):
        exercise = db.session.get(Exercise, exercise_id)
        if exercise is None:
            return {"error": "Exercise not found"}, 404

        db.session.delete(exercise)
        db.session.commit()
        return {"message": "Exercise deleted successfully"}, 200

    # -------- ADD EXERCISE TO WORKOUT --------

    @app.post(
        "/workouts/<int:workout_id>/exercises/"
        "<int:exercise_id>/workout_exercises"
    )
    def add_exercise_to_workout(workout_id, exercise_id):
        workout = db.session.get(Workout, workout_id)
        exercise = db.session.get(Exercise, exercise_id)

        if workout is None:
            return {"error": "Workout not found"}, 404
        if exercise is None:
            return {"error": "Exercise not found"}, 404

        data = workout_exercise_schema.load(request.get_json() or {})

        association = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            **data,
        )
        db.session.add(association)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {"error": "Invalid workout exercise data"}, 400

        return {
            "id": association.id,
            "workout_id": association.workout_id,
            "exercise_id": association.exercise_id,
            "reps": association.reps,
            "sets": association.sets,
            "duration_seconds": association.duration_seconds,
        }, 201

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)

