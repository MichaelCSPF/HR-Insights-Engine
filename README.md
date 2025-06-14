# Analisador de Sentimento de Avaliações de Funcionários
Este projeto é um pipeline de dados e NLP (Processamento de Linguagem Natural) projetado para automatizar a análise de avaliações de funcionários. 
Seu principal objetivo é extrair avaliações textuais (originalmente do Glassdoor), processar os comentários para entender o sentimento e os temas recorrentes, e carregar os resultados enriquecidos de volta ao banco de dados para análise de BI ou investigações de RH.

# Isto é um Case real, de uso comprovado.
## Utilizado para identificar possíveis causas de desligamento e melhoria continua do setor.

# Qual o Propósito?
Empresas recebem centenas de comentários de funcionários em plataformas como o Glassdoor. 
Ler e categorizar manualmente esses dados é ineficiente e propenso a vieses. 
Desenvolvi essa ferramenta pensando nisso, pois boa parte da minha carreira foi no RH - ADM DE PESSOAL.

Este pipeline resolve esse problema ao:
Buscar no glassdor os dados brutos, como prós e contras, notas, média de avaliação, conselhos e feedback dos ex funcionários.
Transformar dados não estruturados (comentários em texto livre) em insights estruturados.
Identificar automaticamente os principais pontos de dor e os pontos positivos da cultura da empresa, analisando os tópicos e o sentimento dos comentários negativos e positivos(NLP).
Monitorar o feedback dos ex-funcionários de forma qualitativa.
Fornecer ao RH e uma base de dados para tomar decisões.

# Principais Funcionalidades
Extração de Dados: Via Web Scrapping, faço um download completo de todos dados do site glassdor, quem conhece entende sua funcionalidade de feedback pra melhoria continua da empresa.
Conecta-se a um banco de dados SQL Server para buscar avaliações brutas com base em critérios definidos (ex: pré fixei em 3.5 as notas, pra identificar nossos piores casos).
Pré-processamento de Texto: Limpeza robusta de texto usando NLTK, incluindo remoção de pontuação, stopwords e conversão para minúsculas.
Análise de Sentimento: Utilizo modelos da Hugging Face para classificar o sentimento de cada comentário (título, prós, contras) como positivo, negativo ou neutro(NPS).
Identificação de Palavras-Chave: Extrai as palavras mais frequentes nos comentários para identificar rapidamente os assuntos mais mencionados.

Carregamento de Resultados: Cria uma nova tabela no banco de dados com os dados originais enriquecidos com as análises de sentimento e texto processado, pronta para ser consumida.


## Tecnologias e Arquitetura
O projeto é construído em Python e segue uma arquitetura modular e orientada a objetos para garantir escalabilidade e manutenção.
Linguagem: Python
Bibliotecas Principais:
selenium.
beatfulsoup 4.
pandas.
pyodbc.
transformers e torch.
nltk.
python-dotenv.


## Arquitetura:
components/: Módulos desacoplados para tarefas específicas (ex: database_handler.py, text_processor.py).
pipelines/: Orquestradores que definem o fluxo de execução.
config/: Configurações não sensíveis do projeto.
Estrutura do Projeto
ANALISADOR_SENTIMENTO_GLASSDOOR/
├── config/
│   └── config.ini
├── data/
│   └── queries/
│       └── select_reviews.sql
├── reports/
│   └── .gitkeep
├── src/
│   ├── components/
│   │   ├── database_handler.py
│   │   └── text_processor.py
│   ├── pipelines/
│   │   └── analysis_pipeline.py
│   ├── config.py
│   └── main.py
├── tests/
│   └── .gitkeep
├── .env
├── .gitignore
├── requirements.txt
└── README.md


Como Configurar e Instalar

Siga os passos abaixo para executar o projeto localmente.

Clone o repositório:
git clone https://github.com/MichaelCSPF/HR-Insights-Engine

cd analisa-glassdor

Crie um ambiente virtual e ative-o:
python -m venv venv
WINDOWS/POWERSHELL: venv\Scripts\activate  

Instale as dependências:
pip install -r requirements.txt


Configure as variáveis de ambiente:
Crie um arquivo chamado .env na raiz do projeto e preencha com suas credenciais do banco de dados.
## .env
DB_SERVER="NOME_DO_SEU_SERVIDOR"
DB_DATABASE="NOME_DO_SEU_BANCO"


Revise o arquivo config/config.ini e ajuste os nomes de tabelas, modelos de NLP ou caminhos, se necessário.

Como Executar
Após a configuração, execute o pipeline principal com o seguinte comando a partir da raiz do projeto:
python src/main.py
