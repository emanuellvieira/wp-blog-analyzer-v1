import requests
from app.cleaning import clean_html, clean_text

def get_all_blog_posts(blog_url):
    """
    Obtém todos os posts de um blog WordPress usando requisições paginadas.
    Retorna uma lista de posts com o título e o conteúdo limpos.
    """
    all_posts = []
    page = 1
    per_page = 100  # Quantidade máxima de posts por página

    while True:
        try:
            # Fazer a requisição para a API do WordPress
            response = requests.get(f"{blog_url}/wp-json/wp/v2/posts?per_page={per_page}&page={page}", verify=False)
            response.raise_for_status()
            posts = response.json()

            # Se não houver mais posts, interromper o loop
            if not posts:
                break

            # Limpar e adicionar os posts extraídos
            for post in posts:
                title = post.get('title', {}).get('rendered', '')
                content = post.get('content', {}).get('rendered', '')
                clean_content = clean_text(clean_html(content))
                all_posts.append({'title': title, 'content': clean_content})

            page += 1

        except requests.exceptions.RequestException as e:
            print(f"Erro ao extrair os posts: {e}")
            break

    return all_posts
