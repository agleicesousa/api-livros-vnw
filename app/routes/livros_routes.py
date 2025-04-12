from flask import Blueprint
from app.controllers import (
    criar_livros,
    listar_livros
)

livros_routes = Blueprint('livros', __name__)

livros_routes.route("/", methods=["POST"])(criar_livros)
livros_routes.route("/", methods=["GET"])(listar_livros)