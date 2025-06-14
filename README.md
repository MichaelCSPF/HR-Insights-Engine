README.md para o seu Projeto no GitHub
Aqui está um modelo de README.md completo e profissional, pronto para você copiar e colar no seu repositório. Ele está escrito em Markdown.
Analisador de Sentimento de Avaliações de Funcionários
Este projeto é um pipeline de dados e NLP (Processamento de Linguagem Natural) projetado para automatizar a análise de avaliações de funcionários. Seu principal objetivo é extrair avaliações textuais (originalmente de fontes como o Glassdoor) de um banco de dados, processar os comentários para entender o sentimento e os temas recorrentes, e carregar os resultados enriquecidos de volta ao banco de dados para análise de BI ou investigações de RH.
![alt text](https://img.shields.io/badge/License-MIT-yellow.svg)
Qual o Propósito? (Usabilidade)
Empresas recebem centenas de comentários de funcionários em plataformas como o Glassdoor. Ler e categorizar manualmente esses dados é ineficiente e propenso a vieses. Este pipeline resolve esse problema ao:
Transformar dados não estruturados (comentários em texto livre) em insights estruturados e acionáveis.
Identificar automaticamente os principais pontos de dor e os pontos positivos da cultura da empresa, analisando os tópicos e o sentimento dos comentários negativos e positivos.
Monitorar o moral dos funcionários de forma quantitativa ao longo do tempo.
Fornecer ao RH e à gestão uma base de dados para tomar decisões estratégicas baseadas em evidências.
Principais Funcionalidades
Extração de Dados: Conecta-se a um banco de dados SQL Server para buscar avaliações brutas com base em critérios definidos (ex: notas baixas).
Pré-processamento de Texto: Limpeza robusta de texto usando NLTK, incluindo remoção de pontuação, stopwords e conversão para minúsculas.
Análise de Sentimento: Utiliza modelos de ponta da Hugging Face (Transformers) para classificar o sentimento de cada comentário (título, prós, contras) como positivo, negativo ou neutro.
Identificação de Palavras-Chave: Extrai as palavras mais frequentes nos comentários para identificar rapidamente os assuntos mais mencionados.
Carregamento de Resultados: Cria uma nova tabela no banco de dados com os dados originais enriquecidos com as análises de sentimento e texto processado, pronta para ser consumida.
Tecnologias e Arquitetura
O projeto é construído em Python 3 e segue uma arquitetura modular e orientada a objetos para garantir escalabilidade e manutenção.
Linguagem: Python
Bibliotecas Principais:
pandas para manipulação de dados.
pyodbc para conexão com SQL Server.
transformers e torch para NLP (Hugging Face).
nltk para pré-processamento de texto.
python-dotenv para gerenciamento de segredos.
Arquitetura:
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
Use code with caution.
Como Configurar e Instalar
Siga os passos abaixo para executar o projeto localmente.
Clone o repositório:
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
Use code with caution.
Bash
Crie um ambiente virtual e ative-o:
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
Use code with caution.
Bash
Instale as dependências:
pip install -r requirements.txt
Use code with caution.
Bash
Configure as variáveis de ambiente:
Crie um arquivo chamado .env na raiz do projeto e preencha com suas credenciais do banco de dados.
# .env
DB_SERVER="NOME_DO_SEU_SERVIDOR"
DB_DATABASE="NOME_DO_SEU_BANCO"
Use code with caution.
Ini
Verifique as configurações do projeto:
Revise o arquivo config/config.ini e ajuste os nomes de tabelas, modelos de NLP ou caminhos, se necessário.
Como Executar
Após a configuração, execute o pipeline principal com o seguinte comando a partir da raiz do projeto:
python src/main.py
Use code with caution.
Bash
O script irá conectar ao banco, processar os dados e salvar os resultados em uma nova tabela, conforme definido no config.ini.
Fluxo do Pipeline
Extração (Extract): A pipeline lê a query SQL de data/queries/ e busca os dados no banco de dados.
Transformação (Transform): O TextProcessor é acionado para limpar os textos e aplicar a análise de sentimento em cada avaliação.
Carga (Load): O DatabaseHandler recebe o DataFrame enriquecido e o salva em uma nova tabela no mesmo banco de dados, substituindo-a se já existir.