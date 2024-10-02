
# Blog Analyzer - Ferramenta de Análise de Posts de Blog

Este projeto realiza a extração e análise de posts de blogs WordPress, gerando insights úteis para estratégias de marketing de conteúdo. Ele classifica os posts de acordo com a intenção (informativa, transacional ou comercial) e o estágio do funil de vendas (Topo, Meio ou Fundo de Funil). Além disso, os tópicos principais são extraídos para facilitar a compreensão do conteúdo abordado.

## Funcionalidades

- **Extração de posts**: Obtém posts de blogs WordPress via API.
- **Análise de intenção**: Determina a intenção do post (informativa, transacional, comercial).
- **Classificação de funil de vendas**: Identifica o estágio do funil de vendas (ToFu, MoFu, BoFu).
- **Geração de CSV**: Exporta os resultados em um arquivo CSV para análise posterior.

## Pré-requisitos

- **Python 3.x**
- **Virtualenv** (opcional, mas recomendado para isolar dependências)
- **NLTK** (Natural Language Toolkit) para análise de texto
- **Bibliotecas Python**:
  - `requests`
  - `beautifulsoup4`
  - `nltk`
  - `tqdm`

## Instalação

1. **Clonar o repositório**:
   ```bash
   git clone https://github.com/emanuellvieira/wp-blog-analyzer-v1
   cd wp-blog-analyzer-v1
   ```

2. **Configurar o ambiente virtual (opcional, mas recomendado)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate  # Windows
   ```

3. **Instalar as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar NLTK**:
   Execute o seguinte comando para baixar os pacotes necessários do NLTK:
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger'); nltk.download('maxent_ne_chunker'); nltk.download('words')"
   ```

## Configuração

1. **Arquivo de Configuração (Futuro)**: Em versões futuras, um arquivo de configuração permitirá inserir a URL do blog, contexto da empresa, e o ICP (Ideal Customer Profile) para análises mais robustas e personalizadas.

## Uso

1. **Executar a aplicação**:
   No terminal, execute o seguinte comando para rodar o aplicativo:
   ```bash
   python main.py
   ```

2. **Resultado**:
   - O script irá realizar a extração dos posts de um blog WordPress via API, fazer a análise e, por fim, salvar os resultados em um arquivo CSV (`output.csv`).
   - O CSV incluirá o título do post, tópicos principais, intenção do conteúdo, e o estágio do funil de vendas.

3. **Customização da URL do Blog**:
   - O blog que você deseja analisar deve ser configurado na variável `blog_url` dentro do arquivo `main.py`.
   ```python
   blog_url = "https://seu-blog.com"
   ```

## Output

Os resultados serão salvos em um arquivo `output.csv` com a seguinte estrutura:

- **title**: Título do post.
- **top_topics**: Tópicos principais do conteúdo.
- **intent**: Intenção do post (informativa, transacional, comercial).
- **funnel_stage**: Estágio do funil de vendas (ToFu, MoFu, BoFu).

## Futuras Implementações

- **Análise personalizada**: Adicionar um arquivo de configuração para incluir a URL do blog, contexto da empresa e do ICP.
- **Modelo de interpretação de texto**: Melhorar a análise de intenção e estágio do funil com modelos de NLP mais avançados.
- **Relatórios detalhados**: Geração de relatórios e gráficos para visualização de insights.

## Contribuição

Fique à vontade para abrir issues e pull requests para melhorias no projeto. Toda contribuição é bem-vinda!

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
