import requests
from typing import Dict, Optional, Any
from src.utils.logger import setup_logger
from src.utils.helpers import is_sraping_allowed, wait_between_requests
from src.config.settings import DEFAULT_USER_AGENT, REQUEST_TIMEOUT

logger = setup_logger(__name__)

class BaseScraper:
    '''Classe base para scrapers'''

    def __init__(self, base_url: str, respect_robots: bool = True):
        self.base_url = base_url
        self.respect_robots = respect_robots
        self.session = requests.Session()
        self.headers = {
            'User-Agent': DEFAULT_USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
        }
    
    def get(self, url: str, params: Optional[Dict] = None) -> Optional[str]:
        '''Realiza uma requisao GET com tratamento de erros e verificao robots.txt'''
        full_url = url if url.startswith('http') else f"{self.base_url}/{url}"

        # Verificar permissao de robts.txt se configurado
        if self.respect_robots and not is_sraping_allowed(full_url, self.headers.get('User-Agent')):
            logger.warning(f"Scraping não permitido para URL: {full_url}")
            return None
        
        try:
            logger.info(f"Acessando URL: {full_url}")
            response = self.session.get(
                url=full_url,
                params=params,
                headers=self.headers,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()

            wait_between_requests() # Pausa entre requisições 
            return response.text
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao acessar URL {full_url}: {e}")
            return None
        
    def post(self, url: str, data: Dict, params: Optional[Dict] = None) -> Optional[str]:
        """Realiza uma requisição POST com tratamento de erros"""
        full_url = url if url.startswith('http') else f"{self.base_url}/{url}"
        
        try:
            logger.info(f"Enviando POST para: {full_url}")
            response = self.session.post(
                url=full_url, 
                data=data, 
                params=params, 
                headers=self.headers,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            
            wait_between_requests()  # Pausa entre requisições
            return response.text
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao enviar POST para {full_url}: {e}")
            return None
    
    def update_headers(self, new_headers: Dict[str, str]) -> None:
        '''Atualiza os headers da sessão'''
        self.headers.update(new_headers)