from marshmallow import Schema, fields

class LivroSchema(Schema):
    titulo = fields.Str(required=True)
    categoria = fields.Str(required=True)
    autor = fields.Str(required=True)
    image_url = fields.Url(required=True, error_messages={"invalid": "URL inválida"})
