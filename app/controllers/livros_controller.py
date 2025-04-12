from flask import request, jsonify
import sqlite3

def criar_livros():
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"erro": "Nenhum dado enviado"}), 400

        livros = [dados] if not isinstance(dados, list) else dados
        campos = ["titulo", "categoria", "autor", "image_url"]

        for livro in livros:
            if not all(campo in livro for campo in campos):
                return jsonify({"erro": f"Faltam campos obrigatórios: {campos}"}), 400

        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            for livro in livros:
                cursor.execute(
                    "INSERT INTO LIVROS (titulo, categoria, autor, image_url) VALUES (?, ?, ?, ?)",
                    (livro["titulo"], livro["categoria"], livro["autor"], livro["image_url"])
                )
            conn.commit()

        return jsonify({"mensagem": f"{len(livros)} livro(s) cadastrado(s) com sucesso"}), 201

    except Exception as e:
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500
