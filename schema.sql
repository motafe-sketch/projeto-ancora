CREATE DATABASE IF NOT EXISTS projeto_ancora;
USE projeto_ancora;

CREATE TABLE usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    telefone VARCHAR(20),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE contato_apoio (
    id_contato INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    nome VARCHAR(150) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    vinculo VARCHAR(50),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

INSERT INTO usuario (nome, email, senha, telefone)
VALUES ('Paciente Alfa', 'alfa@ancora.app', 'senha_hash_123', '11999999999');

INSERT INTO contato_apoio (id_usuario, nome, telefone, vinculo)
VALUES (1, 'Dr. Roberto', '11888888888', 'Terapeuta');