from flask import request, jsonify
import sqlite3

def criar_livros():
    try:
        dados = request.get_json()

        # Validação dos dados
        if not dados:
            return jsonify({"erro": "Nenhum dado enviado"}), 400

        # Converte para lista se for um único livro
        livros = [dados] if not isinstance(dados, list) else dados

        # Campos obrigatórios
        campos_obrigatorios = ["titulo", "categoria", "autor", "image_url"]
        for livro in livros:
            if not all(campo in livro for campo in campos_obrigatorios):
                return jsonify({"erro": f"Faltam campos obrigatórios: {campos_obrigatorios}"}), 400

        # Insere no banco de dados (SQLite exemplo)
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            for livro in livros:
                cursor.execute(
                    "INSERT INTO LIVROS (titulo, categoria, autor, image_url) VALUES (?, ?, ?, ?)",
                    (livro["titulo"], livro["categoria"], livro["autor"], livro["image_url"])
                )
            conn.commit()

        return jsonify({
            "mensagem": f"{len(livros)} livro(s) cadastrado(s) com sucesso",
        }), 201

    except Exception as e:
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500