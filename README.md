# Projeto Âncora — Protótipo Funcional (PIME)

Aplicativo móvel/web de apoio imediato na prevenção de recaídas em dependência química, desenvolvido no **Projeto Integrador Multidisciplinar Extensionista (PIME)** do curso de **Análise e Desenvolvimento de Sistemas (2º Semestre)** do **Centro Universitário Belas Artes de São Paulo (2026)**[cite: 62].

## Integrantes
* Felipe de Souza Mota[cite: 62]
* Maria Beatriz B. de Araujo[cite: 62]
* Thales Matos Queiroz[cite: 62]

## Arquitetura do Protótipo
* **Front-end:** HTML5, CSS3 e JavaScript (`index.html`, `styles.css`) com máscara de telefone e envio assíncrono (`fetch`)[cite: 59, 64, 68].
* **Back-end:** Python 3 com Flask e Flask-CORS (`app.py`), responsável pelas validações de negócio (campos obrigatórios, formato de e-mail, confirmação de senha e bloqueio de duplicidade)[cite: 57, 70, 72].
* **Banco de Dados:** MySQL via XAMPP (`schema.sql`), estruturado com as tabelas `usuario` e `contato_apoio`[cite: 72, 74].

## Como Executar Localmente
1. Inicie os módulos **Apache** e **MySQL** no XAMPP[cite: 54, 72].
2. Acesse `http://localhost/phpmyadmin` e execute o conteúdo de `schema.sql` na aba **SQL**[cite: 54, 74].
3. No terminal, dentro da pasta do projeto, instale as dependências e inicie a API:
   ```bash
   pip3 install flask flask-cors mysql-connector-python
   python3 app.py