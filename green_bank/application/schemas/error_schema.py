from marshmallow import Schema, fields


class ExceptionSchema(Schema):
    message = fields.String(required=True)
    status_code = fields.Integer(required=True)


class ErrorSchema(Schema):
    errors = fields.List(fields.Nested(ExceptionSchema), required=True)
