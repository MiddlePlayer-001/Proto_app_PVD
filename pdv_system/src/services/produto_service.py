"""
Serviço de Produtos - Lógica de Negócio
"""
from src.models.produto_repository import ProdutoRepository
from src.database.models import Produto
from src.utils.logger import log_info, log_error, log_debug
from decimal import Decimal
from typing import List, Dict


class ProdutoService:
    """Serviço de gerenciamento de produtos"""

    def __init__(self):
        self.repo = ProdutoRepository()

    def criar_produto(self, nome: str, codigo: str, preco_venda: float,
                     preco_custo: float = 0.0, estoque: int = 0,
                     descricao: str = None) -> Dict:
        """Cria um novo produto"""
        try:
            produto = self.repo.criar(
                nome=nome,
                codigo=codigo,
                preco_venda=Decimal(str(preco_venda)),
                preco_custo=Decimal(str(preco_custo)),
                estoque=estoque,
                descricao=descricao
            )
            log_info(f"Produto criado: {codigo} - {nome} (Estoque: {estoque})")
            return self._serializar_produto(produto)
        except ValueError as e:
            log_error(f"Erro ao criar produto {codigo}: {str(e)}", exc_info=True)
            raise ValueError(f"Erro ao criar produto: {str(e)}") from e

    def atualizar_produto(self, produto_id: int, **kwargs) -> Dict:
        """Atualiza um produto"""
        try:
            # Converter valores decimais se necessário
            if 'preco_venda' in kwargs:
                kwargs['preco_venda'] = Decimal(str(kwargs['preco_venda']))
            if 'preco_custo' in kwargs:
                kwargs['preco_custo'] = Decimal(str(kwargs['preco_custo']))
            
            produto = self.repo.atualizar(produto_id, **kwargs)
            return self._serializar_produto(produto)
        except ValueError as e:
            raise ValueError(f"Erro ao atualizar produto: {str(e)}") from e

    def obter_produto(self, produto_id: int) -> Dict:
        """Obtém um produto por ID"""
        try:
            produto = self.repo.obter_por_id(produto_id)
            return self._serializar_produto(produto)
        except ValueError as e:
            raise ValueError(f"Erro ao obter produto: {str(e)}") from e

    def obter_produto_por_codigo(self, codigo: str) -> Dict:
        """Obtém um produto por código"""
        try:
            produto = self.repo.obter_por_codigo(codigo)
            return self._serializar_produto(produto)
        except ValueError as e:
            raise ValueError(f"Erro ao obter produto: {str(e)}") from e

    def listar_produtos(self) -> List[Dict]:
        """Lista todos os produtos ativos"""
        produtos = self.repo.listar_ativos()
        return [self._serializar_produto(p) for p in produtos]

    def buscar_produtos(self, termo: str) -> List[Dict]:
        """Busca produtos por termo"""
        produtos = self.repo.buscar(termo)
        return [self._serializar_produto(p) for p in produtos]

    def deletar_produto(self, produto_id: int) -> bool:
        """Deleta um produto"""
        try:
            return self.repo.deletar(produto_id)
        except ValueError as e:
            raise ValueError(f"Erro ao deletar produto: {str(e)}") from e

    def ajustar_estoque(self, produto_id: int, quantidade: int) -> Dict:
        """Ajusta o estoque de um produto"""
        try:
            produto = self.repo.ajustar_estoque(produto_id, quantidade)
            operacao = "adicionado" if quantidade > 0 else "removido"
            log_info(f"Estoque ajustado para {produto.codigo}: {operacao} {abs(quantidade)} un. (Total: {produto.estoque})")
            return self._serializar_produto(produto)
        except ValueError as e:
            log_error(f"Erro ao ajustar estoque do produto {produto_id}: {str(e)}", exc_info=True)
            raise ValueError(f"Erro ao ajustar estoque: {str(e)}") from e

    def obter_valor_total_estoque(self) -> float:
        """Obtém o valor total em estoque"""
        valor = self.repo.obter_valor_estoque()
        return float(valor)

    @staticmethod
    def _serializar_produto(produto: Produto) -> Dict:
        """Converte um produto em dicionário"""
        return {
            'id': produto.id,
            'nome': produto.nome,
            'codigo': produto.codigo,
            'preco_custo': float(produto.preco_custo),
            'preco_venda': float(produto.preco_venda),
            'estoque': produto.estoque,
            'margem_lucro': float(produto.margem_lucro()),
            'ativo': bool(produto.ativo),
            'descricao': produto.descricao,
            'criado_em': produto.criado_em.isoformat() if produto.criado_em else None,
        }
