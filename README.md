# Blog Content Analyzer

## Proposta de Valor
Esta solução tem o objetivo de ajudar as empresas a entender, documentar e organizar seu conteúdo dentro da estratégia de SEO. Além disso, a ferramenta pode ser usada para analisar concorrentes, determinando tópicos de interesse, intenção de posts, e em que estágio do funil de vendas o conteúdo se encontra.

## Visão Geral
O Blog Content Analyzer é um aplicativo que permite extrair posts de um blog WordPress e analisar seus conteúdos com base em tópicos, intenção e estágio do funil de vendas. Ele faz uso de bibliotecas de NLP (Natural Language Processing) para processar e interpretar o texto, auxiliando na otimização e estruturação de estratégias de conteúdo.

## Funcionalidades
- **Extração de Posts**: O aplicativo extrai os posts do blog via API do WordPress.
- **Limpeza de Conteúdo HTML**: O conteúdo HTML dos posts é processado e limpo para análise textual.
- **Análise de Tópicos**: Os principais tópicos de cada post são extraídos com base na relevância.
- **Determinação da Intenção**: Classifica a intenção de cada post como Informativa, Transacional ou Comercial.
- **Estágio do Funil**: Determina se o conteúdo está no topo (ToFu), meio (MoFu) ou fundo (BoFu) do funil de vendas.

## Requisitos
- **Python 3.8+**
- **Bibliotecas Necessárias**: As bibliotecas podem ser instaladas a partir do arquivo `requirements.txt`. O projeto faz uso de `requests`, `beautifulsoup4`, `nltk`, `tqdm` e outras dependências.

## Instalação e Uso

### 1. Clonar o Repositório
Primeiro, clone este repositório em sua máquina local:
```bash
git clone https://github.com/emanuellvieira/wp-blog-analyzer-v1.git
```

### 2. Instalar Dependências
Navegue até o diretório do projeto e instale as dependências:
```bash
cd blog-content-analyzer
pip install -r requirements.txt
```

### 3. Configuração do NLTK
Ao executar o script pela primeira vez, o NLTK irá baixar os pacotes necessários, como `stopwords` e `punkt`.

### 4. Executar o Aplicativo
Para iniciar a análise do blog, basta executar o arquivo `main.py`. O app vai extrair todos os posts do blog e gerar o arquivo `output.csv` com os resultados da análise.

```bash
python main.py
```

O arquivo CSV resultante incluirá os campos:
- **Título**: Título do post.
- **Top Tópicos**: Principais tópicos extraídos do conteúdo.
- **Intenção**: Intenção do conteúdo (Informativa, Transacional, Comercial).
- **Estágio do Funil**: Estágio do conteúdo no funil de vendas (ToFu, MoFu, BoFu).

### 5. Personalização com Arquivo de Configuração (Próxima Atualização)
Em breve, você poderá configurar a URL do blog, o contexto da sua empresa e o ICP (Ideal Customer Profile) em um arquivo de configuração para análises ainda mais personalizadas.

## Créditos
Este projeto foi desenvolvido por **Emanuell Vieira**, especialista em Martech, para ajudar empresas e profissionais a otimizar suas estratégias de conteúdo digital.  
Visite meu site: [emanuellvieira.com](https://emanuellvieira.com)
