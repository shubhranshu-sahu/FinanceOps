from marshmallow import Schema, fields, validate

class TransactionSchema(Schema):
    amount = fields.Float(required=True, validate=validate.Range(min=0.01))
    type = fields.String(required=True, validate=validate.OneOf(["INCOME", "EXPENSE"]))
    category_id = fields.Integer(required=True)
    date = fields.Date(required=True)
    description = fields.String(required=False, allow_none=True)

class TransactionUpdateSchema(Schema):
    amount = fields.Float(required=False, validate=validate.Range(min=0.01))
    type = fields.String(required=False, validate=validate.OneOf(["INCOME", "EXPENSE"]))
    category_id = fields.Integer(required=False)
    date = fields.Date(required=False)
    description = fields.String(required=False, allow_none=True)

transaction_schema = TransactionSchema()
transaction_update_schema = TransactionUpdateSchema()
