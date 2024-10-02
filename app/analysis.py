import nltk
from nltk.corpus import stopwords
from collections import Counter
from app.cleaning import clean_text

# Certifique-se de ter baixado o NLTK stopwords
nltk.download('stopwords')

def extract_topics(posts):
    """
    Extrai os principais tópicos de cada post usando uma abordagem de contagem de palavras.
    Remove stopwords para focar nos termos relevantes.
    """
    all_words = []
    stop_words = set(stopwords.words('portuguese'))

    for post in posts:
        words = nltk.word_tokenize(post['content'])
        words_cleaned = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
        all_words.extend(words_cleaned)

    # Contar as palavras mais comuns
    word_freq = Counter(all_words)
    top_words = [word for word, freq in word_freq.most_common(10)]

    return top_words

def determine_intent(post):
    """
    Determina a intenção do post com base no conteúdo analisado.
    Pode ser informativa, comercial, transacional, ou indeterminada.
    """
    content = post['content'].lower()
    if any(word in content for word in ['comprar', 'adquirir', 'assinar', 'emitir']):
        return 'Transacional'
    elif any(word in content for word in ['benefícios', 'vantagens', 'custo', 'preço', 'serviços']):
        return 'Comercial'
    elif any(word in content for word in ['como', 'dicas', 'informações', 'guia', 'tutorial']):
        return 'Informativa'
    else:
        return 'Indeterminado'

def determine_funnel_stage(post):
    """
    Determina o estágio do funil de vendas com base no conteúdo do post.
    Pode ser topo do funil (ToFu), meio do funil (MoFu) ou fundo do funil (BoFu).
    """
    content = post['content'].lower()
    if any(word in content for word in ['como', 'dicas', 'entenda', 'informações', 'guia']):
        return 'Topo do Funil (ToFu)'
    elif any(word in content for word in ['melhorar', 'otimizar', 'eficiência', 'soluções']):
        return 'Meio do Funil (MoFu)'
    elif any(word in content for word in ['comprar', 'adquirir', 'assinar', 'contratar']):
        return 'Fundo do Funil (BoFu)'
    else:
        return 'Indeterminado'

def analyze_posts(posts):
    """
    Faz a análise dos posts e retorna os tópicos principais, intenção e estágio do funil.
    """
    analyzed_results = []

    for post in posts:
        top_topics = extract_topics([post])  # extrair tópicos de cada post individualmente
        intent = determine_intent(post)
        funnel_stage = determine_funnel_stage(post)

        analyzed_results.append({
            'title': post['title'],
            'top_topics': top_topics,
            'intent': intent,
            'funnel_stage': funnel_stage
        })

    return analyzed_results
