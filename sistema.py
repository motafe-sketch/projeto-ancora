import mysql.connector

class Sistema:
    def __init__(self):
        self.db_config = {
            "host": "127.0.0.1",
            "user": "root",
            "password": "",
            "database": "projeto_ancora"
        }

    def conectar(self):
        return mysql.connector.connect(**self.db_config)

    def buscar_usuario(self, email):
        conn = self.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuario WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        return usuario

    def cadastrar_usuario(self, nome, email, telefone, senha):
        conn = self.conectar()
        cursor = conn.cursor()
        sql = "INSERT INTO usuario (nome, email, senha, telefone) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (nome, email, senha, telefone))
        conn.commit()
        novo_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return novo_id

    def cadastrar_contato_apoio(self, id_usuario, nome, telefone, vinculo):
        conn = self.conectar()
        cursor = conn.cursor()
        sql = "INSERT INTO contato_apoio (id_usuario, nome, telefone, vinculo) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (id_usuario, nome, telefone, vinculo))
        conn.commit()
        novo_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return novo_id