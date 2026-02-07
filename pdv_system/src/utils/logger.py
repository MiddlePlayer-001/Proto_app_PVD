"""
Sistema de Logging Estruturado para PDV
Registra todas as operações em arquivo e console
"""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime


class PDVLogger:
    """Logger centralizado para PDV System"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Inicializa o logger singleton"""
        # Criar diretório de logs
        self.log_dir = Path(__file__).resolve().parent.parent.parent / "logs"
        self.log_dir.mkdir(exist_ok=True)
        
        # Logger principal
        self.logger = logging.getLogger("pdv_system")
        self.logger.setLevel(logging.DEBUG)
        
        # Evitar duplicação de handlers
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        
        # Formato de log
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%d/%m/%Y %H:%M:%S'
        )
        
        # Handler para arquivo (Rotating)
        file_handler = RotatingFileHandler(
            self.log_dir / "pdv_system.log",
            maxBytes=10_000_000,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Handler para arquivo de erros
        error_handler = RotatingFileHandler(
            self.log_dir / "pdv_errors.log",
            maxBytes=5_000_000,  # 5MB
            backupCount=3,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        self.logger.addHandler(error_handler)
        
        # Handler para console (INFO em diante)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
    
    def get_logger(self, name: str = None):
        """Retorna um logger com nome especificado"""
        if name:
            return logging.getLogger(f"pdv_system.{name}")
        return self.logger
    
    def log_info(self, mensagem: str, **kwargs):
        """Log de informação"""
        self.logger.info(f"{mensagem} | {kwargs}" if kwargs else mensagem)
    
    def log_warning(self, mensagem: str, **kwargs):
        """Log de aviso"""
        self.logger.warning(f"{mensagem} | {kwargs}" if kwargs else mensagem)
    
    def log_error(self, mensagem: str, exc_info=False, **kwargs):
        """Log de erro"""
        self.logger.error(
            f"{mensagem} | {kwargs}" if kwargs else mensagem,
            exc_info=exc_info
        )
    
    def log_debug(self, mensagem: str, **kwargs):
        """Log de debug"""
        self.logger.debug(f"{mensagem} | {kwargs}" if kwargs else mensagem)
    
    def log_venda(self, numero_venda: int, acao: str, detalhes: str = ""):
        """Log específico de venda"""
        msg = f"[VENDA #{numero_venda}] {acao}"
        if detalhes:
            msg += f" - {detalhes}"
        self.logger.info(msg)
    
    def log_operacao_banco(self, operacao: str, tabela: str, detalhes: str = ""):
        """Log específico de operações de banco"""
        msg = f"[BD] {operacao} em {tabela}"
        if detalhes:
            msg += f" - {detalhes}"
        self.logger.debug(msg)
    
    def log_performance(self, operacao: str, tempo_ms: float):
        """Log de performance"""
        if tempo_ms > 1000:  # Mais de 1 segundo
            self.logger.warning(f"[PERF] {operacao} levou {tempo_ms:.2f}ms")
        else:
            self.logger.debug(f"[PERF] {operacao} levou {tempo_ms:.2f}ms")


# Instância global do logger
_logger = PDVLogger()

def get_logger(name: str = None):
    """Função helper para obter logger"""
    return _logger.get_logger(name)

def log_info(msg: str, **kwargs):
    """Helper para log de info"""
    _logger.log_info(msg, **kwargs)

def log_error(msg: str, exc_info=False, **kwargs):
    """Helper para log de erro"""
    _logger.log_error(msg, exc_info=exc_info, **kwargs)

def log_warning(msg: str, **kwargs):
    """Helper para log de warning"""
    _logger.log_warning(msg, **kwargs)

def log_debug(msg: str, **kwargs):
    """Helper para log de debug"""
    _logger.log_debug(msg, **kwargs)

def log_venda(numero: int, acao: str, detalhes: str = ""):
    """Helper para logs de venda"""
    _logger.log_venda(numero, acao, detalhes)

def log_bd(operacao: str, tabela: str, detalhes: str = ""):
    """Helper para logs de banco de dados"""
    _logger.log_operacao_banco(operacao, tabela, detalhes)
