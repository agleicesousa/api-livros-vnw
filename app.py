import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
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

# CREATE: Rota para doação de livros
@app.route("/livros", methods=["POST"])
def criar_livros():
    dados = request.get_json()

    # Verifica se foram enviados dados
    if not dados:
        return jsonify({"erro": "Nenhum dado enviado"}), 400

    # Converte para lista se for um único livro
    if not isinstance(dados, list):
        dados = [dados]

    # Verifica se cada livro tem os campos obrigatórios
    campos_obrigatorios = ["titulo", "categoria", "autor", "image_url"]
    for livro in dados:
        if not all(campo in livro for campo in campos_obrigatorios):
            return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

    try:
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            for livro in dados:
                cursor.execute(
                    """
                    INSERT INTO LIVROS (titulo, categoria, autor, image_url) 
                    VALUES (?, ?, ?, ?)
                    """,
                    (livro["titulo"], livro["categoria"], livro["autor"], livro["image_url"])
                )
            conn.commit()
        return jsonify({"mensagem": "Livro(s) cadastrado(s) com sucesso"}), 201
    except sqlite3.Error as e:
        return jsonify({"erro": f"Erro ao inserir no banco de dados: {str(e)}"}), 500

# READ: Rota para listar todos os livros
@app.route("/livros", methods=["GET"])
def listar_livros():
    try:
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM LIVROS")
            livros = cursor.fetchall()

            livros_formatados = [
                {
                    "id": livro[0],
                    "titulo": livro[1],
                    "categoria": livro[2],
                    "autor": livro[3],
                    "image_url": livro[4]
                }
                for livro in livros
            ]
            return jsonify(livros_formatados), 200
    except sqlite3.Error as e:
        return jsonify({"erro": f"Erro ao buscar livros no banco de dados: {str(e)}"}), 500

# READ: Rota para buscar um livro por ID
@app.route("/livros/<int:id>", methods=["GET"])
def buscar_livro(id):
    try:
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM LIVROS WHERE id = ?", (id,))
            livro = cursor.fetchone()

            if livro:
                livro_formatado = {
                    "id": livro[0],
                    "titulo": livro[1],
                    "categoria": livro[2],
                    "autor": livro[3],
                    "image_url": livro[4]
                }
                return jsonify(livro_formatado), 200
            else:
                return jsonify({"erro": "Livro não encontrado"}), 404
    except sqlite3.Error as e:
        return jsonify({"erro": f"Erro ao buscar livro no banco de dados: {str(e)}"}), 500

# Rota para buscar livros pelo título, categoria ou autor
@app.route("/livros/buscar", methods=["GET"])
def buscar_livro_por_titulo():
    palavra_chave = request.args.get("q", "")

    if not palavra_chave:
        return jsonify({"erro": "É necessário fornecer uma palavra-chave para a busca"}), 400

    try:
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM LIVROS 
                WHERE titulo LIKE ? OR categoria LIKE ? OR autor LIKE ?
                """,
                (f"%{palavra_chave}%", f"%{palavra_chave}%", f"%{palavra_chave}%")
            )
            livros = cursor.fetchall()

            if livros:
                livros_formatados = [
                    {
                        "id": livro[0],
                        "titulo": livro[1],
                        "categoria": livro[2],
                        "autor": livro[3],
                        "image_url": livro[4]
                    }
                    for livro in livros
                ]
                return jsonify(livros_formatados), 200
            else:
                return jsonify({"mensagem": "Nenhum livro encontrado"}), 404
    except sqlite3.Error as e:
        return jsonify({"erro": f"Erro ao buscar livros no banco de dados: {str(e)}"}), 500

# UPDATE: Rota para atualizar um livro por ID
@app.route("/livros/<int:id>", methods=["PUT"])
def atualizar_livro(id):
    dados = request.get_json()

    campos_obrigatorios = ["titulo", "categoria", "autor", "image_url"]
    if not all(campo in dados for campo in campos_obrigatorios):
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

    try:
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE LIVROS
                SET titulo = ?, categoria = ?, autor = ?, image_url = ?
                WHERE id = ?
                """,
                (dados["titulo"], dados["categoria"], dados["autor"], dados["image_url"], id)
            )
            conn.commit()

            if cursor.rowcount > 0:
                return jsonify({"mensagem": "Livro atualizado com sucesso"}), 200
            else:
                return jsonify({"erro": "Livro não encontrado"}), 404
    except sqlite3.Error as e:
        return jsonify({"erro": f"Erro ao atualizar livro no banco de dados: {str(e)}"}), 500
    

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