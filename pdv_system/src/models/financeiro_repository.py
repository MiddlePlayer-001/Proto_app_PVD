"""
Repositório Financeiro - Transações e Fechamento
"""
from src.database.models import Transacao, FechamentoDia, Venda
from decimal import Decimal
from datetime import datetime, date
from typing import Dict


class TransacaoRepository:
    """Gerencia transações financeiras unificadas"""

    @staticmethod
    def registrar_transacao(tipo: str, categoria: str, descricao: str,
                           valor: Decimal, data_transacao: datetime = None,
                           venda_id: int = None, observacoes: str = None) -> Transacao:
        """Registra uma nova transação"""
        if data_transacao is None:
            data_transacao = datetime.now()
        
        # Validar tipo e categoria
        tipos_validos = ['ENTRADA', 'SAIDA']
        categorias_validas = ['VENDA', 'DESPESA', 'DEVOLUCAO', 'AJUSTE']
        
        if tipo not in tipos_validos:
            raise ValueError(f"Tipo inválido. Use: {', '.join(tipos_validos)}")
        
        if categoria not in categorias_validas:
            raise ValueError(f"Categoria inválida. Use: {', '.join(categorias_validas)}")
        
        if valor <= 0:
            raise ValueError("Valor deve ser maior que zero")
        
        transacao = Transacao.create(
            tipo=tipo,
            categoria=categoria,
            descricao=descricao,
            valor=valor,
            data_transacao=data_transacao,
            venda_id=venda_id,
            observacoes=observacoes
        )
        return transacao

    @staticmethod
    def registrar_despesa(descricao: str, valor: Decimal,
                         observacoes: str = None) -> Transacao:
        """Atalho para registrar uma despesa (SAIDA)"""
        return TransacaoRepository.registrar_transacao(
            tipo='SAIDA',
            categoria='DESPESA',
            descricao=descricao,
            valor=valor,
            observacoes=observacoes
        )

    @staticmethod
    def listar_transacoes_dia(data_dia: date = None) -> list:
        """Lista todas as transações de um dia"""
        if data_dia is None:
            data_dia = date.today()
        
        inicio = datetime.combine(data_dia, datetime.min.time())
        fim = datetime.combine(data_dia, datetime.max.time())
        
        return list(
            Transacao.select()
            .where(
                (Transacao.data_transacao >= inicio) &
                (Transacao.data_transacao <= fim)
            )
            .order_by(Transacao.data_transacao.desc())
        )

    @staticmethod
    def listar_transacoes_periodo(data_inicio: date, data_fim: date) -> list:
        """Lista transações de um período"""
        inicio = datetime.combine(data_inicio, datetime.min.time())
        fim = datetime.combine(data_fim, datetime.max.time())
        
        return list(
            Transacao.select()
            .where(
                (Transacao.data_transacao >= inicio) &
                (Transacao.data_transacao <= fim)
            )
            .order_by(Transacao.data_transacao.desc())
        )

    @staticmethod
    def obter_resumo_dia(data_dia: date = None) -> Dict:
        """Obtém um resumo financeiro do dia"""
        if data_dia is None:
            data_dia = date.today()
        
        transacoes = TransacaoRepository.listar_transacoes_dia(data_dia)
        
        total_entradas = sum(
            t.valor for t in transacoes if t.tipo == 'ENTRADA'
        )
        total_saidas = sum(
            t.valor for t in transacoes if t.tipo == 'SAIDA'
        )
        
        vendas_dia = Venda.select().where(
            (Venda.processada == 1) &
            (Venda.data_hora >= datetime.combine(data_dia, datetime.min.time())) &
            (Venda.data_hora <= datetime.combine(data_dia, datetime.max.time()))
        )
        
        quantidade_vendas = len(list(vendas_dia))
        
        return {
            'data': data_dia,
            'total_entradas': Decimal(str(total_entradas)),
            'total_saidas': Decimal(str(total_saidas)),
            'saldo': Decimal(str(total_entradas - total_saidas)),
            'quantidade_vendas': quantidade_vendas,
            'quantidade_transacoes': len(transacoes),
        }

    @staticmethod
    def obter_resumo_periodo(data_inicio: date, data_fim: date) -> Dict:
        """Obtém um resumo financeiro de um período"""
        transacoes = TransacaoRepository.listar_transacoes_periodo(data_inicio, data_fim)
        
        total_entradas = sum(
            t.valor for t in transacoes if t.tipo == 'ENTRADA'
        )
        total_saidas = sum(
            t.valor for t in transacoes if t.tipo == 'SAIDA'
        )
        
        return {
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'total_entradas': Decimal(str(total_entradas)),
            'total_saidas': Decimal(str(total_saidas)),
            'saldo': Decimal(str(total_entradas - total_saidas)),
            'quantidade_transacoes': len(transacoes),
        }


