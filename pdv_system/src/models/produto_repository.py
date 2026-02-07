"""
Repositório de Produtos - Camada de Acesso aos Dados
"""
from src.database.models import Produto
from decimal import Decimal
from datetime import datetime


class ProdutoRepository:
    """Gerencia operações CRUD de Produtos"""

    @staticmethod
    def criar(nome: str, codigo: str, preco_venda: Decimal, 
              preco_custo: Decimal = Decimal('0.00'), estoque: int = 0,
              descricao: str = None) -> Produto:
        """Cria um novo produto"""
        try:
            produto = Produto.create(
                nome=nome,
                codigo=codigo,
                preco_venda=preco_venda,
                preco_custo=preco_custo,
                estoque=estoque,
                descricao=descricao,
                ativo=1
            )
            return produto
        except Exception as e:
            raise ValueError(f"Erro ao criar produto: {str(e)}") from e

    @staticmethod
    def atualizar(produto_id: int, **kwargs) -> Produto:
        """Atualiza um produto existente"""
        try:
            produto = Produto.get_by_id(produto_id)
            
            # Campos permitidos para atualização
            campos_permitidos = [
                'nome', 'codigo', 'preco_custo', 'preco_venda', 
                'estoque', 'descricao', 'ativo'
            ]
            
            for campo, valor in kwargs.items():
                if campo in campos_permitidos:
                    setattr(produto, campo, valor)
            
            produto.atualizado_em = datetime.now()
            produto.save()
            return produto
        except Produto.DoesNotExist as exc:
            raise ValueError(f"Produto ID {produto_id} não encontrado") from exc
        except Exception as e:
            raise ValueError(f"Erro ao atualizar produto: {str(e)}") from e

    @staticmethod
    def obter_por_id(produto_id: int) -> Produto:
        """Obtém um produto por ID"""
        try:
            return Produto.get_by_id(produto_id)
        except Produto.DoesNotExist as exc:
            raise ValueError(f"Produto ID {produto_id} não encontrado") from exc

    @staticmethod
    def obter_por_codigo(codigo: str) -> Produto:
        """Obtém um produto por código"""
        try:
            return Produto.get(Produto.codigo == codigo)
        except Produto.DoesNotExist as exc:
            raise ValueError(f"Produto com código '{codigo}' não encontrado") from exc

    @staticmethod
    def listar_ativos() -> list:
        """Lista todos os produtos ativos"""
        return list(Produto.select().where(Produto.ativo == 1).order_by(Produto.nome))

    @staticmethod
    def listar_todos() -> list:
        """Lista todos os produtos (ativos e inativos)"""
        return list(Produto.select().order_by(Produto.nome))

    @staticmethod
    def buscar(termo: str) -> list:
        """Busca produtos por nome ou código"""
        query = (Produto.select()
                 .where(
                    (Produto.nome.contains(termo)) |
                    (Produto.codigo.contains(termo))
                 )
                 .where(Produto.ativo == 1)
                 .order_by(Produto.nome))
        return list(query)

    @staticmethod
    def deletar(produto_id: int) -> bool:
        """Deleta um produto (marca como inativo)"""
        try:
            produto = Produto.get_by_id(produto_id)
            produto.ativo = 0
            produto.atualizado_em = datetime.now()
            produto.save()
            return True
        except Produto.DoesNotExist as exc:
            raise ValueError(f"Produto ID {produto_id} não encontrado") from exc

    @staticmethod
    def ajustar_estoque(produto_id: int, quantidade: int) -> Produto:
        """Ajusta o estoque de um produto"""
        try:
            produto = Produto.get_by_id(produto_id)
            novo_estoque = produto.estoque + quantidade
            
            if novo_estoque < 0:
                raise ValueError("Estoque não pode ser negativo")
            
            produto.estoque = novo_estoque
            produto.atualizado_em = datetime.now()
            produto.save()
            return produto
        except Produto.DoesNotExist as exc:
            raise ValueError(f"Produto ID {produto_id} não encontrado") from exc

    @staticmethod
    def obter_estoque(produto_id: int) -> int:
        """Obtém o estoque atual de um produto"""
        try:
            produto = Produto.get_by_id(produto_id)
            return produto.estoque
        except Produto.DoesNotExist as exc:
            raise ValueError(f"Produto ID {produto_id} não encontrado") from exc

    @staticmethod
    def obter_valor_estoque() -> Decimal:
        """Calcula o valor total em estoque (preço de custo)"""
        produtos = Produto.select()
        valor_total = sum(
            Decimal(str(p.estoque)) * p.preco_custo 
            for p in produtos
        )
        return valor_total
