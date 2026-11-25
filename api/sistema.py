import os
from datetime import timezone, timedelta
import mysql.connector

class Sistema:
    def __init__(self):
        self.db_config = {
            "host": os.environ.get("DB_HOST", "127.0.0.1"),
            "port": int(os.environ.get("DB_PORT", 3306)),
            "user": os.environ.get("DB_USER", "root"),
            "password": os.environ.get("DB_PASSWORD", ""),
            "database": os.environ.get("DB_NAME", "projeto_ancora")
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

    def listar_usuarios(self):
        conn = self.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id_usuario, nome, email, telefone, data_cadastro "
            "FROM usuario ORDER BY id_usuario DESC"
        )
        usuarios = cursor.fetchall()
        fuso_brt = timezone(timedelta(hours=-3))
        for u in usuarios:
            if u.get("data_cadastro"):
                dt_utc = u["data_cadastro"].replace(tzinfo=timezone.utc)
                u["data_cadastro"] = dt_utc.astimezone(fuso_brt).strftime("%d/%m/%Y %H:%M")
        cursor.close()
        conn.close()
        return usuarios

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
