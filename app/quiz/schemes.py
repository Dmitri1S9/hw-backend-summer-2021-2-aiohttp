from marshmallow import Schema, fields, ValidationError, validates_schema


class ThemeSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)


class AnswerSchema(Schema):
    title = fields.Str(required=True)
    is_correct = fields.Bool(required=True)


class QuestionSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)
    theme_id = fields.Int(required=True)
    answers = fields.List(fields.Nested(AnswerSchema), required=True)

    @validates_schema
    def validate_answers(self, data, **kwargs):
        answers = data.get("answers", [])

        if len(answers) < 2:
            raise ValidationError("1WW", field_name="answers")

        correct_count = sum(1 for a in answers if a.get("is_correct"))
        if correct_count == 0:
            raise ValidationError("2WW", field_name="answers")

        if correct_count > 1:
            raise ValidationError("3WW", field_name="answers")


class ThemeListSchema(Schema):
    themes = fields.List(fields.Nested(ThemeSchema))


class ThemeIdSchema(Schema):
    pass


class ListQuestionSchema(Schema):
    questions = fields.List(fields.Nested(QuestionSchema))
