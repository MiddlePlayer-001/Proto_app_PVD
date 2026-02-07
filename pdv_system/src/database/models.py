"""
Modelos de banco de dados usando Peewee ORM
"""
from peewee import (
    Model, CharField, DecimalField, IntegerField, 
    DateTimeField, ForeignKeyField
)
from datetime import datetime
from src.database.connection import get_db

db = get_db()


class BaseModel(Model):
    """Modelo base para todas as tabelas"""
    class Meta:
        database = db


class Produto(BaseModel):
    """Modelo de Produtos - CRUD Completo"""
    nome = CharField(max_length=200, unique=True, index=True)
    codigo = CharField(max_length=50, unique=True, index=True)
    preco_custo = DecimalField(max_digits=10, decimal_places=2, default=0.00)
    preco_venda = DecimalField(max_digits=10, decimal_places=2)
    estoque = IntegerField(default=0)
    ativo = IntegerField(default=1)  # 0 = inativo, 1 = ativo
    descricao = CharField(max_length=500, null=True)
    criado_em = DateTimeField(default=datetime.now)
    atualizado_em = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'produtos'
        indexes = (
            (('codigo',), False),
            (('nome',), False),
            (('ativo',), False),
        )

    def __str__(self):
        return f"{self.codigo} - {self.nome}"

    def margem_lucro(self):
        """Calcula a margem de lucro em percentual"""
        if self.preco_custo == 0:
            return 0
        return ((self.preco_venda - self.preco_custo) / self.preco_custo) * 100


class Venda(BaseModel):
    """Modelo de Vendas"""
    numero = IntegerField(unique=True)  # ID da venda para rastreamento
    data_hora = DateTimeField(default=datetime.now, index=True)
    total = DecimalField(max_digits=10, decimal_places=2, default=0.00)
    desconto = DecimalField(max_digits=10, decimal_places=2, default=0.00)
    valor_pago = DecimalField(max_digits=10, decimal_places=2, default=0.00)
    troco = DecimalField(max_digits=10, decimal_places=2, default=0.00)
    forma_pagamento = CharField(max_length=50)  # Dinheiro, Cartão, PIX
    observacoes = CharField(max_length=500, null=True)
    processada = IntegerField(default=1)  # Marcar como finalizada

    class Meta:
        table_name = 'vendas'
        indexes = (
            (('data_hora',), False),
            (('numero',), True),
        )

    def __str__(self):
        return f"Venda #{self.numero} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"


class ItemVenda(BaseModel):
    """Modelo de Itens de Venda (Carrinho)"""
    venda = ForeignKeyField(Venda, backref='itens')
    produto = ForeignKeyField(Produto, backref='itens_venda')
    quantidade = IntegerField()
    preco_unitario = DecimalField(max_digits=10, decimal_places=2)
    subtotal = DecimalField(max_digits=10, decimal_places=2)  # quantidade * preco_unitario

    class Meta:
        table_name = 'itens_venda'
        indexes = (
            (('venda',), False),
            (('produto',), False),
        )

    def __str__(self):
        return f"{self.produto.codigo} x {self.quantidade}"


class Transacao(BaseModel):
    """Modelo Unificado de Transações Financeiras"""
    TIPO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SAIDA', 'Saída'),
    ]
    
    CATEGORIA_CHOICES = [
        ('VENDA', 'Venda'),
        ('DESPESA', 'Despesa'),
        ('DEVOLUCAO', 'Devolução'),
        ('AJUSTE', 'Ajuste'),
    ]

    tipo = CharField(max_length=10, choices=TIPO_CHOICES)  # ENTRADA ou SAIDA
    categoria = CharField(max_length=20, choices=CATEGORIA_CHOICES)
    descricao = CharField(max_length=300)
    valor = DecimalField(max_digits=10, decimal_places=2)
    data_transacao = DateTimeField(index=True)
    data_criacao = DateTimeField(default=datetime.now)
    venda = ForeignKeyField(Venda, null=True, backref='transacoes')
    observacoes = CharField(max_length=500, null=True)

    class Meta:
        table_name = 'transacoes'
        indexes = (
            (('data_transacao',), False),
            (('tipo',), False),
            (('categoria',), False),
        )

    def __str__(self):
        return f"{self.tipo} - {self.categoria}: R$ {float(self.valor):.2f}"


class FechamentoDia(BaseModel):
    """Modelo de Fechamento Diário"""
    data = DateTimeField(unique=True, index=True)
    total_vendas = DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_despesas = DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_entradas = DecimalField(max_digits=10, decimal_places=2, default=0.00)
    saldo = DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantidade_transacoes = IntegerField(default=0)
    observacoes = CharField(max_length=500, null=True)
    criado_em = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'fechamento_dia'
        indexes = (
            (('data',), True),
        )

    def __str__(self):
        return f"Fechamento {self.data.strftime('%d/%m/%Y')}"
