# 📚 API de Doações de Livros

**Uma API REST feita em Flask para cadastrar, buscar, atualizar e remover livros.**  
Feita com 💜 por quem ama código limpo, validação decente e deploy no peito.

---

## 🔥 Tecnologias Usadas

- Python 3.11
- Flask
- Flask-CORS
- Marshmallow
- SQLite
- Gunicorn
- Render
- Dotenv

---

## 🧠 Estrutura da API

```bash
📦 api-livros-vnw
├── app/
│   ├── controllers/        # Funções da lógica principal
│   ├── routes/             # Endpoints organizados
│   ├── schemas/            # Validações com Marshmallow
│   ├── models/             # (Reservado pra evoluções futuras)
│   └── __init__.py         # create_app() mora aqui
├── database.db             # Banco SQLite (temporário)
├── .env                    # Variáveis de ambiente
├── requirements.txt        # Dependências do projeto
├── Procfile                # Comando de execução pro Render
├── wsgi.py                 # Ponto de entrada oficial
└── README.md               # Você está aqui 👋
```

---

## 🚀 Como rodar local

```bash
# Clone o projeto
git clone https://github.com/agleicesousa/api-livros-vnw.git
cd api-livros-vnw

# Crie e ative o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Rode a aplicação
python wsgi.py
```

---

## 🌍 Endpoints principais

| Método | Rota                         | Descrição                              |
|--------|------------------------------|----------------------------------------|
| GET    | `/`                          | Página de boas-vindas                  |
| GET    | `/livros`                    | Lista todos os livros cadastrados      |
| GET    | `/livros/<id>`              | Retorna um livro específico            |
| GET    | `/livros/buscar?q=termo`     | Busca por título, autor ou categoria   |
| POST   | `/livros`                    | Adiciona um ou vários livros           |
| PUT    | `/livros/<id>`              | Atualiza todos os dados de um livro    |
| PATCH  | `/livros/<id>`              | Atualiza parcialmente um livro         |
| DELETE | `/livros/<id>`              | Remove um livro                        |

---

## 🔐 Validação com Marshmallow

A API valida os seguintes campos obrigatórios ao cadastrar:

- `titulo`: string
- `categoria`: string
- `autor`: string
- `image_url`: URL válida

Se faltar algo, ela **não passa pano.** Vai devolver um erro 400 com mensagem clara!

---

## 🛠️ Melhorias futuras (roadmap)

- [ ] Trocar SQLite por PostgreSQL
- [ ] Documentação com Swagger/OpenAPI
- [ ] Autenticação com tokens (JWT ou OAuth)
- [ ] Integração com frontend em React ou Vue
- [ ] Testes automatizados com Pytest

---

## 👩‍💻 Desenvolvido por

**Agleice Sousa**
💼 [linkedin.com/in/agleice-sousa](https://linkedin.com/in/agleice-sousa)

---

## 🧾 Licença

MIT — Porque conhecimento foi feito pra circular.  
Use, modifique e compartilhe, mas dá aquele crédito bonito 👊
