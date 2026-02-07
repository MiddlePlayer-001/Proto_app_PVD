"""
Serviço Financeiro - Lógica de Negócio
"""
from src.models.financeiro_repository import (
    TransacaoRepository, FechamentoDiaRepository
)
from decimal import Decimal
from typing import Dict, List
from datetime import date


class FinanceiroService:
    """Serviço de gerenciamento financeiro"""

    def __init__(self):
        self.transacao_repo = TransacaoRepository()
        self.fechamento_repo = FechamentoDiaRepository()

    def registrar_despesa(self, descricao: str, valor: float,
                         observacoes: str = None) -> Dict:
        """Registra uma despesa"""
        try:
            transacao = self.transacao_repo.registrar_despesa(
                descricao,
                Decimal(str(valor)),
                observacoes
            )
            return self._serializar_transacao(transacao)
        except Exception as e:
            raise ValueError(f"Erro ao registrar despesa: {str(e)}") from e

    def obter_resumo_dia(self, data_dia: date = None) -> Dict:
        """Obtém o resumo financeiro do dia"""
        try:
            resumo = self.transacao_repo.obter_resumo_dia(data_dia)
            
            return {
                'data': resumo['data'].isoformat(),
                'total_entradas': float(resumo['total_entradas']),
                'total_saidas': float(resumo['total_saidas']),
                'saldo': float(resumo['saldo']),
                'quantidade_vendas': resumo['quantidade_vendas'],
                'quantidade_transacoes': resumo['quantidade_transacoes'],
            }
        except Exception as e:
            raise ValueError(f"Erro ao obter resumo: {str(e)}") from e

    def obter_resumo_periodo(self, data_inicio: date, data_fim: date) -> Dict:
        """Obtém o resumo financeiro de um período"""
        try:
            resumo = self.transacao_repo.obter_resumo_periodo(data_inicio, data_fim)
            
            return {
                'data_inicio': resumo['data_inicio'].isoformat(),
                'data_fim': resumo['data_fim'].isoformat(),
                'total_entradas': float(resumo['total_entradas']),
                'total_saidas': float(resumo['total_saidas']),
                'saldo': float(resumo['saldo']),
                'quantidade_transacoes': resumo['quantidade_transacoes'],
            }
        except Exception as e:
            raise ValueError(f"Erro ao obter resumo: {str(e)}") from e

    def listar_transacoes_dia(self, data_dia: date = None) -> List[Dict]:
        """Lista transações do dia"""
        try:
            transacoes = self.transacao_repo.listar_transacoes_dia(data_dia)
            return [self._serializar_transacao(t) for t in transacoes]
        except Exception as e:
            raise ValueError(f"Erro ao listar transações: {str(e)}") from e

    def listar_transacoes_periodo(self, data_inicio: date,
                                 data_fim: date) -> List[Dict]:
        """Lista transações de um período"""
        try:
            transacoes = self.transacao_repo.listar_transacoes_periodo(
                data_inicio,
                data_fim
            )
            return [self._serializar_transacao(t) for t in transacoes]
        except Exception as e:
            raise ValueError(f"Erro ao listar transações: {str(e)}") from e

    def criar_fechamento(self, data_dia: date = None) -> Dict:
        """Cria um fechamento do dia"""
        try:
            fechamento = self.fechamento_repo.criar_fechamento(data_dia)
            return self._serializar_fechamento(fechamento)
        except Exception as e:
            raise ValueError(f"Erro ao criar fechamento: {str(e)}") from e

    def obter_fechamento(self, data_dia: date = None) -> Dict:
        """Obtém o fechamento de um dia"""
        try:
            fechamento = self.fechamento_repo.obter_fechamento(data_dia)
            return self._serializar_fechamento(fechamento)
        except Exception as e:
            raise ValueError(f"Erro ao obter fechamento: {str(e)}") from e

    def verificar_fechamento_existe(self, data_dia: date = None) -> bool:
        """Verifica se existe fechamento para o dia"""
        try:
            return self.fechamento_repo.verificar_fechamento_existe(data_dia)
        except Exception as e:
            raise ValueError(f"Erro ao verificar fechamento: {str(e)}") from e

    def listar_fechamentos(self, data_inicio: date = None,
                          data_fim: date = None) -> List[Dict]:
        """Lista fechamentos de um período"""
        try:
            fechamentos = self.fechamento_repo.listar_fechamentos(
                data_inicio,
                data_fim
            )
            return [self._serializar_fechamento(f) for f in fechamentos]
        except Exception as e:
            raise ValueError(f"Erro ao listar fechamentos: {str(e)}") from e

    @staticmethod
    def _serializar_transacao(transacao) -> Dict:
        """Converte uma transação em dicionário"""
        return {
            'id': transacao.id,
            'tipo': transacao.tipo,
            'categoria': transacao.categoria,
            'descricao': transacao.descricao,
            'valor': float(transacao.valor),
            'data_transacao': transacao.data_transacao.isoformat(),
            'observacoes': transacao.observacoes,
        }

    @staticmethod
    def _serializar_fechamento(fechamento) -> Dict:
        """Converte um fechamento em dicionário"""
        return {
            'id': fechamento.id,
            'data': fechamento.data.date().isoformat(),
            'total_vendas': float(fechamento.total_vendas),
            'total_despesas': float(fechamento.total_despesas),
            'total_entradas': float(fechamento.total_entradas),
            'saldo': float(fechamento.saldo),
            'quantidade_transacoes': fechamento.quantidade_transacoes,
            'observacoes': fechamento.observacoes,
        }
