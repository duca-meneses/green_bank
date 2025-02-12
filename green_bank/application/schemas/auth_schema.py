from marshmallow import Schema, fields


class CreateLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class TokenSchema(Schema):
    access_token = fields.String(required=True)

class PasswordChangeSchema(Schema):
    old_password = fields.String(required=True)
    new_password = fields.String(required=True)
    new_password_confirm = fields.String(required=True)
