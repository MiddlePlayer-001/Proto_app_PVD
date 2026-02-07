"""
Configurações da aplicação
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Diretórios
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
SRC_DIR = BASE_DIR / "src"

# Banco de dados
DATABASE_PATH = os.getenv("DATABASE_PATH", str(DATA_DIR / "loja.db"))

# Loja
STORE_NAME = os.getenv("STORE_NAME", "Minha Loja")

# Impressão
RECEIPT_WIDTH = int(os.getenv("RECEIPT_WIDTH", "58"))  # 58mm ou 80mm

# Fuso horário
TIMEZONE = os.getenv("TIMEZONE", "UTC-3")

# Debug
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Cores do tema escuro (Flet)
COLORS = {
    'primary': '#2196F3',
    'primary_dark': '#1976D2',
    'primary_light': '#42A5F5',
    'accent': '#FF5722',
    'background': '#121212',
    'surface': '#1E1E1E',
    'surface_light': '#262626',
    'text_primary': '#FFFFFF',
    'text_secondary': '#BDBDBD',
    'success': '#4CAF50',
    'warning': '#FF9800',
    'error': '#F44336',
    'info': '#2196F3',
}

# Configuração de temas
THEME_CONFIG = {
    'primary_color': COLORS['primary'],
    'accent_color': COLORS['accent'],
    'background_color': COLORS['background'],
    'text_color': COLORS['text_primary'],
}

# Formas de pagamento
FORMAS_PAGAMENTO = [
    'Dinheiro',
    'Cartão de Crédito',
    'Cartão de Débito',
    'PIX',
    'Boleto',
    'Cheque',
]

# Configuração de PDV
PDV_CONFIG = {
    'auto_logout_seconds': 600,  # 10 minutos
    'modo_demo': False,
    'som_ativo': True,
    'impressao_automatica': False,
}
