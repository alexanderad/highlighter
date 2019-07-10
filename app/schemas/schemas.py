from marshmallow import Schema, fields


class AuthTokenSchema(Schema):
    callback_url = fields.String(required=True)


class WordSchema(Schema):
    lang = fields.String(required=True)
    word = fields.String(required=True)
    translation = fields.String(required=True)
    section = fields.String()
    section_rank = fields.Integer()
    frequency = fields.Float(required=True)
    example = fields.String(required=True)
