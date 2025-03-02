#src/config/settings.py
import os 
from pathlib import Path

# caminhos
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = os.path.join(BASE_DIR, "data")
LOGS_DIR = os.path.join(BASE_DIR, "logs")   

# Configurações do scraper 
INPI_BASE_URL = "https://busca.inpi.gov.br/pePI/servlet"
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
REQUEST_TIMEOUT = 30 # segundos
DELAY_BETWENN_REQUESTS = 2 # segundos 

# Configurações de logging 
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = os.path.join(LOGS_DIR, "inpi_scraper.log")

# verificar e criar diretorios necessários 
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)