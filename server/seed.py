
from datetime import date

from server.app import create_app
from server.models import db, Exercise, Workout, WorkoutExercise


def seed():
    app = create_app()

    with app.app_context():
        db.create_all()

        exercises = [
            Exercise(
                name="Push-ups",
                category="Strength",
                equipment_needed=False,
            ),
            Exercise(
                name="Squats",
                category="Strength",
                equipment_needed=False,
            ),
            Exercise(
                name="Running",
                category="Cardio",
                equipment_needed=False,
            ),
        ]

        for exercise in exercises:
            existing = Exercise.query.filter_by(name=exercise.name).first()
            if existing is None:
                db.session.add(exercise)

        db.session.commit()

        workout = Workout.query.filter_by(
            date=date.today(),
            notes="Sample full-body workout",
        ).first()

        if workout is None:
            workout = Workout(
                date=date.today(),
                duration_minutes=40,
                notes="Sample full-body workout",
            )
            db.session.add(workout)
            db.session.flush()

            pushups = Exercise.query.filter_by(name="Push-ups").first()
            squats = Exercise.query.filter_by(name="Squats").first()

            db.session.add_all([
                WorkoutExercise(
                    workout_id=workout.id,
                    exercise_id=pushups.id,
                    reps=10,
                    sets=3,
                ),
                WorkoutExercise(
                    workout_id=workout.id,
                    exercise_id=squats.id,
                    reps=12,
                    sets=3,
                ),
            ])

        db.session.commit()
        print("Seed data created successfully.")


if __name__ == "__main__":
    seed()
