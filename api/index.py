from flask import Flask, request, jsonify
from mysql.connector import Error
from .sistema import Sistema

app = Flask(__name__)
sistema = Sistema()

@app.after_request
def aplicar_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

@app.route("/api/usuarios", methods=["GET", "OPTIONS"])
def listar_usuarios():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    try:
        usuarios = sistema.listar_usuarios()
        return jsonify({"usuarios": usuarios}), 200
    except Error as err:
        return jsonify({"mensagem": f"Erro de banco de dados: {err}"}), 500

@app.route("/api/cadastrar", methods=["POST", "OPTIONS"])
def cadastrar():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    dados = request.get_json() or {}
    nome = dados.get("nome", "").strip()
    email = dados.get("email", "").strip()
    telefone = dados.get("telefone", "").strip()
    senha = dados.get("senha", "")
    confirma_senha = dados.get("confirma_senha", "")
    termos = dados.get("termos", False)

    # Regra 1: Campos obrigatórios (Seção 2.4)
    if nome == "" or email == "" or telefone == "" or senha == "" or confirma_senha == "":
        return jsonify({"mensagem": "Erro: todos os campos devem ser preenchidos."}), 400

    if not termos:
        return jsonify({"mensagem": "Erro: você precisa aceitar os termos de uso."}), 400

    # Regra 2: Presença de '@' no e-mail (Seção 2.4)
    if "@" not in email:
        return jsonify({"mensagem": "Erro: e-mail inválido."}), 400

    # Regra 3: Confirmação de senha (Seção 2.4)
    if senha != confirma_senha:
        return jsonify({"mensagem": "Erro: as senhas não são iguais."}), 400

    try:
        # Regra 4: Bloqueio de e-mail duplicado (Seção 2.4 / UNIQUE no MySQL)
        if sistema.buscar_usuario(email) is not None:
            return jsonify({"mensagem": "Erro: e-mail já cadastrado."}), 409

        # Regra 5: Persistência física no MySQL (Seção 3.2)
        id_gerado = sistema.cadastrar_usuario(nome, email, telefone, senha)
        msg = f"Cadastro realizado com sucesso! (ID gerado: {id_gerado})"
        return jsonify({"mensagem": msg, "id_usuario": id_gerado}), 201

    except Error as err:
        return jsonify({"mensagem": f"Erro de banco de dados: {err}"}), 500