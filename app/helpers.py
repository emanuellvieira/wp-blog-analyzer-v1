import nltk
import ssl

def setup_nltk():
    """
    Função para configurar e baixar os pacotes do NLTK.
    """
    ssl._create_default_https_context = ssl._create_unverified_context
    nltk.data.path.append('/Users/emanuellvieira/nltk_data')

    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('maxent_ne_chunker')
    nltk.download('words')
