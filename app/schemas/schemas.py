from marshmallow import Schema, fields


class AuthTokenSchema(Schema):
    callback_url = fields.String(required=True)
