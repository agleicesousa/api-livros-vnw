from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from app.models import init_db
from app.routes import livros_bp

def create_app():
    load_dotenv()
    app = Flask(__name__)

    frontend_origin = os.getenv("FRONTEND_ORIGIN")
    CORS(app, resources={r"/": {"origins": frontend_origin}})

    init_db()
    app.register_blueprint(livros_bp)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', frontend_origin)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,PATCH')
        return response

    @app.route("/")
    def index():
        return "<h2>Bem-vindo à API de Doações de Livros!</h2>"

    return app
