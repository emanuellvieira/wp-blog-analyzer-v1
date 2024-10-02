from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
from nltk.tokenize import word_tokenize, sent_tokenize

def extract_topics_tfidf(posts):
    """
    Função para extrair os principais tópicos de cada post usando TF-IDF.

    Args:
        posts (list): Lista de conteúdos dos posts.

    Returns:
        dict: Dicionário com o título do post como chave e os principais tópicos como valor.
    """
    corpus = [post['content'] for post in posts]
    titles = [post['title'] for post in posts]

    vectorizer = TfidfVectorizer(stop_words='english', max_features=10)
    tfidf_matrix = vectorizer.fit_transform(corpus)

    feature_names = vectorizer.get_feature_names_out()
    topics = {}

    for idx, title in enumerate(titles):
        tfidf_scores = tfidf_matrix[idx].T.todense()
        top_indices = tfidf_scores.argsort().flatten().tolist()[::-1]
        top_terms = [feature_names[i] for i in top_indices[:5]]
        topics[title] = top_terms

    return topics

def classify_intent(content):
    """
    Função para classificar a intenção do post.

    Args:
        content (str): O conteúdo textual do post.

    Returns:
        str: A intenção do post (informativa, transacional, navegacional).
    """
    if "comprar" in content or "preço" in content:
        return "Transacional"
    elif "como" in content or "dicas" in content:
        return "Informativa"
    else:
        return "Navegacional"

def classify_funnel_stage(content):
    """
    Função para classificar o estágio do funil de vendas ao qual o post se destina.

    Args:
        content (str): O conteúdo textual do post.

    Returns:
        str: O nível do funil (ToFu, MoFu, BoFu).
    """
    if "introdutório" in content or "o que é" in content:
        return "Topo do Funil (ToFu)"
    elif "solução" in content or "como resolver" in content:
        return "Meio do Funil (MoFu)"
    elif "testemunho" in content or "depoimento" in content:
        return "Fundo do Funil (BoFu)"
    else:
        return "Indeterminado"

def analyze_posts(posts):
    """
    Função para realizar uma análise completa dos posts.

    Args:
        posts (list): Lista de dicionários contendo os dados dos posts.

    Returns:
        list: Lista de resultados de análise contendo tópicos, intenção, e estágio do funil.
    """
    analysis_results = []
    topics = extract_topics_tfidf(posts)

    for post in posts:
        title = post['title']
        content = post['content']
        intent = classify_intent(content)
        funnel_stage = classify_funnel_stage(content)
        top_topics = topics[title]

        result = {
            "title": title,
            "top_topics": top_topics,
            "intent": intent,
            "funnel_stage": funnel_stage
        }
        analysis_results.append(result)

    return analysis_results
