from flask import Blueprint
from app.controllers import (
    criar_livros,
    listar_livros,
    buscar_livro,
    buscar_livro_por_titulo
)

livros_routes = Blueprint('livros', __name__)

livros_routes.route("/", methods=["POST"])(criar_livros)
livros_routes.route("/", methods=["GET"])(listar_livros)
livros_routes.route("/<int:id>", methods=["GET"])(buscar_livro)
livros_routes.route("/titulo/<string:titulo>", methods=["GET"])(buscar_livro_por_titulo)