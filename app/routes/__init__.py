from flask import Blueprint
from .livros_routes import livros_routes

livros_bp = Blueprint('livros', __name__, url_prefix='/livros')
livros_bp.register_blueprint(livros_routes)
