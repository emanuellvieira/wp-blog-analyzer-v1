from bs4 import BeautifulSoup
import re

def clean_html(raw_html):
    """
    Remove tags HTML e retorna apenas o texto limpo.
    """
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text()

def clean_text(text):
    """
    Limpa o texto removendo caracteres especiais, múltiplos espaços e novas linhas.
    """
    text = re.sub(r'\s+', ' ', text)  # Remove múltiplos espaços
    text = text.strip()  # Remove espaços em branco no início e no fim
    return text
