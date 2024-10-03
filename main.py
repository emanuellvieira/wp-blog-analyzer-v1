import json
from tqdm import tqdm
from app.extractor import get_all_blog_posts
from app.analysis import analyze_posts
from app.helpers import setup_nltk
from app.output import save_to_csv, save_report

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

# Função para gerar o relatório global
def generate_report(results):
    """
    Gera um relatório com base na análise dos posts.
    """
    total_posts = len(results)
    funnel_distribution = {}
    top_intents = {}
    top_topics = {}

    for result in results:
        funnel_stage = result.get('funnel_stage', 'Indeterminado')
        intent = result.get('intent', 'Indeterminado')
        topics = result.get('top_topics', [])

        if funnel_stage in funnel_distribution:
            funnel_distribution[funnel_stage] += 1
        else:
            funnel_distribution[funnel_stage] = 1

        if intent in top_intents:
            top_intents[intent] += 1
        else:
            top_intents[intent] = 1

        for topic in topics:
            if topic in top_topics:
                top_topics[topic] += 1
            else:
                top_topics[topic] = 1

    report = {
        "total_posts": total_posts,
        "funnel_distribution": funnel_distribution,
        "top_intents": top_intents,
        "top_topics": sorted(top_topics.items(), key=lambda x: x[1], reverse=True)
    }

    return report

# Configurar e baixar pacotes do NLTK
setup_nltk()

if __name__ == "__main__":
    # Carregar configurações do arquivo config.json
    config = load_config()
    blog_url = config.get("blog_url")
    company_context = config.get("company_context")
    icp = config.get("ideal_customer_profile")

    if not blog_url or not company_context or not icp:
        print("Configuração inválida. Verifique o arquivo config.json.")
    else:
        print("Extraindo posts do blog...")
        # Passando o config para a função get_all_blog_posts
        posts = get_all_blog_posts(blog_url, config)

        if posts:
            print(f"Total de posts encontrados: {len(posts)}")
            print("Analisando posts...")

            # Mostrar barra de progresso com tqdm
            results = list(tqdm(analyze_posts(posts, company_context, icp), total=len(posts)))

            # Salvar os resultados no CSV
            save_to_csv(results)

            # Criar e salvar o relatório global
            report = generate_report(results)
            save_report(report)
        else:
            print("Nenhum post encontrado.")
