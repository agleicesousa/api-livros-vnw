from marshmallow import Schema, fields, validates, ValidationError
import re

class LivroSchema(Schema):
    titulo = fields.Str(required=True)
    categoria = fields.Str(required=True)
    autor = fields.Str(required=True)
    image_url = fields.Url(required=True, error_messages={"invalid": "URL inválida"})

    @validates("image_url")
    def validar_extensao_imagem(self, valor):
        if not re.match(r'^https?:\/\/.+\.(jpg|jpeg|png|webp)$', valor, re.IGNORECASE):
            raise ValidationError("A URL deve terminar com .jpg, .jpeg, .png ou .webp")
