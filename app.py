from flask import Flask, request, jsonify
from mysql.connector import Error
from sistema import Sistema

app = Flask(__name__)
sistema = Sistema()

@app.after_request
def aplicar_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return response

@app.route("/cadastrar", methods=["POST", "OPTIONS"])
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

    print(f"\n[PILOTO] Tentativa de cadastro recebida -> Nome: '{nome}' | E-mail: '{email}'")

    # Regra 1: Campos obrigatórios (Seção 2.4)
    if nome == "" or email == "" or telefone == "" or senha == "" or confirma_senha == "":
        msg = "Erro: todos os campos devem ser preenchidos."
        print(f"[BLOQUEADO] {msg}")
        return jsonify({"mensagem": msg}), 400

    if not termos:
        msg = "Erro: você precisa aceitar os termos de uso."
        print(f"[BLOQUEADO] {msg}")
        return jsonify({"mensagem": msg}), 400

    # Regra 2: Presença de '@' no e-mail (Seção 2.4)
    if "@" not in email:
        msg = "Erro: e-mail inválido."
        print(f"[BLOQUEADO] {msg}")
        return jsonify({"mensagem": msg}), 400

    # Regra 3: Confirmação de senha (Seção 2.4)
    if senha != confirma_senha:
        msg = "Erro: as senhas não são iguais."
        print(f"[BLOQUEADO] {msg}")
        return jsonify({"mensagem": msg}), 400

    try:
        # Regra 4: Bloqueio de e-mail duplicado (Seção 2.4 / UNIQUE no MySQL)
        if sistema.buscar_usuario(email) is not None:
            msg = "Erro: e-mail já cadastrado."
            print(f"[BLOQUEADO] {msg}")
            return jsonify({"mensagem": msg}), 409

        # Regra 5: Persistência física no MySQL (Seção 3.2)
        id_gerado = sistema.cadastrar_usuario(nome, email, telefone, senha)
        msg = f"Cadastro realizado com sucesso! (ID gerado: {id_gerado})"
        print(f"[SUCESSO] {msg}")
        return jsonify({"mensagem": msg, "id_usuario": id_gerado}), 201

    except Error as err:
        msg = f"Erro de banco de dados: {err}"
        print(f"[ERRO SQL] {msg}")
        return jsonify({"mensagem": msg}), 500

if __name__ == "__main__":
    print("=== Servidor Projeto Âncora rodando em http://127.0.0.1:5000 ===")
    app.run(host="127.0.0.1", port=5000, debug=False)