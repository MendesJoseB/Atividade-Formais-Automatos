import sys

from tarefas.config import ARQUIVO_BANCO, ARQUIVO_PAGINA, PASTA_DOWNLOAD
from tarefas.tarefa_002_baixar_pagina import baixar_pagina
from tarefas.tarefa_003_extrair_dados import extrair_palestrantes
from tarefas.tarefa_004_baixar_imagens import baixar_imagens
from tarefas.tarefa_005_criar_banco import criar_banco
from tarefas.tarefa_006_registrar_dados import (
    listar_palestrantes,
    registrar_palestrantes,
)


def titulo(texto):
    print()
    print("=" * 70)
    print(texto)
    print("=" * 70)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    titulo("TAREFA 002 - Baixando o codigo-fonte da pagina")
    html = baixar_pagina()
    print(f"{len(html)} caracteres gravados em {ARQUIVO_PAGINA}")

    titulo("TAREFA 003 - Extraindo os dados com Expressoes Regulares")
    palestrantes = extrair_palestrantes()
    print(f"{len(palestrantes)} palestrantes encontrados\n")
    for posicao, palestrante in enumerate(palestrantes, start=1):
        print(f"  {posicao:02d}. {palestrante['name']}")
        print(f"      trabalho: {palestrante['work']}")
        print(f"      contato.: {palestrante['email']}")
        print(f"      imagem..: {palestrante['image_url']}")

    titulo("TAREFA 004 - Baixando as imagens dos palestrantes")
    baixar_imagens(palestrantes)
    print(f"\nImagens gravadas em {PASTA_DOWNLOAD}")

    titulo("TAREFA 005 - Criando o banco event.db e a tabela speaker")
    criar_banco()
    print(f"Banco pronto em {ARQUIVO_BANCO}")

    titulo("TAREFA 006 - Registrando os palestrantes na tabela speaker")
    total = registrar_palestrantes(palestrantes)
    print(f"{total} registros gravados\n")
    for registro in listar_palestrantes():
        identificador, nome, trabalho, email, imagem = registro
        print(f"  {identificador:02d} | {nome} | {email} | {imagem}")

    print("\nProcesso concluido.")


if __name__ == "__main__":
    main()
