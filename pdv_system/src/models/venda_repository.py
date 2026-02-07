"""
Repositório de Vendas - Camada de Acesso aos Dados
"""
from src.database.models import Venda, ItemVenda, Produto, Transacao
from src.database.connection import get_db
from src.utils.logger import log_info, log_error, log_debug, log_venda
from decimal import Decimal
from datetime import datetime, date


class VendaRepository:
    """Gerencia operações de Vendas e Carrinho"""

    @staticmethod
    def obter_proximo_numero() -> int:
        """Obtém o próximo número de venda sequencial"""
        ultima_venda = Venda.select().order_by(Venda.numero.desc()).first()
        return (ultima_venda.numero + 1) if ultima_venda else 1

    @staticmethod
    def criar_venda(forma_pagamento: str, observacoes: str = None) -> Venda:
        """Cria uma nova venda vazia"""
        try:
            numero = VendaRepository.obter_proximo_numero()
            
            venda = Venda.create(
                numero=numero,
                data_hora=datetime.now(),
                forma_pagamento=forma_pagamento,
                observacoes=observacoes,
                processada=0  # 0 = em andamento, 1 = finalizada
            )
            log_venda(numero, "INICIADA", f"Forma: {forma_pagamento}")
            return venda
        except Exception as e:
            log_error(f"Erro ao criar venda: {str(e)}", exc_info=True)
            raise

    @staticmethod
    def adicionar_item(venda_id: int, produto_id: int, quantidade: int) -> ItemVenda:
        """Adiciona um item ao carrinho da venda"""
        try:
            venda = Venda.get_by_id(venda_id)
            produto = Produto.get_by_id(produto_id)
            
            if quantidade <= 0:
                raise ValueError("Quantidade deve ser maior que zero")
            
            if produto.estoque < quantidade:
                log_error(
                    f"Estoque insuficiente ao adicionar {produto.codigo}",
                    estoque_disponivel=produto.estoque,
                    quantidade_solicitada=quantidade
                )
                raise ValueError(f"Estoque insuficiente. Disponível: {produto.estoque}")
            
            # Verificar se o item já existe no carrinho
            item_existente = ItemVenda.select().where(
                (ItemVenda.venda == venda) &
                (ItemVenda.produto == produto)
            ).first()
            
            if item_existente:
                # Atualizar quantidade
                item_existente.quantidade += quantidade
                item_existente.subtotal = (
                    item_existente.quantidade * item_existente.preco_unitario
                )
                item_existente.save()
                item = item_existente
                log_debug(f"Item atualizado na venda #{venda.numero}: {produto.codigo} x {quantidade}")
            else:
                # Criar novo item
                item = ItemVenda.create(
                    venda=venda,
                    produto=produto,
                    quantidade=quantidade,
                    preco_unitario=produto.preco_venda,
                    subtotal=quantidade * produto.preco_venda
                )
                log_debug(f"Item adicionado à venda #{venda.numero}: {produto.codigo} x {quantidade}")
            
            # Atualizar total da venda
            VendaRepository._atualizar_total_venda(venda_id)
            return item
            
        except (Venda.DoesNotExist, Produto.DoesNotExist) as e:
            log_error(f"Venda ou Produto não encontrado ao adicionar item: {str(e)}", exc_info=True)
            raise ValueError(f"Venda ou Produto não encontrado: {str(e)}") from e

    @staticmethod
    def remover_item(item_id: int) -> bool:
        """Remove um item do carrinho"""
        try:
            item = ItemVenda.get_by_id(item_id)
            venda_id = item.venda_id
            item.delete_instance()
            VendaRepository._atualizar_total_venda(venda_id)
            return True
        except ItemVenda.DoesNotExist as exc:
            raise ValueError(f"Item ID {item_id} não encontrado") from exc

    @staticmethod
    def atualizar_quantidade_item(item_id: int, nova_quantidade: int) -> ItemVenda:
        """Atualiza a quantidade de um item"""
        try:
            if nova_quantidade <= 0:
                return VendaRepository.remover_item(item_id)
            
            item = ItemVenda.get_by_id(item_id)
            
            # Validar estoque
            if item.produto.estoque < nova_quantidade:
                raise ValueError(
                    f"Estoque insuficiente. Disponível: {item.produto.estoque}"
                )
            
            item.quantidade = nova_quantidade
            item.subtotal = nova_quantidade * item.preco_unitario
            item.save()
            
            VendaRepository._atualizar_total_venda(item.venda_id)
            return item
        except ItemVenda.DoesNotExist as exc:
            raise ValueError(f"Item ID {item_id} não encontrado") from exc

    @staticmethod
    def obter_itens_carrinho(venda_id: int) -> list:
        """Obtém todos os itens de uma venda"""
        return list(ItemVenda.select().where(ItemVenda.venda_id == venda_id))

    @staticmethod
    def _atualizar_total_venda(venda_id: int):
        """Atualiza o total da venda somando os itens"""
        try:
            venda = Venda.get_by_id(venda_id)
            itens = ItemVenda.select().where(ItemVenda.venda == venda)
            
            total = sum(Decimal(str(item.subtotal)) for item in itens)
            venda.total = total
            venda.save()
        except Venda.DoesNotExist:
            pass

    @staticmethod
    def aplicar_desconto(venda_id: int, desconto: Decimal) -> Venda:
        """Aplica um desconto à venda"""
        try:
            venda = Venda.get_by_id(venda_id)
            
            if desconto < 0:
                raise ValueError("Desconto não pode ser negativo")
            
            if desconto > venda.total:
                raise ValueError("Desconto não pode ser maior que o total")
            
            venda.desconto = desconto
            venda.save()
            return venda
        except Venda.DoesNotExist as exc:
            raise ValueError(f"Venda ID {venda_id} não encontrada") from exc

    @staticmethod
    def finalizar_venda(venda_id: int, valor_pago: Decimal) -> Venda:
        """Finaliza a venda e calcula o troco com transação ACID"""
        db = get_db()
        
        try:
            with db.atomic():  # Transação ACID - tudo ou nada
                venda = Venda.get_by_id(venda_id)
                
                total_final = venda.total - venda.desconto
                
                if valor_pago < total_final:
                    log_venda(venda.numero, "ERRO - VALOR INSUFICIENTE", 
                             f"Valor: {float(valor_pago):.2f}, Total: {float(total_final):.2f}")
                    raise ValueError(
                        f"Valor pago insuficiente. Total: R$ {float(total_final):.2f}"
                    )
                
                troco = valor_pago - total_final
                
                # 1. Atualizar venda
                venda.valor_pago = valor_pago
                venda.troco = troco
                venda.processada = 1
                venda.save()
                log_debug(f"Venda #{venda.numero} marcada como processada")
                
                # 2. Registrar transação de venda
                total_venda = venda.total - venda.desconto
                Transacao.create(
                    tipo='ENTRADA',
                    categoria='VENDA',
                    descricao=f'Venda #{venda.numero}',
                    valor=total_venda,
                    data_transacao=venda.data_hora,
                    venda=venda
                )
                log_debug(f"Transação financeira registrada para venda #{venda.numero}")
                
                # 3. Descontar estoque
                for item in venda.itens:
                    quantidade_anterior = item.produto.estoque
                    item.produto.estoque -= item.quantidade
                    item.produto.save()
                    log_debug(
                        f"Estoque atualizado: {item.produto.codigo} "
                        f"{quantidade_anterior} -> {item.produto.estoque}"
                    )
                
                log_venda(venda.numero, "FINALIZADA", 
                         f"Total: R$ {float(total_venda):.2f}, Troco: R$ {float(troco):.2f}")
                return venda
                
        except Venda.DoesNotExist as exc:
            log_error(f"Venda ID {venda_id} não encontrada ao finalizar", exc_info=True)
            raise ValueError(f"Venda ID {venda_id} não encontrada") from exc
        except Exception as e:
            log_error(f"Erro ao finalizar venda #{venda_id}: {str(e)}", exc_info=True)
            raise

    @staticmethod
    def obter_venda(venda_id: int) -> Venda:
        """Obtém uma venda específica"""
        try:
            return Venda.get_by_id(venda_id)
        except Venda.DoesNotExist as exc:
            raise ValueError(f"Venda ID {venda_id} não encontrada") from exc

    @staticmethod
    def listar_vendas_dia(data_dia: date = None) -> list:
        """Lista todas as vendas de um dia específico"""
        if data_dia is None:
            data_dia = date.today()
        
        inicio = datetime.combine(data_dia, datetime.min.time())
        fim = datetime.combine(data_dia, datetime.max.time())
        
        return list(
            Venda.select()
            .where(
                (Venda.data_hora >= inicio) &
                (Venda.data_hora <= fim) &
                (Venda.processada == 1)
            )
            .order_by(Venda.data_hora.desc())
        )

    @staticmethod
    def total_vendas_dia(data_dia: date = None) -> Decimal:
        """Calcula o total de vendas do dia"""
        vendas = VendaRepository.listar_vendas_dia(data_dia)
        total = sum(
            (v.total - v.desconto) for v in vendas
        )
        return Decimal(str(total))

    @staticmethod
    def cancelar_venda(venda_id: int) -> bool:
        """Cancela uma venda não processada"""
        try:
            venda = Venda.get_by_id(venda_id)
            
            if venda.processada == 1:
                log_error(f"Tentativa de cancelar venda já processada: #{venda.numero}")
                raise ValueError("Não é possível cancelar uma venda finalizada")
            
            # Remover itens do carrinho
            ItemVenda.delete().where(ItemVenda.venda == venda).execute()
            venda.delete_instance()
            log_venda(venda.numero, "CANCELADA", "Venda removida do sistema")
            return True
        except Venda.DoesNotExist as exc:
            log_error(f"Venda ID {venda_id} não encontrada ao cancelar", exc_info=True)
            raise ValueError(f"Venda ID {venda_id} não encontrada") from exc