class FechamentoDiaRepository:
    """Gerencia fechamento diário"""

    @staticmethod
    def criar_fechamento(data_dia: date = None) -> FechamentoDia:
        """Cria um fechamento do dia"""
        if data_dia is None:
            data_dia = date.today()
        
        # Verificar se já existe fechamento
        fechamento_existente = FechamentoDia.select().where(
            FechamentoDia.data == data_dia
        ).first()
        
        if fechamento_existente:
            raise ValueError(f"Já existe fechamento para {data_dia}")
        
        # Calcular totais
        total_vendas = Decimal('0')
        total_despesas = Decimal('0')
        total_entradas = Decimal('0')
        
        vendas = Venda.select().where(
            (Venda.processada == 1) &
            (Venda.data_hora >= datetime.combine(data_dia, datetime.min.time())) &
            (Venda.data_hora <= datetime.combine(data_dia, datetime.max.time()))
        )
        
        for venda in vendas:
            total_vendas += (venda.total - venda.desconto)
        
        transacoes = TransacaoRepository.listar_transacoes_dia(data_dia)
        
        for transacao in transacoes:
            if transacao.tipo == 'ENTRADA':
                total_entradas += transacao.valor
            elif transacao.tipo == 'SAIDA':
                total_despesas += transacao.valor
        
        # Criar fechamento
        fechamento = FechamentoDia.create(
            data=datetime.combine(data_dia, datetime.min.time()),
            total_vendas=total_vendas,
            total_despesas=total_despesas,
            total_entradas=total_entradas,
            saldo=total_entradas - total_despesas,
            quantidade_transacoes=len(transacoes)
        )
        
        return fechamento

    @staticmethod
    def obter_fechamento(data_dia: date = None) -> FechamentoDia:
        """Obtém o fechamento de um dia"""
        if data_dia is None:
            data_dia = date.today()
        
        try:
            return FechamentoDia.get(FechamentoDia.data == data_dia)
        except FechamentoDia.DoesNotExist as exc:
            raise ValueError(f"Fechamento não encontrado para {data_dia}") from exc

    @staticmethod
    def listar_fechamentos(data_inicio: date = None, data_fim: date = None) -> list:
        """Lista fechamentos de um período"""
        query = FechamentoDia.select()
        
        if data_inicio and data_fim:
            inicio = datetime.combine(data_inicio, datetime.min.time())
            fim = datetime.combine(data_fim, datetime.max.time())
            query = query.where(
                (FechamentoDia.data >= inicio) &
                (FechamentoDia.data <= fim)
            )
        
        return list(query.order_by(FechamentoDia.data.desc()))

    @staticmethod
    def verificar_fechamento_existe(data_dia: date = None) -> bool:
        """Verifica se já existe fechamento para o dia"""
        if data_dia is None:
            data_dia = date.today()
        
        return FechamentoDia.select().where(
            FechamentoDia.data == data_dia
        ).exists()


def get_resumo_dia(data: date = None) -> Dict:
    """
    Retorna um resumo financeiro do dia (Dashboard)
    
    Consulta a tabela Transacao (MovimentoFinanceiro) e calcula:
    - Total de Vendas (ENTRADA onde categoria=VENDA)
    - Total de Despesas (SAIDA)
    - Saldo Líquido (Vendas - Despesas)
    
    Args:
        data (date): Data para consulta (padrão: hoje)
        
    Returns:
        dict: {
            'total_vendas': Decimal,
            'total_despesas': Decimal,
            'saldo_liquido': Decimal,
            'data': date,
            'quantidade_transacoes': int
        }
    """
    if data is None:
        data = date.today()
    
    # Buscar todas as transações do dia
    inicio_dia = datetime.combine(data, datetime.min.time())
    fim_dia = datetime.combine(data, datetime.max.time())
    
    transacoes = Transacao.select().where(
        (Transacao.data_transacao >= inicio_dia) &
        (Transacao.data_transacao <= fim_dia)
    )
    
    # Calcular totais
    total_vendas = Decimal('0.00')
    total_despesas = Decimal('0.00')
    
    for transacao in transacoes:
        if transacao.tipo == 'ENTRADA' and transacao.categoria == 'VENDA':
            total_vendas += transacao.valor
        elif transacao.tipo == 'SAIDA':
            total_despesas += transacao.valor
    
    saldo_liquido = total_vendas - total_despesas
    
    return {
        'total_vendas': total_vendas,
        'total_despesas': total_despesas,
        'saldo_liquido': saldo_liquido,
        'data': data,
        'quantidade_transacoes': len(list(transacoes))
    }

