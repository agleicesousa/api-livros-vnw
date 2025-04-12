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
