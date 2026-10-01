import html as html_utils
import re

from .config import ARQUIVO_PAGINA

RE_SECAO = re.compile(
    r'<div[^>]*id="palestrantes-container"[^>]*>'
    r'(.*?)'
    r'<div[^>]*class="d-flex justify-content-center mt-4"',
    re.DOTALL,
)

RE_INICIO_BLOCO = re.compile(
    r'<div[^>]*class="[^"]*palestrante-item[^"]*"[^>]*id="Palestrante(\d+)"[^>]*>'
)

RE_IMAGEM = re.compile(r'<img\s+src="([^"]+)"\s+alt="Palestrante"')

RE_NOME = re.compile(r'<h4>\s*(.*?)\s*</h4>', re.DOTALL)

RE_TRABALHO = re.compile(r'<h6>\s*(.*?)\s*</h6>', re.DOTALL)

RE_EMAIL = re.compile(
    r'<p>\s*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})\s*</p>'
)

RE_NOME_CARTAO = re.compile(
    r'<p[^>]*class="card-text"[^>]*>\s*(.*?)\s*</p>', re.DOTALL
)


def _limpar(texto):
    if texto is None:
        return ""
    texto = re.sub(r'<[^>]+>', '', texto)
    texto = html_utils.unescape(texto)
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()


def separar_blocos(codigo_fonte):
    secao = RE_SECAO.search(codigo_fonte)
    if not secao:
        raise ValueError(
            "Secao de palestrantes nao encontrada no arquivo. "
            "Execute a tarefa 002 novamente."
        )

    conteudo = secao.group(1)
    inicios = [m.start() for m in RE_INICIO_BLOCO.finditer(conteudo)]

    blocos = []
    for posicao, inicio in enumerate(inicios):
        fim = inicios[posicao + 1] if posicao + 1 < len(inicios) else len(conteudo)
        blocos.append(conteudo[inicio:fim])
    return blocos


def extrair_de_bloco(bloco):
    imagem = RE_IMAGEM.search(bloco)
    nome = RE_NOME.search(bloco) or RE_NOME_CARTAO.search(bloco)
    trabalho = RE_TRABALHO.search(bloco)
    email = RE_EMAIL.search(bloco)

    return {
        "name": _limpar(nome.group(1)) if nome else "",
        "work": _limpar(trabalho.group(1)) if trabalho else "",
        "email": _limpar(email.group(1)) if email else "",
        "image_url": imagem.group(1).strip() if imagem else "",
    }


def extrair_palestrantes(origem=ARQUIVO_PAGINA):
    if not origem.exists():
        raise FileNotFoundError(
            f"Arquivo {origem} nao encontrado. Execute a tarefa 002 primeiro."
        )

    codigo_fonte = origem.read_text(encoding="utf-8")
    return [extrair_de_bloco(bloco) for bloco in separar_blocos(codigo_fonte)]


def main():
    palestrantes = extrair_palestrantes()
    print(f"[003] {len(palestrantes)} palestrantes encontrados em {ARQUIVO_PAGINA}\n")
    for posicao, palestrante in enumerate(palestrantes, start=1):
        print(f"  {posicao:02d}. {palestrante['name']}")
        print(f"      Local de trabalho: {palestrante['work']}")
        print(f"      Contato..........: {palestrante['email']}")
        print(f"      Imagem...........: {palestrante['image_url']}")


if __name__ == "__main__":
    main()
