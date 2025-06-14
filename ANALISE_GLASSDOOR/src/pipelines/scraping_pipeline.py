import math
import threading
import time
from tqdm import tqdm
from src.components.web_scraper import GlassdoorScraper
from src.components.database_handler import DatabaseHandler
from src.config import DB_SERVER, DB_DATABASE # Supondo que você refatorou para src/config.py

# Carregando configs específicas do Scraper
from src.config import SCRAPING_CONFIG, SELECTORS_CONFIG, DB_CONFIG

COLUMN_NAMES = [
    'DATA_AVALIACAO', 'TITULO', 'CARGO_LOCAL', 'NOTA_GERAL_TEXT', 
    'PROS', 'CONS', 'CONSELHOS_DIRETORIA', 'RECOMENDA',
    'APROVA_CEO', 'PERSPECTIVA_EMPRESA', 'DATA_EXTRACAO'
]

# Variáveis globais para a pipeline de scraping
all_results = []
results_lock = threading.Lock()

def _thread_worker(scraper: GlassdoorScraper, page_range: list, thread_id: int):
    """Função alvo para cada thread."""
    global all_results, results_lock
    thread_results = scraper.scrape_page_range(page_range, thread_id)
    if thread_results:
        with results_lock:
            all_results.extend(thread_results)

def run_scraping_pipeline():
    """Orquestra o processo completo de web scraping e armazenamento de dados."""
    print("--- INICIANDO PIPELINE DE WEB SCRAPING ---")
    start_time = time.time()
    
    # 1. Montar Configuração
    scraper_config = {**SCRAPING_CONFIG, "selectors": SELECTORS_CONFIG}

    # 2. Inicializar Componentes
    scraper = GlassdoorScraper(scraper_config)
    db_handler = DatabaseHandler(server=DB_SERVER, database=DB_DATABASE)

    # 3. Preparar e Iniciar Threads
    total_pages = int(scraper_config['total_pages'])
    num_threads = int(scraper_config['num_threads'])
    pages_per_thread = math.ceil(total_pages / num_threads)
    threads = []
    
    for i in range(num_threads):
        start_page = i * pages_per_thread + 1
        end_page = min((i + 1) * pages_per_thread, total_pages)
        if start_page > total_pages: break
        
        page_range_for_thread = list(range(start_page, end_page + 1))
        thread = threading.Thread(
            target=_thread_worker,
            args=(scraper, page_range_for_thread, i + 1)
        )
        threads.append(thread)
        thread.start()

    # 4. Aguardar Conclusão com Barra de Progresso
    for thread in tqdm(threads, desc="Executando Threads de Scraping"):
        thread.join()

    print(f"\nScraping concluído. Total de {len(all_results)} avaliações coletadas.")

    # 5. Salvar no Banco de Dados
    if not all_results:
        print("Nenhum dado coletado. Encerrando pipeline.")
        return

    try:
        db_handler.connect()
        # Aqui, usamos uma função aprimorada do db_handler (que você irá adicionar)
        db_handler.create_table_if_not_exists(
            schema_name=DB_CONFIG['db_schema'],
            table_name=DB_CONFIG['raw_data_table_name'],
            column_names=COLUMN_NAMES
        )
        db_handler.bulk_insert_data(
            schema_name=DB_CONFIG['db_schema'],
            table_name=DB_CONFIG['raw_data_table_name'],
            column_names=COLUMN_NAMES,
            data=all_results
        )
    except Exception as e:
        print(f"!!! ERRO CRÍTICO NA GRAVAÇÃO DO BANCO: {e} !!!")
    finally:
        db_handler.close()

    end_time = time.time()
    print(f"--- PIPELINE DE SCRAPING CONCLUÍDA EM {end_time - start_time:.2f} segundos ---")