import re
from urllib.parse import unquote, urljoin

import requests

from .config import CABECALHOS, PASTA_DOWNLOAD, TEMPO_LIMITE, URL_BASE
from .tarefa_003_extrair_dados import extrair_palestrantes

RE_CARACTERE_INVALIDO = re.compile(r'[<>:"/\|?*]')


def nome_do_arquivo(url_imagem):
    nome = unquote(url_imagem.split("/")[-1].split("?")[0])
    return RE_CARACTERE_INVALIDO.sub("_", nome)


def baixar_imagem(url_imagem, pasta=PASTA_DOWNLOAD):
    pasta.mkdir(parents=True, exist_ok=True)

    url_completa = urljoin(URL_BASE, url_imagem)
    nome = nome_do_arquivo(url_imagem)
    destino = pasta / nome

    resposta = requests.get(url_completa, headers=CABECALHOS, timeout=TEMPO_LIMITE)
    resposta.raise_for_status()
    destino.write_bytes(resposta.content)
    return nome


def baixar_imagens(palestrantes=None, pasta=PASTA_DOWNLOAD):
    if palestrantes is None:
        palestrantes = extrair_palestrantes()

    for palestrante in palestrantes:
        url_imagem = palestrante.get("image_url", "")
        if not url_imagem:
            palestrante["image"] = ""
            print(f"[004] {palestrante['name']}: sem imagem no codigo-fonte")
            continue

        try:
            nome = baixar_imagem(url_imagem, pasta)
            palestrante["image"] = nome
            print(f"[004] {nome}")
        except requests.RequestException as erro:
            palestrante["image"] = ""
            print(f"[004] Falha ao baixar {url_imagem}: {erro}")

    return palestrantes


def main():
    palestrantes = baixar_imagens()
    baixadas = sum(1 for p in palestrantes if p.get("image"))
    print(f"\n[004] {baixadas}/{len(palestrantes)} imagens gravadas em {PASTA_DOWNLOAD}")


if __name__ == "__main__":
    main()
