
from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)

    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100),
    )
    category = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=50),
    )
    equipment_needed = fields.Bool(load_default=False)


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(
        required=True,
        validate=validate.Range(min=1),
    )
    notes = fields.Str(allow_none=True)


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)

    reps = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1),
    )
    sets = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1),
    )
    duration_seconds = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1),
    )

    @validates_schema
    def validate_activity_details(self, data, **kwargs):
        if not any(
            data.get(field) is not None
            for field in ("reps", "sets", "duration_seconds")
        ):
            raise ValidationError(
                "Provide at least one of reps, sets, or duration_seconds."
            )
