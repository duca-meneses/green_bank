from marshmallow import Schema, fields


class MessageSchema(Schema):
    message = fields.String(required=True)

class HealthCheckSchema(Schema):
    status = fields.String(required=True)
