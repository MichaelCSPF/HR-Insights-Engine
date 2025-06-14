from pipelines.scraping_pipeline import run_scraping_pipeline
from pipelines.analysis_pipeline import run_analysis_pipeline
import time

if __name__ == "__main__":
    print("=====================================================")
    print("= INICIANDO PROCESSO COMPLETO: SCRAPING E ANÁLISE   =")
    print("=====================================================")
    
    # --- ETAPA 1: Coleta de Dados Brutos ---
    run_scraping_pipeline()
    
    print("\nPausa de 5 segundos entre as pipelines...")
    time.sleep(5)
    
    # --- ETAPA 2: Análise e Processamento de NLP ---
    run_analysis_pipeline()

    print("\n=====================================================")
    print("= PROCESSO COMPLETO FINALIZADO                    =")
    print("=====================================================")