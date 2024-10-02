import csv
from tqdm import tqdm
from app.extractor import get_all_blog_posts
from app.analysis import analyze_posts
from app.helpers import setup_nltk
import json

# Configurar e baixar pacotes do NLTK
setup_nltk()

# Função para salvar o resultado em CSV
def save_to_csv(results, filename="output.csv"):
    """
    Função para salvar os resultados da análise em um arquivo CSV.
    
    Args:
        results (list): Lista de dicionários contendo os dados analisados.
        filename (str): Nome do arquivo CSV.
    """
    if results:
        keys = results[0].keys()  # Usar as chaves do primeiro resultado como cabeçalhos

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            writer.writerows(results)
        
        print(f"Arquivo CSV salvo como {filename}")
    else:
        print("Nenhum dado disponível para salvar.")

# Carregar a URL do blog do config.json
def load_config():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    return config['blog_url']

if __name__ == "__main__":
    # Carregar URL do blog a partir do config.json
    blog_url = load_config()
    print(f"Extraindo posts do blog da URL: {blog_url}")
    
    # Extrair todos os posts do blog
    posts = get_all_blog_posts(blog_url)
    
    if posts:
        print(f"Total de posts encontrados: {len(posts)}")
        print("Analisando posts...")

        # Mostrar barra de progresso com tqdm
        results = []
        for result in tqdm(analyze_posts(posts)):
            results.append(result)

        # Verificar se há resultados de análise
        if results:
            # Exibir os resultados no terminal
            for result in results:
                print(f"Título: {result['title']}")
                print(f"Tópicos Principais: {result['top_topics']}")
                print(f"Intenção: {result['intent']}")
                print(f"Nível do Funil: {result['funnel_stage']}")
                print("\n")

            # Salvar os resultados no CSV
            save_to_csv(results)
        else:
            print("Nenhuma análise realizada.")
    else:
        print("Nenhum post encontrado.")
