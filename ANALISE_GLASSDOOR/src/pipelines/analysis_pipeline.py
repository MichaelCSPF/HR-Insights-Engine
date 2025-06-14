# Importa as configurações já processadas do módulo config
from src import config 
from src.components.database_handler import DatabaseHandler
from src.components.text_processor import TextProcessor

def run_analysis_pipeline():
    """Orquestra todo o processo de ETL e análise."""
    print("--- INICIANDO PIPELINE DE ANÁLISE DE SENTIMENTO ---")

    # 1. Inicializar Componentes (usando as configs importadas)
    db_handler = DatabaseHandler(server=config.DB_SERVER, database=config.DB_DATABASE)
    text_processor = TextProcessor(
        sentiment_model=config.SENTIMENT_MODEL,
        sentiment_model_fallback=config.SENTIMENT_MODEL_FALLBACK
    )
    
    try:
        # 2. Conectar e Executar
        db_handler.connect()

        with open(config.QUERIES["select_reviews"], 'r') as f:
            query = f.read()
        
        raw_df = db_handler.fetch_data(query)

        if raw_df.empty:
            print("Nenhum dado retornado. Encerrando.")
            return

        processed_df = text_processor.run_full_analysis(raw_df, config.TEXT_COLUMNS)

        db_handler.write_dataframe(processed_df, config.RESULTS_TABLE_NAME, if_exists='replace')

    except Exception as e:
        print(f"!!! ERRO CRÍTICO NA PIPELINE: {e} !!!")
    finally:
        db_handler.close()
        print("--- PIPELINE CONCLUÍDA ---")