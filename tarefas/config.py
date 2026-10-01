from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

URL_EVENTO = "https://eventos.ifgoiano.edu.br/integra2026/"
URL_BASE = "https://eventos.ifgoiano.edu.br"
ARQUIVO_PAGINA = RAIZ / "pagina.txt"

PASTA_DOWNLOAD = RAIZ / "download"

ARQUIVO_BANCO = RAIZ / "event.db"

CABECALHOS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}

TEMPO_LIMITE = 60
