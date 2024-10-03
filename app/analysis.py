from transformers import pipeline
from bertopic import BERTopic
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(stopwords.words('portuguese'))

def clean_text(text):
    """
    Limpa o texto removendo stopwords e pontuação.
    """
    if not text:
        return ''
    words = word_tokenize(text.lower())
    return ' '.join([word for word in words if word.isalpha() and word not in stop_words])

def split_text(text, max_length=512):
    """
    Divide o texto em partes menores para caber no limite do modelo.
    """
    if not text:
        return []
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

def determine_intent(post_content, company_context, icp):
    """
    Determina a intenção de um post com base no conteúdo e no contexto da empresa.
    Processa textos longos em partes menores.
    """
    classifier = pipeline('zero-shot-classification', model='prajjwal1/bert-tiny')

    labels = [
        "informar", "educar", "vender", "engajar",
        f"resolver desafios de {icp.get('sector', 'indústria')}",
        f"ajudar empresas com {icp.get('key_challenges', 'desafios')}"
    ]

    # Dividir o conteúdo em partes menores para não exceder o limite do modelo
    text_segments = split_text(post_content)

    # Verifica se o conteúdo do post é válido
    if not text_segments:
        return "Indeterminado"

    aggregated_results = {}
    try:
        for segment in text_segments:
            result = classifier(segment, candidate_labels=labels)
            top_label = result['labels'][0]
            if top_label in aggregated_results:
                aggregated_results[top_label] += 1
            else:
                aggregated_results[top_label] = 1

        # Retorna o rótulo mais frequente
        return max(aggregated_results, key=aggregated_results.get)

    except Exception as e:
        print(f"Erro ao determinar a intenção: {e}")
        return "Indeterminado"


    # Dividir o conteúdo em partes menores
    text_segments = split_text(post_content)

    if not text_segments:
        return "Indeterminado"

    aggregated_results = {}
    try:
        for segment in text_segments:
            result = classifier(segment, candidate_labels=labels)
            top_label = result['labels'][0]
            aggregated_results[top_label] = aggregated_results.get(top_label, 0) + 1

        # Retorna o rótulo mais frequente
        return max(aggregated_results, key=aggregated_results.get)
    except Exception as e:
        print(f"Erro ao determinar a intenção: {e}")
        return "Indeterminado"

def determine_funnel_stage(post_content):
    """
    Determina o estágio do funil de vendas de um post com base no conteúdo.
    Processa textos longos em partes menores.
    """
    classifier = pipeline('zero-shot-classification', model='prajjwal1/bert-tiny')

    labels = ["topo do funil", "meio do funil", "fundo do funil"]

    # Dividir o conteúdo em partes menores
    text_segments = split_text(post_content)

    if not text_segments:
        return "Indeterminado"

    aggregated_results = {}
    try:
        for segment in text_segments:
            result = classifier(segment, candidate_labels=labels)
            top_label = result['labels'][0]
            aggregated_results[top_label] = aggregated_results.get(top_label, 0) + 1

        # Retorna o estágio mais frequente
        return max(aggregated_results, key=aggregated_results.get)
    except Exception as e:
        print(f"Erro ao determinar o estágio do funil: {e}")
        return "Indeterminado"

def extract_topics(posts):
    """
    Extrai tópicos dos posts usando TF-IDF para identificar as principais palavras-chave.
    Adiciona debug para verificar se os textos estão sendo processados corretamente.
    """
    cleaned_posts = []

    # Garantir que o conteúdo seja extraído corretamente
    for post in posts:
        if isinstance(post, dict):
            content = post.get('content', {}).get('rendered', '')
            if isinstance(content, str):  # Verifica se o conteúdo é uma string
                cleaned_post = clean_text(content)
                if cleaned_post:
                    cleaned_posts.append(cleaned_post)
                    print(f"Texto Limpo: {cleaned_post}")  # Debug: Exibir o conteúdo limpo
                else:
                    print(f"Post sem conteúdo válido após a limpeza: {post.get('title', 'Sem título')}")
            else:
                print(f"Erro: Conteúdo do post não é uma string. Ignorando o post: {post.get('title', 'Sem título')}")
        else:
            print(f"Erro: O post não é um dicionário. Ignorando: {post}")

    # Verificar se temos posts limpos
    if not cleaned_posts:
        print("Nenhum post contém conteúdo válido após a limpeza.")
        return ["Nenhum tópico encontrado"]

    try:
        # Aplicar TF-IDF para extração de tópicos
        vectorizer = TfidfVectorizer(max_features=10)
        tfidf_matrix = vectorizer.fit_transform(cleaned_posts)
        feature_names = vectorizer.get_feature_names_out()

        topics = []
        for row in tfidf_matrix:
            topic_words = [feature_names[i] for i in row.nonzero()[1]]
            topics.append(topic_words)
            print(f"Tópicos extraídos: {topic_words}")  # Debug: Exibir os tópicos extraídos

        return topics if topics else ["Nenhum tópico encontrado"]

    except Exception as e:
        print(f"Erro ao extrair tópicos: {e}")
        return ["Erro ao extrair tópicos"]

# No analyze_posts, vamos garantir que não estamos pulando posts com conteúdo que pode ser limpo
def analyze_posts(posts, company_context, icp):
    """
    Analisa os posts determinando os tópicos principais, intenção e estágio do funil.
    """
    for post in posts:
        if not isinstance(post, dict) or 'title' not in post or 'content' not in post:
            print(f"Post com estrutura inesperada: {post}. Pulando.")
            continue

        title = post.get('title', 'Sem título')
        content = clean_text(post.get('content', ''))

        # Verifica se o conteúdo está vazio após a limpeza
        if not content:
            print(f"Post '{title}' sem conteúdo válido. Pulando.")
            continue

        try:
            topics = extract_topics([post])
        except Exception as e:
            print(f"Erro ao extrair tópicos: {e}")
            topics = ["Indeterminado"]

        try:
            intent = determine_intent(content, company_context, icp)
        except Exception as e:
            print(f"Erro ao determinar a intenção: {e}")
            intent = "Indeterminado"

        try:
            funnel_stage = determine_funnel_stage(content)
        except Exception as e:
            print(f"Erro ao determinar o estágio do funil: {e}")
            funnel_stage = "Indeterminado"

        yield {
            'title': title,
            'content': content,
            'top_topics': topics,
            'intent': intent,
            'funnel_stage': funnel_stage
        }


def generate_report(results):
    """
    Gera um relatório com base na análise dos posts.
    """
    total_posts = len(results)
    funnel_distribution = {}
    top_intents = {}
    top_topics = {}
    suggestions = []

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

        # Adicionando sugestões de melhoria com base na análise
        if funnel_stage == 'Indeterminado' or intent == 'Indeterminado':
            suggestions.append(f"Post '{result['title']}' não tem uma intenção ou estágio do funil claro.")

    report = {
        "total_posts": total_posts,
        "funnel_distribution": funnel_distribution,
        "top_intents": top_intents,
        "top_topics": sorted(top_topics.items(), key=lambda x: x[1], reverse=True),
        "suggestions": suggestions or ["Nenhuma sugestão no momento."]
    }

    return report
