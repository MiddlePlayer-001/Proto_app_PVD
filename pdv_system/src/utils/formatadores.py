"""
Formatadores de dados para exibição
"""
from datetime import datetime, date


class FormataçãoUtil:
    """Utilitários de formatação"""

    @staticmethod
    def formatar_moeda(valor: float) -> str:
        """Formata um valor como moeda brasileira"""
        return f"R$ {valor:,.2f}".replace(",", ".")

    @staticmethod
    def formatar_percentual(valor: float, casas: int = 2) -> str:
        """Formata um valor como percentual"""
        return f"{valor:.{casas}f}%"

    @staticmethod
    def formatar_quantidade(quantidade: int) -> str:
        """Formata uma quantidade"""
        return f"{quantidade:,}".replace(",", ".")

    @staticmethod
    def formatar_data(data: date, formato: str = "%d/%m/%Y") -> str:
        """Formata uma data"""
        if isinstance(data, datetime):
            return data.strftime(formato)
        return data.strftime(formato)

    @staticmethod
    def formatar_data_hora(dt: datetime, formato: str = "%d/%m/%Y %H:%M:%S") -> str:
        """Formata uma data e hora"""
        return dt.strftime(formato)

    @staticmethod
    def formatar_codigo_barra(codigo: str) -> str:
        """Formata um código de barras"""
        return codigo.strip().upper()

    @staticmethod
    def truncar_texto(texto: str, max_chars: int = 50) -> str:
        """Trunca um texto"""
        if len(texto) > max_chars:
            return texto[:max_chars - 3] + "..."
        return texto

    @staticmethod
    def remover_acentos(texto: str) -> str:
        """Remove acentos de um texto"""
        import unicodedata
        nfd = unicodedata.normalize('NFD', texto)
        return ''.join(c for c in nfd if unicodedata.category(c) != 'Mn')
