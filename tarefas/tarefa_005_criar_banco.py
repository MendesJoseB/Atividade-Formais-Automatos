import sqlite3

from .config import ARQUIVO_BANCO

SQL_CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS speaker (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    name  VARCHAR(255) NOT NULL,
    work  VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    image VARCHAR(255) NOT NULL
);
"""


def conectar(banco=ARQUIVO_BANCO):
    banco.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(banco)


def criar_banco(banco=ARQUIVO_BANCO):
    with conectar(banco) as conexao:
        conexao.execute(SQL_CRIAR_TABELA)
    return banco


def main():
    banco = criar_banco()
    print(f"[005] Banco pronto em {banco} com a tabela speaker")


if __name__ == "__main__":
    main()
