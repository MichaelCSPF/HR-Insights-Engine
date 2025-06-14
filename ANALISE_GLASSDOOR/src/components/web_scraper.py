import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

class GlassdoorScraper:
    """Encapsula a lógica de scraping do Glassdoor usando Selenium e BeautifulSoup."""

    def __init__(self, config: dict):
        """Inicializa o scraper com as configurações e seletores."""
        self.config = config
        self.base_url = config['base_url_template']

    def _get_safe_text(self, soup_element, selector):
        try:
            tag = soup_element.select_one(selector)
            return tag.get_text(strip=True) if tag else None
        except Exception:
            return None

    def _parse_review_data(self, review_soup):
        """Extrai dados de um único container de avaliação."""
        data = {
            'DATA_AVALIACAO': self._get_safe_text(review_soup, self.config['selectors']['review_date']),
            'TITULO': self._get_safe_text(review_soup, self.config['selectors']['review_title']),
            'CARGO_LOCAL': self._get_safe_text(review_soup, self.config['selectors']['job_title']),
            'NOTA_GERAL_TEXT': self._get_safe_text(review_soup, self.config['selectors']['rating_overall']),
            'PROS': self._get_safe_text(review_soup, self.config['selectors']['pros']),
            'CONS': self._get_safe_text(review_soup, self.config['selectors']['cons']),
            'CONSELHOS_DIRETORIA': self._get_safe_text(review_soup, self.config['selectors']['advice']),
            'RECOMENDA': self._get_safe_text(review_soup, self.config['selectors']['recommend']),
            'APROVA_CEO': self._get_safe_text(review_soup, self.config['selectors']['ceo_approval']),
            'PERSPECTIVA_EMPRESA': self._get_safe_text(review_soup, self.config['selectors']['business_outlook']),
        }
        # Retorna apenas se dados essenciais foram encontrados
        return data if data['TITULO'] and data['NOTA_GERAL_TEXT'] else None

    def scrape_page_range(self, page_range: list, thread_id: int) -> list:
        """
        Raspa um intervalo de páginas e retorna uma lista de avaliações.
        Projetado para ser executado dentro de uma thread.
        """
        print(f"[Thread {thread_id}] Iniciando. Páginas: {page_range[0]}-{page_range[-1]}")
        driver = None
        results = []

        try:
            # Configuração do WebDriver
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument(f"user-agent={self.config['user_agent']}")
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.set_page_load_timeout(self.config['page_load_timeout'])

            for page_num in page_range:
                try:
                    driver.get(self.base_url.format(page=page_num))
                    WebDriverWait(driver, self.config['page_load_timeout']).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, self.config['selectors']['review_container']))
                    )
                    
                    # Clicar em "Mostrar Mais"
                    buttons = driver.find_elements(By.CSS_SELECTOR, self.config['selectors']['show_more_button'])
                    for button in buttons:
                        try:
                            driver.execute_script("arguments[0].click();", button)
                        except Exception:
                            pass
                    if buttons:
                        time.sleep(self.config['click_wait_time'])
                    
                    # Parsear
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    review_elements = soup.select(self.config['selectors']['review_container'])
                    for review_elem in review_elements:
                        data = self._parse_review_data(review_elem)
                        if data:
                            results.append(data)
                except TimeoutException:
                    print(f"[Thread {thread_id} | Pg {page_num}] ERRO: Timeout. Pulando página.")
                except Exception as e:
                    print(f"[Thread {thread_id} | Pg {page_num}] ERRO Inesperado: {type(e).__name__}. Pulando página.")
        finally:
            if driver:
                driver.quit()

        print(f"[Thread {thread_id}] Finalizada. Coletou {len(results)} avaliações.")
        return results