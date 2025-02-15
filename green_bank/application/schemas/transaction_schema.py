from marshmallow import Schema, fields


class CreateTransactionSchema(Schema):
    value = fields.Decimal()
    payer = fields.UUID()
    payee = fields.UUID()


class UserTransactionSchema(Schema):
    id = fields.UUID()
    name = fields.String()

class TransactionSchema(Schema):
    value = fields.Decimal()
    payer = fields.Nested(UserTransactionSchema)
    payee = fields.Nested(UserTransactionSchema)
    created = fields.DateTime()

