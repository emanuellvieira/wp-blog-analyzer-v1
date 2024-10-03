import requests
from bs4 import BeautifulSoup

def clean_html(raw_html):
    """
    Remove as tags HTML do conteúdo bruto e retorna apenas o texto.
    """
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text()

def get_all_blog_posts(blog_url, config):
    """
    Extrai todos os posts de um blog WordPress usando a API, com a opção de limitar o número de posts.
    """
    page = 1
    all_posts = []
    max_posts = config.get("max_posts", None)  # Pega o número máximo de posts no config
    limit_posts = config.get("limit_posts", False)  # Define se deve limitar o número de posts

    while True:
        try:
            # Faz a requisição para a API do WordPress
            response = requests.get(f"{blog_url}/wp-json/wp/v2/posts?per_page=100&page={page}", verify=False)
            response.raise_for_status()  # Garante que a requisição foi bem-sucedida

            posts = response.json()

            if not posts:
                break  # Encerra o loop se não houver mais posts

            # Limpa o conteúdo HTML dos posts
            for post in posts:
                content_raw = post.get('content', {}).get('rendered', '')
                cleaned_content = clean_html(content_raw)
                all_posts.append({
                    'title': post.get('title', {}).get('rendered', 'Sem título'),
                    'content': cleaned_content
                })

            page += 1

            # Verifica se o limite de posts foi alcançado
            if limit_posts and max_posts and len(all_posts) >= max_posts:
                all_posts = all_posts[:max_posts]
                break

        except requests.exceptions.RequestException as e:
            print(f"Erro ao extrair os posts: {e}")
            break

    return all_posts
