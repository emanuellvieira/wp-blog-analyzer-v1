def generate_seo_suggestions(posts_analysis):
    """
    Gera sugestões de SEO baseadas na análise dos posts.
    """
    suggestions = []

    # Sugestão 1: Tópicos com pouca cobertura
    low_coverage_topics = [topic for topic in posts_analysis['top_topics'] if posts_analysis['top_topics'].count(topic) == 1]
    if low_coverage_topics:
        suggestions.append(f"Aumente a cobertura de tópicos como: {', '.join(low_coverage_topics)}")

    # Sugestão 2: Tópicos saturados
    saturated_topics = [topic for topic in posts_analysis['top_topics'] if posts_analysis['top_topics'].count(topic) > 3]
    if saturated_topics:
        suggestions.append(f"Evite repetir demasiadamente tópicos como: {', '.join(saturated_topics)}")

    # Sugestão 3: Palavras-chave
    if 'vender' in posts_analysis['intent']:
        suggestions.append("Considere focar em palavras-chave relacionadas a vendas, como 'aumentar vendas', 'estratégias de vendas', etc.")

    return suggestions if suggestions else ["Sem sugestões disponíveis"]
