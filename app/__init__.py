from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from app.models import init_db
from app.routes import livros_bp

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    frontend_origin = os.getenv("FRONTEND_ORIGIN")
    CORS(app, resources={r"/livros*": {"origins": frontend_origin}})

    init_db()
    app.register_blueprint(livros_bp)

    @app.route("/")
    def index():
        return "<h2>Bem-vindo à API de Doações de Livros!</h2>"

    return app
