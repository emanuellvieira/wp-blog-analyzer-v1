import nltk
from nltk.corpus import stopwords
from collections import Counter

# Funções auxiliares importadas
from app.cleaning import clean_html_content

nltk.download('stopwords')

# Stopwords em português
stop_words = set(stopwords.words('portuguese'))

def tokenize_and_remove_stopwords(text):
    tokens = nltk.word_tokenize(text)
    tokens = [word.lower() for word in tokens if word.isalnum()]
    tokens = [word for word in tokens if word not in stop_words]
    return tokens

def extract_topics(posts):
    """
    Extrai os principais tópicos dos posts processados.
    """
    cleaned_posts = [clean_html_content(post['content']) for post in posts]
    processed_posts = [tokenize_and_remove_stopwords(post) for post in cleaned_posts]
    top_topics = [Counter(post).most_common(10) for post in processed_posts]
    return [[topic for topic, freq in topics] for topics in top_topics]

def classify_intent(post_content):
    """
    Classifica a intenção do post com base no conteúdo.
    """
    informativa_keywords = ['como', 'guia', 'dicas', 'informações', 'entenda', 'aprenda']
    transacional_keywords = ['compre', 'adquira', 'oferta', 'produto', 'promoção']
    comercial_keywords = ['avaliação', 'produto', 'preço', 'serviço', 'comparativo']

    post_tokens = tokenize_and_remove_stopwords(post_content)

    if any(keyword in post_tokens for keyword in transacional_keywords):
        return 'Transacional'
    elif any(keyword in post_tokens for keyword in comercial_keywords):
        return 'Comercial'
    elif any(keyword in post_tokens for keyword in informativa_keywords):
        return 'Informativa'
    else:
        return 'Indeterminado'

def classify_funnel_stage(post_content):
    """
    Classifica o estágio do funil de vendas com base no conteúdo.
    """
    topo_keywords = ['o que é', 'dicas', 'introdução', 'guia', 'começar']
    meio_keywords = ['como', 'benefícios', 'vantagens', 'processo', 'melhor']
    fundo_keywords = ['compre', 'adquira', 'serviço', 'produto', 'contrate']

    post_tokens = tokenize_and_remove_stopwords(post_content)

    if any(keyword in post_tokens for keyword in fundo_keywords):
        return 'Fundo do Funil (BoFu)'
    elif any(keyword in post_tokens for keyword in meio_keywords):
        return 'Meio do Funil (MoFu)'
    elif any(keyword in post_tokens for keyword in topo_keywords):
        return 'Topo do Funil (ToFu)'
    else:
        return 'Indeterminado'

def analyze_posts(posts):
    """
    Analisa os posts para extrair tópicos, classificar intenção e estágio do funil.
    """
    results = []
    for post in posts:
        post_content = clean_html_content(post['content'])
        top_topics = extract_topics([post])[0]  # Extrair tópicos para o post atual
        intent = classify_intent(post_content)  # Classificar a intenção
        funnel_stage = classify_funnel_stage(post_content)  # Classificar estágio do funil

        results.append({
            "title": post['title'],
            "top_topics": top_topics,
            "intent": intent,
            "funnel_stage": funnel_stage
        })
    return results
