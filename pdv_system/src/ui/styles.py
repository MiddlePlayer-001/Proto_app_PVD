"""
Estilos e tema da aplicação
"""
from src.utils.config import COLORS


class AppTheme:
    """Tema da aplicação"""
    
    PRIMARY = COLORS['primary']
    PRIMARY_DARK = COLORS['primary_dark']
    PRIMARY_LIGHT = COLORS['primary_light']
    ACCENT = COLORS['accent']
    
    BACKGROUND = COLORS['background']
    SURFACE = COLORS['surface']
    SURFACE_LIGHT = COLORS['surface_light']
    
    TEXT_PRIMARY = COLORS['text_primary']
    TEXT_SECONDARY = COLORS['text_secondary']
    
    SUCCESS = COLORS['success']
    WARNING = COLORS['warning']
    ERROR = COLORS['error']
    INFO = COLORS['info']

    # Espaçamentos
    PADDING_SMALL = 8
    PADDING_MEDIUM = 16
    PADDING_LARGE = 24

    # Tamanhos de fonte
    FONT_SMALL = 12
    FONT_NORMAL = 14
    FONT_MEDIUM = 16
    FONT_LARGE = 18
    FONT_XLARGE = 24

    # Alturas de botão
    BUTTON_HEIGHT_SMALL = 32
    BUTTON_HEIGHT_NORMAL = 40
    BUTTON_HEIGHT_LARGE = 56  # Para PDV

    # Raios de borda
    BORDER_RADIUS_SMALL = 4
    BORDER_RADIUS_NORMAL = 8
    BORDER_RADIUS_LARGE = 12


class ButtonStyle:
    """Estilos de botão"""
    
    @staticmethod
    def primary():
        """Botão principal"""
        return {
            'bgcolor': AppTheme.PRIMARY,
            'color': AppTheme.TEXT_PRIMARY,
            'height': AppTheme.BUTTON_HEIGHT_NORMAL,
        }
    
    @staticmethod
    def primary_large():
        """Botão principal grande (para PDV)"""
        return {
            'bgcolor': AppTheme.PRIMARY,
            'color': AppTheme.TEXT_PRIMARY,
            'height': AppTheme.BUTTON_HEIGHT_LARGE,
        }
    
    @staticmethod
    def accent():
        """Botão de ação"""
        return {
            'bgcolor': AppTheme.ACCENT,
            'color': AppTheme.TEXT_PRIMARY,
            'height': AppTheme.BUTTON_HEIGHT_NORMAL,
        }
    
    @staticmethod
    def success():
        """Botão de sucesso"""
        return {
            'bgcolor': AppTheme.SUCCESS,
            'color': AppTheme.TEXT_PRIMARY,
            'height': AppTheme.BUTTON_HEIGHT_NORMAL,
        }
    
    @staticmethod
    def danger():
        """Botão de perigo"""
        return {
            'bgcolor': AppTheme.ERROR,
            'color': AppTheme.TEXT_PRIMARY,
            'height': AppTheme.BUTTON_HEIGHT_NORMAL,
        }
    
    @staticmethod
    def secondary():
        """Botão secundário"""
        return {
            'bgcolor': AppTheme.SURFACE_LIGHT,
            'color': AppTheme.TEXT_PRIMARY,
            'height': AppTheme.BUTTON_HEIGHT_NORMAL,
        }
