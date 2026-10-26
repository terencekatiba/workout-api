
"""Baseline migration for the workout database."""

from alembic import op
import sqlalchemy as sa

revision = "e71f5025b05e"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "workouts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("duration_minutes", sa.Integer(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.CheckConstraint(
            "duration_minutes > 0",
            name="check_workout_duration_positive",
        ),
    )

    op.create_table(
        "exercises",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("category", sa.String(50), nullable=False),
        sa.Column(
            "equipment_needed",
            sa.Boolean(),
            nullable=False,
        ),
        sa.UniqueConstraint("name"),
    )

    op.create_table(
        "workout_exercises",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "workout_id",
            sa.Integer(),
            sa.ForeignKey("workouts.id"),
            nullable=False,
        ),
        sa.Column(
            "exercise_id",
            sa.Integer(),
            sa.ForeignKey("exercises.id"),
            nullable=False,
        ),
        sa.Column("reps", sa.Integer(), nullable=True),
        sa.Column("sets", sa.Integer(), nullable=True),
        sa.Column("duration_seconds", sa.Integer(), nullable=True),
        sa.CheckConstraint(
            "reps IS NULL OR reps > 0",
            name="check_reps_positive",
        ),
        sa.CheckConstraint(
            "sets IS NULL OR sets > 0",
            name="check_sets_positive",
        ),
        sa.CheckConstraint(
            "duration_seconds IS NULL OR duration_seconds > 0",
            name="check_exercise_duration_positive",
        ),
    )


def downgrade():
    op.drop_table("workout_exercises")
    op.drop_table("exercises")
    op.drop_table("workouts")
