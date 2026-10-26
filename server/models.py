
from datetime import date

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint


db = SQLAlchemy()


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=date.today)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    __table_args__ = (
        CheckConstraint(
            "duration_minutes > 0",
            name="check_workout_duration_positive",
        ),
    )

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan",
    )

    exercises = db.relationship(
        "Exercise",
        secondary="workout_exercises",
        viewonly=True,
    )

    def __repr__(self):
        return f"<Workout id={self.id} date={self.date}>"


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan",
    )

    workouts = db.relationship(
        "Workout",
        secondary="workout_exercises",
        viewonly=True,
    )

    def __repr__(self):
        return f"<Exercise id={self.id} name={self.name!r}>"


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(
        db.Integer,
        db.ForeignKey("workouts.id"),
        nullable=False,
    )
    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey("exercises.id"),
        nullable=False,
    )

    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    __table_args__ = (
        CheckConstraint(
            "reps IS NULL OR reps > 0",
            name="check_reps_positive",
        ),
        CheckConstraint(
            "sets IS NULL OR sets > 0",
            name="check_sets_positive",
        ),
        CheckConstraint(
            "duration_seconds IS NULL OR duration_seconds > 0",
            name="check_exercise_duration_positive",
        ),
    )

    workout = db.relationship(
        "Workout",
        back_populates="workout_exercises",
    )
    exercise = db.relationship(
        "Exercise",
        back_populates="workout_exercises",
    )

    def __repr__(self):
        return (
            f"<WorkoutExercise workout_id={self.workout_id} "
            f"exercise_id={self.exercise_id}>"
        )
