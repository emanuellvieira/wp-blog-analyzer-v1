import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_page(url, params):
    """
    Função para fazer a requisição de uma página específica de posts.
    """
    try:
        response = requests.get(url, params=params, verify=False, timeout=10)
        response.raise_for_status()  # Levanta um erro se a requisição não for bem-sucedida
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar página {params['page']}: {e}")
        return []

def get_blog_posts(base_url, num_posts=100):
    """
    Função para buscar posts de um blog WordPress via API, com requisições paralelas.

    Args:
        base_url (str): URL base do blog WordPress.
        num_posts (int): Número de posts a serem buscados no total.

    Returns:
        list: Lista de dicionários contendo título e conteúdo dos posts.
    """
    url = f"{base_url}/wp-json/wp/v2/posts"
    posts = []
    total_posts = 0
    per_page = 20  # Definindo 20 posts por página para reduzir o número de requisições

    print("Iniciando extração dos posts...")

    # Calcular o número de páginas necessárias
    total_pages = (num_posts // per_page) + 1

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []

        for page in range(1, total_pages + 1):
            params = {"per_page": per_page, "page": page}
            futures.append(executor.submit(fetch_page, url, params))

        for future in as_completed(futures):
            result = future.result()
            if result:
                posts.extend(result)
                total_posts += len(result)
                print(f"Total de posts até agora: {total_posts}")

            # Limitar ao número máximo de posts desejados
            if total_posts >= num_posts:
                break

    print(f"Extração concluída. Total de posts extraídos: {total_posts}")
    return [{"title": post['title']['rendered'], "content": post['content']['rendered']} for post in posts[:num_posts]]
