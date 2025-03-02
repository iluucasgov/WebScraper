# main.py
import argparse
import sys
from src.services.inpi_service import INPIService
from src.services.export_service import ExportService
from src.utils.logger import setup_logger

logger = setup_logger("main")

def create_parser():
    """Cria o parser de argumentos de linha de comando"""
    parser = argparse.ArgumentParser(description="Web Scraper para o INPI")
    
    parser.add_argument("--termo", "-t", required=True, help="Termo de busca")
    parser.add_argument("--tipo", choices=["MU", "PI", "DI"], default="MU", 
                        help="Tipo de processo (MU=Marca, PI=Patente, DI=Desenho Industrial)")
    parser.add_argument("--detalhes", "-d", action="store_true", 
                        help="Obter detalhes de cada processo")
    parser.add_argument("--max", "-m", type=int, default=None, 
                        help="Número máximo de resultados para obter detalhes")
    parser.add_argument("--formato", "-f", choices=["csv", "json", "excel"], default="csv", 
                        help="Formato de exportação dos dados")
    parser.add_argument("--saida", "-o", help="Nome do arquivo de saída")
    parser.add_argument("--usuario", "-u", help="Nome de usuário para login")
    parser.add_argument("--senha", "-p", help="Senha para login")
    
    return parser

def main():
    """Função principal do programa"""
    # Criar parser e processar argumentos
    parser = create_parser()
    args = parser.parse_args()
    
    # Inicializar serviço
    inpi_service = INPIService()
    
    # Tentar login se credenciais foram fornecidas
    if args.usuario or args.senha:
        if not inpi_service.login(args.usuario, args.senha):
            logger.error("Falha no login. Saindo.")
            sys.exit(1)
    
    # Realizar busca
    logger.info(f"Buscando por '{args.termo}' com tipo '{args.tipo}'")
    search_result = inpi_service.search_trademark(args.termo, args.tipo)
    
    if search_result.count() == 0:
        logger.info(f"Nenhum resultado encontrado para '{args.termo}'")
        sys.exit(0)
    
    logger.info(f"Encontrados {search_result.count()} resultados")
    
    # Obter detalhes se solicitado
    if args.detalhes:
        logger.info("Obtendo detalhes dos processos...")
        search_result = inpi_service.enrich_results_with_details(search_result, args.max)
    
    # Exportar resultados
    export_service = ExportService()
    
    if args.formato == "csv":
        export_service.to_csv(search_result, args.saida)
    elif args.formato == "json":
        export_service.to_json(search_result, args.saida)
    elif args.formato == "excel":
        export_service.to_excel(search_result, args.saida)

if __name__ == "__main__":
    main()