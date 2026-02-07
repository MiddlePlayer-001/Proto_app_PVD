"""
Serviço de Vendas - Lógica de Negócio
"""
from src.models.venda_repository import VendaRepository
from src.models.produto_repository import ProdutoRepository
from src.database.models import Venda, ItemVenda
from src.utils.logger import log_info, log_error, log_venda
from decimal import Decimal
from typing import List, Dict
from datetime import date


class VendaService:
    """Serviço de gerenciamento de vendas"""

    def __init__(self):
        self.venda_repo = VendaRepository()
        self.produto_repo = ProdutoRepository()

    def iniciar_venda(self, forma_pagamento: str, observacoes: str = None) -> Dict:
        """Inicia uma nova venda"""
        try:
            venda = self.venda_repo.criar_venda(forma_pagamento, observacoes)
            return self._serializar_venda(venda)
        except Exception as e:
            raise ValueError(f"Erro ao iniciar venda: {str(e)}") from e

    def adicionar_item_carrinho(self, venda_id: int, codigo_produto: str,
                               quantidade: int) -> Dict:
        """Adiciona um item ao carrinho"""
        try:
            # Buscar produto por código
            produto = self.produto_repo.obter_por_codigo(codigo_produto)
            
            # Adicionar ao carrinho
            item = self.venda_repo.adicionar_item(venda_id, produto.id, quantidade)
            return self._serializar_item(item)
        except Exception as e:
            raise ValueError(f"Erro ao adicionar item: {str(e)}") from e

    def remover_item_carrinho(self, item_id: int) -> bool:
        """Remove um item do carrinho"""
        try:
            return self.venda_repo.remover_item(item_id)
        except Exception as e:
            raise ValueError(f"Erro ao remover item: {str(e)}") from e

    def atualizar_quantidade_item(self, item_id: int, nova_quantidade: int) -> Dict:
        """Atualiza a quantidade de um item"""
        try:
            item = self.venda_repo.atualizar_quantidade_item(item_id, nova_quantidade)
            return self._serializar_item(item)
        except Exception as e:
            raise ValueError(f"Erro ao atualizar quantidade: {str(e)}") from e

    def obter_carrinho(self, venda_id: int) -> Dict:
        """Obtém os itens do carrinho de uma venda"""
        try:
            venda = self.venda_repo.obter_venda(venda_id)
            itens = self.venda_repo.obter_itens_carrinho(venda_id)
            
            return {
                'venda_id': venda.id,
                'numero': venda.numero,
                'forma_pagamento': venda.forma_pagamento,
                'itens': [self._serializar_item(item) for item in itens],
                'subtotal': float(venda.total),
                'desconto': float(venda.desconto),
                'total': float(venda.total - venda.desconto),
            }
        except Exception as e:
            raise ValueError(f"Erro ao obter carrinho: {str(e)}") from e

    def aplicar_desconto(self, venda_id: int, desconto: float) -> Dict:
        """Aplica um desconto à venda"""
        try:
            venda = self.venda_repo.aplicar_desconto(
                venda_id,
                Decimal(str(desconto))
            )
            return self._serializar_venda(venda)
        except Exception as e:
            raise ValueError(f"Erro ao aplicar desconto: {str(e)}") from e

    def finalizar_venda(self, venda_id: int, valor_pago: float) -> Dict:
        """Finaliza a venda"""
        try:
            venda = self.venda_repo.finalizar_venda(
                venda_id,
                Decimal(str(valor_pago))
            )
            log_info(f"Venda #{venda.numero} finalizada com sucesso pelo serviço")
            return self._serializar_venda(venda)
        except Exception as e:
            log_error(f"Erro ao finalizar venda #{venda_id}: {str(e)}", exc_info=True)
            raise ValueError(f"Erro ao finalizar venda: {str(e)}") from e

    def cancelar_venda(self, venda_id: int) -> bool:
        """Cancela uma venda"""
        try:
            resultado = self.venda_repo.cancelar_venda(venda_id)
            log_info(f"Venda #{venda_id} cancelada com sucesso")
            return resultado
        except Exception as e:
            log_error(f"Erro ao cancelar venda #{venda_id}: {str(e)}", exc_info=True)
            raise ValueError(f"Erro ao cancelar venda: {str(e)}") from e

    def listar_vendas_dia(self, data_dia: date = None) -> List[Dict]:
        """Lista vendas do dia"""
        try:
            vendas = self.venda_repo.listar_vendas_dia(data_dia)
            return [self._serializar_venda(v) for v in vendas]
        except Exception as e:
            raise ValueError(f"Erro ao listar vendas: {str(e)}") from e

    def obter_total_vendas_dia(self, data_dia: date = None) -> float:
        """Obtém o total de vendas do dia"""
        try:
            total = self.venda_repo.total_vendas_dia(data_dia)
            return float(total)
        except Exception as e:
            raise ValueError(f"Erro ao obter total: {str(e)}") from e

    @staticmethod
    def _serializar_venda(venda: Venda) -> Dict:
        """Converte uma venda em dicionário"""
        return {
            'id': venda.id,
            'numero': venda.numero,
            'data_hora': venda.data_hora.isoformat(),
            'subtotal': float(venda.total),
            'desconto': float(venda.desconto),
            'total': float(venda.total - venda.desconto),
            'valor_pago': float(venda.valor_pago),
            'troco': float(venda.troco),
            'forma_pagamento': venda.forma_pagamento,
            'processada': bool(venda.processada),
            'observacoes': venda.observacoes,
        }

    @staticmethod
    def _serializar_item(item: ItemVenda) -> Dict:
        """Converte um item de venda em dicionário"""
        return {
            'id': item.id,
            'produto_id': item.produto.id,
            'codigo_produto': item.produto.codigo,
            'nome_produto': item.produto.nome,
            'quantidade': item.quantidade,
            'preco_unitario': float(item.preco_unitario),
            'subtotal': float(item.subtotal),
        }
