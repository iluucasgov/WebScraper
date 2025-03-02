# src/core/parser.py
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Any
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class BaseParser:
    '''Classe base para parsers HTML'''

    @staticmethod
    def create_soup(html_content: str) -> Optional[BeautifulSoup]:
        '''Cria um objeto Beautifulsoup a partir do HTML'''
        if not html_content:
            return None
        return BeautifulSoup(html_content, 'html.parser')
    
    @staticmethod
    def extract_text(element, selector: str, default: str = "") -> str:
        '''Extrai texto de um elemento usando selctor CSS'''
        if not element:
            return default
        
        found = element.select_one(selector)
        return found.text.strip() if found else default
    
    @staticmethod
    def extract_attribute(element, selector: str, attr: str, default: Optional[str] = None) -> Optional[str]:
        '''Extrai um atributo de um elemento usando selctor CSS'''
        if not element:
            return default
        
        found = element.select_one(selector)
        return found.get(attr, default) if found else default
