import csv

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

def generate_report(results):
    """
    Gera um relatório com base na análise dos posts.
    
    Args:
        results (list): Lista de dicionários contendo os dados analisados.

    Returns:
        dict: Um dicionário com insights globais sobre os posts.
    """
    total_posts = len(results)
    funnel_distribution = {}
    top_intents = {}
    top_topics = {}

    # Contabilizar a distribuição dos posts por estágio do funil e intenções
    for result in results:
        funnel_stage = result.get('funnel_stage', 'Indeterminado')
        intent = result.get('intent', 'Indeterminado')
        topics = result.get('top_topics', [])

        # Atualizar a contagem do estágio do funil
        if funnel_stage in funnel_distribution:
            funnel_distribution[funnel_stage] += 1
        else:
            funnel_distribution[funnel_stage] = 1

        # Atualizar a contagem da intenção
        if intent in top_intents:
            top_intents[intent] += 1
        else:
            top_intents[intent] = 1

        # Atualizar a contagem dos tópicos
        for topic in topics:
            if topic in top_topics:
                top_topics[topic] += 1
            else:
                top_topics[topic] = 1

    # Gerar um relatório com os insights globais
    report = {
        "total_posts": total_posts,
        "funnel_distribution": funnel_distribution,
        "top_intents": top_intents,
        "top_topics": sorted(top_topics.items(), key=lambda x: x[1], reverse=True)
    }

    return report


def save_report(report, filename="relatorio_global.csv"):
    """
    Salva o relatório global em um arquivo CSV.
    """
    if not report:
        print("Nenhum dado disponível para salvar.")
        return

    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Cabeçalhos
            writer.writerow(['Total de Posts', 'Distribuição do Funil', 'Principais Intenções', 'Tópicos Principais', 'Sugestões'])

            # Conteúdo do relatório
            total_posts = report.get('total_posts', 'N/A')
            funnel_distribution = report.get('funnel_distribution', 'N/A')
            top_intents = report.get('top_intents', 'N/A')
            top_topics = report.get('top_topics', 'N/A')
            suggestions = report.get('suggestions', [])

            writer.writerow([total_posts, funnel_distribution, top_intents, top_topics, suggestions])

            # Verifica se existem sugestões
            if suggestions:
                for suggestion in suggestions:
                    writer.writerow([suggestion])
            else:
                writer.writerow(["Sem sugestões disponíveis"])

    except Exception as e:
        print(f"Erro ao salvar o relatório: {e}")
