from bs4 import BeautifulSoup

def clean_html_content(html_content):
    """
    Remove tags HTML e retorna o texto limpo.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    cleaned_text = soup.get_text(separator=" ")  # Extrai o texto e separa por espaço
    return cleaned_text.strip()
