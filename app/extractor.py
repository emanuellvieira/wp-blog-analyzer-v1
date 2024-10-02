import requests
from bs4 import BeautifulSoup

def clean_html(raw_html):
    """
    Remove as tags HTML do conteúdo bruto e retorna apenas o texto.
    """
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text()

def get_all_blog_posts(blog_url):
    """
    Faz uma requisição para a API do WordPress para obter todos os posts do blog.
    Limpa o HTML dos posts e retorna uma lista com títulos e conteúdos limpos.
    """
    all_posts = []
    page = 1

    while True:
        try:
            response = requests.get(f"{blog_url}/wp-json/wp/v2/posts?per_page=100&page={page}", verify=False)
            response.raise_for_status()
            posts = response.json()

            # Se a resposta não contiver posts, saímos do loop
            if not posts:
                break

            for post in posts:
                title = post.get('title', {}).get('rendered', '')
                content = post.get('content', {}).get('rendered', '')
                clean_content = clean_html(content)
                all_posts.append({'title': title, 'content': clean_content})

            page += 1  # Avança para a próxima página

        except requests.exceptions.RequestException as e:
            print(f"Erro ao extrair os posts: {e}")
            break

    return all_posts
