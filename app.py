import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

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

# Rota para a página inicial
@app.route("/")
def index():
    return "<h2>Bem-vindo à API de Doações de Livros!</h2>"

# Rota para doação de livros
@app.route("/doar", methods=["POST"])
def doar():
    dados = request.get_json()

    # Verifica se todos os campos necessários estão presentes
    campos_obrigatorios = ["titulo", "categoria", "autor", "image_url"]
    if not all(campo in dados for campo in campos_obrigatorios):
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

    titulo = dados["titulo"]
    categoria = dados["categoria"]
    autor = dados["autor"]
    image_url = dados["image_url"]

    try:
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO LIVROS (titulo, categoria, autor, image_url) 
                VALUES (?, ?, ?, ?)
                """,
                (titulo, categoria, autor, image_url)
            )
            conn.commit()
    except sqlite3.Error as e:
        return jsonify({"erro": f"Erro ao inserir no banco de dados: {str(e)}"}), 500

    return jsonify({"mensagem": "Livro cadastrado com sucesso"}), 201

# Rota para listar todos os livros
@app.route("/livros", methods=["GET"])
def listar_livros():
    try:
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM LIVROS")
            livros = cursor.fetchall()

            # Transforma os resultados em uma lista de dicionários
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
        return jsonify({"erro": f"Erro ao buscar livros: {str(e)}"}), 500

# Rota para buscar um livro por ID
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
        return jsonify({"erro": f"Erro ao buscar livro: {str(e)}"}), 500

# Rota para deletar um livro por ID
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
        return jsonify({"erro": f"Erro ao deletar livro: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
