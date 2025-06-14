import os
import configparser
from dotenv import load_dotenv

# Carrega variáveis do .env para o ambiente do sistema
load_dotenv()

# --- CARREGAR SEGREDOS DO AMBIENTE ---
DB_SERVER = os.getenv('DB_SERVER')
DB_DATABASE = os.getenv('DB_DATABASE')

# --- CARREGAR CONFIGURAÇÕES DO ARQUIVO .INI ---
_parser = configparser.ConfigParser()
_parser.read('config/config.ini') # Caminho relativo à raiz do projeto

# -- Paths --
QUERY_DIR = _parser.get('Paths', 'query_dir')
QUERIES = {
    "select_reviews": QUERY_DIR + 'select_reviews.sql'
}

# -- Database --
RESULTS_TABLE_NAME = _parser.get('Database', 'results_table_name')

# -- NLP --
SENTIMENT_MODEL = _parser.get('NLP', 'sentiment_model')
SENTIMENT_MODEL_FALLBACK = _parser.get('NLP', 'sentiment_model_fallback')
TEXT_COLUMNS = [col.strip() for col in _parser.get('NLP', 'text_columns').split(',')]

print("Configurações carregadas.")