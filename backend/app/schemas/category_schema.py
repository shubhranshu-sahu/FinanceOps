from marshmallow import Schema, fields, validate

class CategorySchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, error="Category name cannot be empty."))

category_schema = CategorySchema()
