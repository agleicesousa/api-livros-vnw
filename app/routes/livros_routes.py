from flask import Blueprint
from app.controllers import (
    criar_livros
)

livros_routes = Blueprint('livros', __name__)

livros_routes.route("/", methods=["POST"])(criar_livros)