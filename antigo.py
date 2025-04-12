import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
frontend_origin = os.getenv("FRONTEND_ORIGIN")
CORS(app, resources={r"/livros/*": {"origins": frontend_origin}})

# Função para inicializar o banco de dados
def init_db():
    with sqlite3.connect("database.db") as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS LIVROS(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                categoria TEXT NOT NULL,
                autor TEXT NOT NULL,
                image_url TEXT NOT NULL
            )
            """
        )

# Inicializa o banco de dados ao iniciar a aplicação
init_db()

# Configuração de CORS para permitir requisições do frontend
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', frontend_origin)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE')
    return response

# Página inicial
@app.route("/")
def index():
    return "<h2>Bem-vindo à API de Doações de Livros!</h2>"
    

# PATCH: Atualizar parcialmente um livro por ID
@app.route("/livros/<int:id>", methods=["PATCH"])
def atualizar_parcial_livro(id):
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Nenhum dado enviado para atualização"}), 400

    try:
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()

            # Monta dinamicamente a query apenas com os campos enviados
            campos_para_atualizar = ", ".join([f"{campo} = ?" for campo in dados.keys()])
            valores = list(dados.values()) + [id]

            cursor.execute(
                f"UPDATE LIVROS SET {campos_para_atualizar} WHERE id = ?", valores
            )
            conn.commit()

            if cursor.rowcount > 0:
                return jsonify({"mensagem": "Livro atualizado com sucesso"}), 200
            else:
                return jsonify({"erro": "Livro não encontrado"}), 404
    except sqlite3.Error as e:
        return jsonify({"erro": f"Erro ao atualizar livro: {str(e)}"}), 500

# DELETE: Rota para deletar um livro por ID
@app.route("/livros/<int:id>", methods=["DELETE"])
def deletar_livro(id):
    try:
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM LIVROS WHERE id = ?", (id,))
            conn.commit()

            if cursor.rowcount > 0:
                return jsonify({"mensagem": "Livro deletado com sucesso"}), 200
            else:
                return jsonify({"erro": "Livro não encontrado"}), 404
    except sqlite3.Error as e:
        return jsonify({"erro": f"Erro ao deletar livro no banco de dados: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)