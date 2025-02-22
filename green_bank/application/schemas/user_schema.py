from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.UUID(required=True)
    name = fields.String(required=True)
    email = fields.Email(required=True)
    document_number = fields.String(required=True)
    wallet_balance = fields.Decimal(required=True)
    created = fields.DateTime(required=True)


class listUserSchema(Schema):
    users = fields.List(fields.Nested(UserSchema), required=True)


class CreateUserSchema(Schema):
    name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)
    document_number = fields.String(required=True)
    wallet_balance = fields.Decimal(required=True)


class UpdateUserSchema(Schema):
    id = fields.UUID(required=True)
    name = fields.String(required=True)
    email = fields.Email(required=True)
    created = fields.DateTime(required=False)
    updated = fields.DateTime(required=False)


class CreateUpdateUserSchema(Schema):
    name = fields.String(required=True)
    email = fields.Email(required=True)
