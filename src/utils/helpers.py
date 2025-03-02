import urllib.robotparser 
import urllib.parse
import time
import os
from datetime import datetime
from src.config.settings import DELAY_BETWEEN_REQUESTS

def is_sraping_allowed(ur, user_agent="*"):
    '''Verifica se o scraping é permitido pelo robots.txt'''
    try:
        rp = urllib.robotparser.RobotFileParser()
        base_url = urllib.parse.urlparse(url).scheme + "://" + urllib.parse.urlparse(url).netloc
        robots_url = urllib.parse.urljoin(base_url, "/robots.txt")  
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch(user_agent, url)
    except Exception:
        # Em caso de erro, assumir permissao por padrao, mas logar aviso
        return True
    
def wait_between_request(custom_delay=None):
    '''Pausa entre requisições para evitar sobrecar do servidor'''
    delay = custom_delay if custom_delay is not None else DELAY_BETWEEN_REQUESTS
    time.sleep(delay)

def generate_filename(prefix, extension=None):
    '''Gera um nome de arquivo com timestamp'''
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"