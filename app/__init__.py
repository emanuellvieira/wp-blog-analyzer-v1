from app.extractor import get_all_blog_posts
from app.analysis import analyze_posts
from app.helpers import setup_nltk

# Configurar e baixar pacotes do NLTK
setup_nltk()

if __name__ == "__main__":
    blog_url = "https://seu-blog.com"
    
    # Utilize a função correta para pegar todos os posts
    posts = get_all_blog_posts(blog_url)
    
    if posts:
        results = analyze_posts(posts)

        for result in results:
            print(f"Título: {result['title']}")
            print(f"Tópicos Principais: {result['top_topics']}")
            print(f"Intenção: {result['intent']} (Indeterminado se não for possível)")
            print(f"Nível do Funil: {result['funnel_stage']} (Indeterminado se não for possível)")
            print("\n")
    else:
        print("Nenhum post encontrado.")
