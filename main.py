import csv
from tqdm import tqdm
from app.extractor import get_blog_posts
from app.analysis import analyze_posts
from app.helpers import setup_nltk

# Configurar e baixar pacotes do NLTK
setup_nltk()

def save_to_csv(results, filename="output.csv"):
    """
    Função para salvar os resultados da análise em um arquivo CSV.
    
    Args:
        results (list): Lista de dicionários contendo os dados analisados.
        filename (str): Nome do arquivo CSV.
    """
    keys = results[0].keys()  # Usar as chaves do primeiro resultado como cabeçalhos

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"Arquivo CSV salvo como {filename}")

if __name__ == "__main__":
    blog_url = "https://nfe.io/blog"
    print("Extraindo posts do blog...")
    posts = get_blog_posts(blog_url)
    
    if posts:
        print(f"Total de posts encontrados: {len(posts)}")
        print("Analisando posts...")

        # Mostrar barra de progresso com tqdm
        results = []
       
