"""
Validadores de dados de entrada
"""
import re


class ValidadorUtil:
    """Utilitários de validação"""

    @staticmethod
    def validar_moeda(valor: str) -> bool:
        """Valida se um valor é moeda válida"""
        try:
            float(valor)
            return True
        except ValueError:
            return False

    @staticmethod
    def validar_inteiro(valor: str) -> bool:
        """Valida se um valor é inteiro"""
        try:
            int(valor)
            return True
        except ValueError:
            return False

    @staticmethod
    def validar_codigo_produto(codigo: str) -> bool:
        """Valida um código de produto"""
        if not codigo or len(codigo) == 0:
            return False
        if len(codigo) > 50:
            return False
        return True

    @staticmethod
    def validar_nome_produto(nome: str) -> bool:
        """Valida um nome de produto"""
        if not nome or len(nome) < 3:
            return False
        if len(nome) > 200:
            return False
        return True

    @staticmethod
    def validar_preco(preco: float) -> bool:
        """Valida um preço"""
        if preco <= 0:
            return False
        return True

    @staticmethod
    def validar_quantidade(quantidade: int) -> bool:
        """Valida uma quantidade"""
        if quantidade < 0:
            return False
        return True

    @staticmethod
    def validar_email(email: str) -> bool:
        """Valida um email"""
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(padrao, email) is not None

    @staticmethod
    def validar_telefone(telefone: str) -> bool:
        """Valida um telefone brasileiro"""
        # Remove caracteres especiais
        telefone_limpo = re.sub(r'[^0-9]', '', telefone)
        # Valida DDD (11) + número (9 dígitos)
        return len(telefone_limpo) >= 10 and len(telefone_limpo) <= 11

    @staticmethod
    def validar_cpf(cpf: str) -> bool:
        """Valida um CPF"""
        # Remove caracteres especiais
        cpf_limpo = re.sub(r'[^0-9]', '', cpf)
        
        if len(cpf_limpo) != 11:
            return False
        
        # CPF com todos dígitos iguais é inválido
        if cpf_limpo == cpf_limpo[0] * 11:
            return False
        
        # Validar primeiro dígito verificador
        soma = sum(int(cpf_limpo[i]) * (10 - i) for i in range(9))
        digito1 = 11 - (soma % 11)
        digito1 = 0 if digito1 > 9 else digito1
        
        # Validar segundo dígito verificador
        soma = sum(int(cpf_limpo[i]) * (11 - i) for i in range(10))
        digito2 = 11 - (soma % 11)
        digito2 = 0 if digito2 > 9 else digito2
        
        return int(cpf_limpo[9]) == digito1 and int(cpf_limpo[10]) == digito2
