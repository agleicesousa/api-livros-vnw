from flask import request, jsonify
import sqlite3
from marshmallow import ValidationError
from app.schemas import LivroSchema

schema = LivroSchema()

def criar_livros():
    try:
        dados = request.get_json()

        if not dados:
            return jsonify({"erro": "Nenhum dado enviado"}), 400

        livros = [dados] if not isinstance(dados, list) else dados

        livros_validados = []
        for livro in livros:
            try:
                livro_validado = schema.load(livro)
                livros_validados.append(livro_validado)
            except ValidationError as err:
                return jsonify({"erro": "Dados inválidos", "detalhes": err.messages}), 400

        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            for livro in livros_validados:
                cursor.execute(
                    "INSERT INTO LIVROS (titulo, categoria, autor, image_url) VALUES (?, ?, ?, ?)",
                    (livro["titulo"], livro["categoria"], livro["autor"], livro["image_url"])
                )
            conn.commit()

        return jsonify({"mensagem": f"{len(livros_validados)} livro(s) cadastrado(s) com sucesso"}), 201

    except Exception as e:
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500


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


def atualizar_livro(id):
    try:
        dados = request.get_json()
        dados_validados = schema.load(dados)

        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE LIVROS
                SET titulo = ?, categoria = ?, autor = ?, image_url = ?
                WHERE id = ?
                """,
                (
                    dados_validados["titulo"],
                    dados_validados["categoria"],
                    dados_validados["autor"],
                    dados_validados["image_url"],
                    id
                )
            )
            conn.commit()

            if cursor.rowcount > 0:
                return jsonify({"mensagem": "Livro atualizado com sucesso"}), 200
            else:
                return jsonify({"erro": "Livro não encontrado"}), 404
    except ValidationError as err:
        return jsonify({"erro": "Dados inválidos", "detalhes": err.messages}), 400
    except sqlite3.Error as e:
        return jsonify({"erro": f"Erro ao atualizar livro no banco de dados: {str(e)}"}), 500


def atualizar_parcial_livro(id):
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Nenhum dado enviado para atualização"}), 400

    try:
        dados_validados = schema.load(dados, partial=True)

        campos_para_atualizar = ", ".join([f"{campo} = ?" for campo in dados_validados])
        valores = list(dados_validados.values()) + [id]

        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE LIVROS SET {campos_para_atualizar} WHERE id = ?", valores
            )
            conn.commit()

            if cursor.rowcount > 0:
                return jsonify({"mensagem": "Livro atualizado com sucesso"}), 200
            else:
                return jsonify({"erro": "Livro não encontrado"}), 404
    except ValidationError as err:
        return jsonify({"erro": "Dados inválidos", "detalhes": err.messages}), 400
    except sqlite3.Error as e:
        return jsonify({"erro": f"Erro ao atualizar livro: {str(e)}"}), 500


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
