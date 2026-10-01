import requests

from .config import ARQUIVO_PAGINA, CABECALHOS, TEMPO_LIMITE, URL_EVENTO


def baixar_pagina(url=URL_EVENTO, destino=ARQUIVO_PAGINA):
    resposta = requests.get(url, headers=CABECALHOS, timeout=TEMPO_LIMITE)
    resposta.raise_for_status()

    resposta.encoding = "utf-8"
    html = resposta.text

    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(html, encoding="utf-8")
    return html


def main():
    html = baixar_pagina()
    print(f"[002] Pagina baixada de {URL_EVENTO}")
    print(f"[002] {len(html)} caracteres gravados em {ARQUIVO_PAGINA}")


if __name__ == "__main__":
    main()
