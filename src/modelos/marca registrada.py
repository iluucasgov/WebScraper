# src/models/trademark.py
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime

@dataclass
class TrademarkProcess:
    '''Representa um processo de marca/patente no INPI'''
    processo: str
    marca: str
    situacao: str
    data: str
    link_detalhes: Optional[str] = None
    detalhes: Dict  = field(default_factory=dict)

    def to_dict(self) -> Dict:
        '''Converte o objeto para dicionário'''
        base_dict = {
            "processo": self.processo,
            "marca": self.marca,
            "situacao": self.situacao,
            "data": self.data,
            "link_detalhes": self.link_detalhes
        }

        # Adicionar detalhes se existirem 
        if self.detalhes:
            for key, value in self.detalhes.items():
                if key not in base_dict: # Evitar sobrescrevcer dados principais 
                    base_dict[key]  = value 
      
        return base_dict
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'TrademarkProcess':
        '''Cria objeto apartir de um dicionario'''
        details = {k: v for k, v in data.items()
                   if k not in ["processo", "marca", "situação", "data", "link_detalhes"]}
        
        return cls(
            processo=data.get("processo", ""),
            marca=data.get("marca", ""),
            situacao=data.get("situacao", ""),
            data=data.get("data", ""),
            link_detalhes=data.get("link_detalhes"),
            detalhes=details
        )
    
@dataclass
class SearchResult:
    '''Representa resultados de uma busca'''
    query: str
    timestamp: datetime = field(default_factory=datetime.now)
    results: List[TrademarkProcess] = field(default_factory=list)

    def to_dict_list(self) -> List[dict]:
        '''Converter os resultadoss para lista de dicionario'''
        return [result.to_dict() for result in self.results]
    
    def count(self) -> int:
        '''Retorna a quantidade de resoltados'''
        return len(self.results)