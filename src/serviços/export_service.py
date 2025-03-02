# src/services/export_service.py
import pandas as pd
import json
import os
from typing import List, Dict, Union, Optional
from src.models.trademark import SearchResult
from src.utils.logger import setup_logger
from src.utils.helpers import generate_filename
from src.config.settings import DATA_DIR

logger = setup_logger(__name__)

class ExportService:
    """Serviço para exportação de dados"""
    
    @staticmethod
    def to_csv(data: Union[List[Dict], SearchResult], filename: Optional[str] = None) -> str:
        """Exporta dados para CSV"""
        if isinstance(data, SearchResult):
            data_to_export = data.to_dict_list()
        else:
            data_to_export = data
        
        if not data_to_export:
            logger.warning("Não há dados para exportar")
            return ""
        
        if not filename:
            filename = os.path.join(DATA_DIR, generate_filename("inpi_results", "csv"))
        elif not os.path.isabs(filename):
            filename = os.path.join(DATA_DIR, filename)
        
        try:
            df = pd.DataFrame(data_to_export)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            logger.info(f"Dados exportados para CSV: {filename}")
            return filename
        except Exception as e:
            logger.error(f"Erro ao exportar para CSV: {e}")
            return ""
    
    @staticmethod
    def to_json(data: Union[List[Dict], SearchResult], filename: Optional[str] = None) -> str:
        """Exporta dados para JSON"""
        if isinstance(data, SearchResult):
            data_to_export = data.to_dict_list()
        else:
            data_to_export = data
        
        if not data_to_export:
            logger.warning("Não há dados para exportar")
            return ""
        
        if not filename:
            filename = os.path.join(DATA_DIR, generate_filename("inpi_results", "json"))
        elif not os.path.isabs(filename):
            filename = os.path.join(DATA_DIR, filename)
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data_to_export, f, ensure_ascii=False, indent=4)
            
            logger.info(f"Dados exportados para JSON: {filename}")
            return filename
        except Exception as e:
            logger.error(f"Erro ao exportar para JSON: {e}")
            return ""
    
    @staticmethod
    def to_excel(data: Union[List[Dict], SearchResult], filename: Optional[str] = None) -> str:
        """Exporta dados para Excel"""
        if isinstance(data, SearchResult):
            data_to_export = data.to_dict_list()
        else:
            data_to_export = data
        
        if not data_to_export:
            logger.warning("Não há dados para exportar")
            return ""
        
        if not filename:
            filename = os.path.join(DATA_DIR, generate_filename("inpi_results", "xlsx"))
        elif not os.path.isabs(filename):
            filename = os.path.join(DATA_DIR, filename)
        
        try:
            df = pd.DataFrame(data_to_export)
            df.to_excel(filename, index=False, engine='openpyxl')
            logger.info(f"Dados exportados para Excel: {filename}")
            return filename
        except Exception as e:
            logger.error(f"Erro ao exportar para Excel: {e}")
            return ""