from .config import ARQUIVO_BANCO
from .tarefa_003_extrair_dados import extrair_palestrantes
from .tarefa_004_baixar_imagens import baixar_imagens
from .tarefa_005_criar_banco import conectar, criar_banco

SQL_INSERIR = """
INSERT INTO speaker (name, work, email, image) VALUES (?, ?, ?, ?);
"""


def limpar_tabela(conexao):
    conexao.execute("DELETE FROM speaker;")
    conexao.execute("DELETE FROM sqlite_sequence WHERE name = 'speaker';")


def registrar_palestrantes(palestrantes, banco=ARQUIVO_BANCO, substituir=True):
    criar_banco(banco)

    linhas = [
        (
            palestrante.get("name", ""),
            palestrante.get("work", ""),
            palestrante.get("email", ""),
            palestrante.get("image", ""),
        )
        for palestrante in palestrantes
    ]

    with conectar(banco) as conexao:
        if substituir:
            limpar_tabela(conexao)
        conexao.executemany(SQL_INSERIR, linhas)

    return len(linhas)


def listar_palestrantes(banco=ARQUIVO_BANCO):
    with conectar(banco) as conexao:
        cursor = conexao.execute(
            "SELECT id, name, work, email, image FROM speaker ORDER BY id;"
        )
        return cursor.fetchall()


def main():
    palestrantes = baixar_imagens(extrair_palestrantes())
    total = registrar_palestrantes(palestrantes)
    print(f"\n[006] {total} palestrantes registrados em {ARQUIVO_BANCO}\n")
    for registro in listar_palestrantes():
        print(f"  {registro[0]:02d} | {registro[1]} | {registro[3]} | {registro[4]}")


if __name__ == "__main__":
    main()
