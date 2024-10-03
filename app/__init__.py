import json
from app.extractor import get_all_blog_posts
from app.analysis import analyze_posts
from app.helpers import setup_nltk

# Função para carregar o arquivo config.json
def load_config(config_file="config.json"):
    """
    Função para carregar o arquivo de configuração config.json.
    """
    try:
        with open(config_file, 'r', encoding='utf-8') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print(f"Arquivo {config_file} não encontrado.")
        return {}
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar {config_file}: {e}")
        return {}

# Configurar e baixar pacotes do NLTK
setup_nltk()

if __name__ == "__main__":
    # Carregar configurações do arquivo config.json
    config = load_config()
    blog_url = config.get("blog_url", "https://nfe.io/blog")
    company_context = config.get("company_context", {})
    icp = config.get("ideal_customer_profile", {})

    print("Extraindo posts do blog...")
    posts = get_all_blog_posts(blog_url, config)  # Passar o config para limitar posts, se necessário

    if posts:
        print(f"Total de posts encontrados: {len(posts)}")
        print("Analisando posts...")

        # Analisar os posts
        results = analyze_posts(posts, company_context, icp)

        # Exibir os resultados
        for result in results:
            print(f"Título: {result['title']}")
            print(f"Tópicos Principais: {result['top_topics']}")
            print(f"Intenção: {result['intent']}")
            print(f"Nível do Funil: {result['funnel_stage']}")
            print("\n")
    else:
        print("Nenhum post encontrado.")
