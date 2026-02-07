"""
Visualização de PDV (Ponto de Venda) em Flet
Layout: Esquerda (70%) - Carrinho | Direita (30%) - Busca + Total + Botões
"""
import flet as ft
from decimal import Decimal
from src.ui.styles import AppTheme
from src.services.venda_service import VendaService
from src.services.produto_service import ProdutoService
from src.services.financeiro_service import FinanceiroService


class PDVView:
    """Visualização do Ponto de Venda com Flet"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.venda_service = VendaService()
        self.produto_service = ProdutoService()
        self.financeiro_service = FinanceiroService()
        
        # Estado da venda atual
        self.venda_id = None
        self.itens_carrinho = {}  # {produto_id: {'produto': obj, 'quantidade': int}}
        self.total = Decimal('0.00')
        self.desconto = Decimal('0.00')
        
        # Componentes da UI
        self.campo_busca = None
        self.lista_carrinho = None
        self.label_total = None
        self.label_subtotal = None
        self.label_desconto = None
        self.btn_finalizar = None
        self.snackbar = None
        
    def criar_interface(self) -> ft.Container:
        """Cria a interface principal do PDV"""
        
        # Criar venda nova
        venda_response = self.venda_service.iniciar_venda(
            forma_pagamento="Dinheiro",
            observacoes="PDV"
        )
        self.venda_id = venda_response['id']
        
        # ═══════════════════════════════════════════════════════════
        # LADO ESQUERDO: CARRINHO (70%)
        # ═══════════════════════════════════════════════════════════
        
        self.lista_carrinho = ft.ListView(
            auto_scroll=True,
            expand=True,
            spacing=0,
            padding=0,
        )
        
        carrinho_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Text("CARRINHO DE COMPRAS", size=18, weight="bold", color=AppTheme.PRIMARY),
                        padding=10,
                        bgcolor=AppTheme.SURFACE_LIGHT,
                        border_radius=4,
                    ),
                    # Cabeçalho da tabela
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Text("ITEM", size=12, weight="bold", width=120),
                                ft.Text("QTD", size=12, weight="bold", width=50),
                                ft.Text("PREÇO", size=12, weight="bold", width=80),
                                ft.Text("TOTAL", size=12, weight="bold", width=100),
                                ft.Text("", size=12, width=40),  # Remove
                            ],
                            spacing=5,
                        ),
                        padding=10,
                        bgcolor=AppTheme.SURFACE,
                        border_radius=4,
                    ),
                    # Lista de itens
                    self.lista_carrinho,
                ],
                expand=True,
                spacing=0,
            ),
            padding=10,
            expand=True,
        )
        
        # ═══════════════════════════════════════════════════════════
        # LADO DIREITO: BUSCA + TOTAL + BOTÕES (30%)
        # ═══════════════════════════════════════════════════════════
        
        # Campo de busca
        self.campo_busca = ft.TextField(
            label="🔍 Código ou Nome do Produto",
            autofocus=True,
            min_lines=1,
            max_lines=1,
            border_color=AppTheme.PRIMARY,
            focused_border_color=AppTheme.ACCENT,
            on_submit=lambda e: self._buscar_e_adicionar_produto(e.control.value),
            width=300,
        )
        
        # Display de total
        self.label_subtotal = ft.Text(
            "R$ 0,00",
            size=14,
            color=AppTheme.TEXT_SECONDARY,
            weight="normal",
        )
        
        self.label_desconto = ft.Text(
            "R$ 0,00",
            size=14,
            color=AppTheme.WARNING,
            weight="normal",
        )
        
        self.label_total = ft.Text(
            "R$ 0,00",
            size=32,
            weight="bold",
            color=AppTheme.SUCCESS,
        )
        
        # Botões de ação
        btn_10_percent = self._criar_botao_desconto("10%", 10)
        btn_20_percent = self._criar_botao_desconto("20%", 20)
        btn_50_reais = self._criar_botao_desconto("R$50", -50)
        
        self.btn_finalizar = ft.ElevatedButton(
            content=ft.Text("FINALIZAR (F5)", size=18),
            bgcolor=AppTheme.SUCCESS,
            color="white",
            width=300,
            height=56,
            on_click=self._finalizar_venda,
        )
        
        btn_cancelar = ft.ElevatedButton(
            content=ft.Text("CANCELAR (ESC)", size=14),
            bgcolor=AppTheme.ERROR,
            color="white",
            width=300,
            height=48,
            on_click=self._cancelar_venda,
        )
        
        lado_direito = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(height=10),
                    ft.Text("BUSCA DE PRODUTO", size=14, weight="bold", color=AppTheme.PRIMARY),
                    self.campo_busca,
                    ft.Container(height=20),
                    
                    ft.Text("RESUMO DA VENDA", size=14, weight="bold", color=AppTheme.PRIMARY),
                    ft.Divider(height=1),
                    
                    # Subtotal
                    ft.Row(
                        controls=[
                            ft.Text("Subtotal:", size=12),
                            self.label_subtotal,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    
                    # Desconto
                    ft.Row(
                        controls=[
                            ft.Text("Desconto:", size=12),
                            self.label_desconto,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    
                    ft.Divider(height=1),
                    
                    # Total em destaque
                    ft.Row(
                        controls=[
                            ft.Text("TOTAL:", size=16, weight="bold"),
                            self.label_total,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    
                    ft.Container(height=20),
                    
                    # Botões de desconto
                    ft.Text("ATALHOS DE DESCONTO", size=12, weight="bold", color=AppTheme.PRIMARY),
                    ft.Row(
                        controls=[btn_10_percent, btn_20_percent, btn_50_reais],
                        spacing=5,
                        wrap=True,
                    ),
                    
                    ft.Container(height=20),
                    
                    # Botões principais
                    self.btn_finalizar,
                    btn_cancelar,
                ],
                spacing=5,
                expand=False,
            ),
            padding=10,
            border_radius=4,
            bgcolor=AppTheme.SURFACE,
        )
        
        # ═══════════════════════════════════════════════════════════
        # LAYOUT PRINCIPAL: ROW COM 70% ESQUERDA E 30% DIREITA
        # ═══════════════════════════════════════════════════════════
        
        self.snackbar = ft.SnackBar(ft.Text(""))
        
        conteudo = ft.Row(
            controls=[
                ft.Container(
                    content=carrinho_container,
                    expand=True,
                    flex=7,
                )
            ],
            expand=True,
            spacing=5,
        )
        
        # Adicionar lado direito responsivo
        if self.page.width and self.page.width > 1000:
            # Desktop: mostrar lado a lado
            conteudo.controls.append(
                ft.Container(
                    content=lado_direito,
                    expand=True,
                    flex=3,
                )
            )
        else:
            # Mobile: botões flutuantes
            conteudo = ft.Stack(
                controls=[
                    carrinho_container,
                    ft.Container(
                        content=lado_direito,
                        alignment=ft.alignment.bottom_right,
                        padding=10,
                    )
                ]
            )
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.AppBar(
                        title=ft.Text("💳 PDV - PONTO DE VENDA", size=20, weight="bold"),
                        center_title=True,
                        bgcolor=AppTheme.PRIMARY,
                        toolbar_height=60,
                    ),
                    conteudo,
                    self.snackbar,
                ],
                expand=True,
                spacing=0,
            ),
            expand=True,
            bgcolor=AppTheme.BACKGROUND,
        )
    
    def _buscar_e_adicionar_produto(self, codigo_ou_nome: str) -> None:
        """Busca produto e adiciona ao carrinho"""
        if not codigo_ou_nome.strip():
            return
        
        try:
            # Tentar buscar por código primeiro
            produtos = self.produto_service.buscar_produtos(codigo_ou_nome)
            
            if not produtos:
                self._mostrar_mensagem(f"❌ Produto '{codigo_ou_nome}' não encontrado!", AppTheme.ERROR)
                self.campo_busca.value = ""
                self.campo_busca.focus()
                self.page.update()
                return
            
            produto = produtos[0]  # Pegar o primeiro resultado
            
            # Verificar estoque
            if produto['estoque'] <= 0:
                self._mostrar_mensagem(f"❌ Produto '{produto['nome']}' sem estoque!", AppTheme.ERROR)
                self.campo_busca.value = ""
                self.campo_busca.focus()
                self.page.update()
                return
            
            # Adicionar ao carrinho (incrementar quantidade se já existe)
            produto_id = produto['id']
            
            if produto_id in self.itens_carrinho:
                # Incrementar quantidade
                quantidade_atual = self.itens_carrinho[produto_id]['quantidade']
                quantidade_maxima = produto['estoque']
                
                if quantidade_atual < quantidade_maxima:
                    self.itens_carrinho[produto_id]['quantidade'] += 1
                    self._mostrar_mensagem(f"✓ Quantidade aumentada: {self.itens_carrinho[produto_id]['quantidade']}", AppTheme.SUCCESS)
                else:
                    self._mostrar_mensagem(f"⚠️ Estoque máximo atingido ({quantidade_maxima})", AppTheme.WARNING)
            else:
                # Adicionar novo item
                self.itens_carrinho[produto_id] = {
                    'produto': produto,
                    'quantidade': 1,
                }
                self._mostrar_mensagem(f"✓ {produto['nome']} adicionado!", AppTheme.SUCCESS)
            
            # Atualizar visualização
            self._atualizar_carrinho()
            
            # Limpar campo e manter foco
            self.campo_busca.value = ""
            self.campo_busca.focus()
            self.page.update()
            
        except (ValueError, OSError, AttributeError, KeyError) as e:
            self._mostrar_mensagem(f"Erro ao adicionar: {str(e)}", AppTheme.ERROR)
            self.page.update()
    
    def _atualizar_carrinho(self) -> None:
        """Atualiza a visualização do carrinho"""
        self.lista_carrinho.controls.clear()
        
        subtotal = Decimal('0.00')
        
        for produto_id, item in self.itens_carrinho.items():
            produto = item['produto']
            quantidade = item['quantidade']
            preco = Decimal(str(produto['preco_venda']))
            total_item = preco * quantidade
            
            subtotal += total_item
            
            # Linha do item
            linha = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(
                            produto['nome'][:20],
                            size=11,
                            width=120,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                        ft.TextField(
                            value=str(quantidade),
                            width=50,
                            height=35,
                            text_style=ft.TextStyle(size=11),
                            border_radius=4,
                            on_change=lambda e, pid=produto_id: self._atualizar_quantidade(pid, e),
                        ),
                        ft.Text(
                            f"R$ {preco:.2f}",
                            size=11,
                            width=80,
                        ),
                        ft.Text(
                            f"R$ {total_item:.2f}",
                            size=11,
                            weight="bold",
                            width=100,
                        ),
                        ft.IconButton(
                            icon=ft.icons.CLOSE,
                            icon_size=16,
                            on_click=lambda e, pid=produto_id: self._remover_item(pid),
                            width=40,
                        ),
                    ],
                    spacing=5,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.padding.symmetric(vertical=5, horizontal=5),
                border_bottom=f"1px solid {AppTheme.SURFACE}",
            )
            
            self.lista_carrinho.controls.append(linha)
        
        # Atualizar totais
        self.total = subtotal - self.desconto
        self._atualizar_totais(subtotal)
    
    def _atualizar_quantidade(self, produto_id: int, event) -> None:
        """Atualiza quantidade de um item"""
        try:
            nova_quantidade = int(event.control.value)
            
            if nova_quantidade <= 0:
                self._remover_item(produto_id)
            else:
                estoque = self.itens_carrinho[produto_id]['produto']['estoque']
                if nova_quantidade <= estoque:
                    self.itens_carrinho[produto_id]['quantidade'] = nova_quantidade
                    self._atualizar_carrinho()
                else:
                    event.control.value = str(self.itens_carrinho[produto_id]['quantidade'])
                    self._mostrar_mensagem(f"⚠️ Estoque insuficiente (máx: {estoque})", AppTheme.WARNING)
                    self.page.update()
        except ValueError:
            pass
    
    def _remover_item(self, produto_id: int) -> None:
        """Remove item do carrinho"""
        if produto_id in self.itens_carrinho:
            nome = self.itens_carrinho[produto_id]['produto']['nome']
            del self.itens_carrinho[produto_id]
            self._mostrar_mensagem(f"✓ {nome} removido do carrinho", AppTheme.SUCCESS)
            self._atualizar_carrinho()
    
    def _criar_botao_desconto(self, texto: str, valor: int) -> ft.ElevatedButton:
        """Cria botão de atalho de desconto"""
        return ft.ElevatedButton(
            content=ft.Text(texto, size=11),
            width=90,
            height=40,
            bgcolor=AppTheme.ACCENT,
            color="white",
            on_click=lambda e, v=valor: self._aplicar_desconto_atalho(v),
        )
    
    def _aplicar_desconto_atalho(self, valor: int) -> None:
        """Aplica desconto via atalho"""
        if valor > 0:
            # Percentual
            desconto_novo = (self.total * Decimal(str(valor)) / 100)
        else:
            # Valor fixo
            desconto_novo = Decimal(str(-valor))
        
        # Não deixar desconto maior que o total
        if desconto_novo <= self.total:
            self.desconto = desconto_novo
            self._atualizar_carrinho()
        else:
            self._mostrar_mensagem("⚠️ Desconto não pode ser maior que o total!", AppTheme.WARNING)
            self.page.update()
    
    def _atualizar_totais(self, subtotal: Decimal) -> None:
        """Atualiza os labels de total"""
        self.label_subtotal.value = f"R$ {subtotal:.2f}"
        self.label_desconto.value = f"R$ {self.desconto:.2f}" if self.desconto > 0 else "R$ 0,00"
        self.label_total.value = f"R$ {self.total:.2f}"
        self.page.update()
    
    def _finalizar_venda(self, _event) -> None:
        """Finaliza a venda e salva no banco"""
        if not self.itens_carrinho:
            self._mostrar_mensagem("⚠️ Carrinho vazio! Adicione produtos antes de finalizar.", AppTheme.WARNING)
            self.page.update()
            return
        
        try:
            # Desabilitar botão durante processamento
            self.btn_finalizar.disabled = True
            self.page.update()
            
            # Adicionar itens à venda via serviço
            for _produto_id, item in self.itens_carrinho.items():
                produto = item['produto']
                quantidade = item['quantidade']
                
                self.venda_service.adicionar_item_carrinho(
                    self.venda_id,
                    produto['codigo'],
                    quantidade
                )
            
            # Aplicar desconto se houver
            if self.desconto > 0:
                self.venda_service.aplicar_desconto(self.venda_id, float(self.desconto))
            
            # Finalizar venda
            venda_finalizada = self.venda_service.finalizar_venda(
                self.venda_id,
                float(self.total)
            )
            
            # Simular impressão
            self._simular_impressao(venda_finalizada)
            
            # Mostrar mensagem de sucesso
            self._mostrar_mensagem(
                f"✅ Venda #{venda_finalizada['numero']} finalizada com sucesso!",
                AppTheme.SUCCESS
            )
            
            # Limpar carrinho
            self.itens_carrinho.clear()
            self.desconto = Decimal('0.00')
            
            # Iniciar nova venda
            venda_response = self.venda_service.iniciar_venda(
                forma_pagamento="Dinheiro",
                observacoes="PDV"
            )
            self.venda_id = venda_response['id']
            
            # Atualizar UI
            self._atualizar_carrinho()
            self.campo_busca.value = ""
            self.campo_busca.focus()
            
        except (ValueError, OSError, RuntimeError, KeyError) as e:
            self._mostrar_mensagem(f"Erro ao finalizar venda: {str(e)}", AppTheme.ERROR)
        
        finally:
            self.btn_finalizar.disabled = False
            self.page.update()
    
    def _cancelar_venda(self, _event) -> None:
        """Cancela a venda atual"""
        if not self.itens_carrinho:
            return
        
        # Limpar carrinho
        self.itens_carrinho.clear()
        self.desconto = Decimal('0.00')
        
        # Iniciar nova venda
        try:
            self.venda_service.cancelar_venda(self.venda_id)
        except (OSError, ValueError, RuntimeError):
            pass  # Ignorar se falhar
        
        venda_response = self.venda_service.iniciar_venda(
            forma_pagamento="Dinheiro",
            observacoes="PDV"
        )
        self.venda_id = venda_response['id']
        
        # Atualizar UI
        self._atualizar_carrinho()
        self.campo_busca.value = ""
        self.campo_busca.focus()
        
        self._mostrar_mensagem("✓ Venda cancelada. Nova venda iniciada.", AppTheme.SUCCESS)
        self.page.update()
    
    def _simular_impressao(self, venda: dict) -> None:
        """Simula impressão de cupom"""
        cupom = f"""
╔════════════════════════════════════════════════════════════╗
║                      PDV - CUPOM DE VENDA                 ║
╚════════════════════════════════════════════════════════════╝

Venda Nº: {venda['numero']}
Data/Hora: {venda['data_hora']}
────────────────────────────────────────────────────────────

ITENS:
"""
        # Adicionar itens
        total_itens = Decimal('0.00')
        for _produto_id, item in self.itens_carrinho.items():
            produto = item['produto']
            quantidade = item['quantidade']
            preco = Decimal(str(produto['preco_venda']))
            subtotal_item = preco * quantidade
            
            cupom += f"\n{produto['nome'][:30]:<30}"
            cupom += f"\n  {quantidade:>2} x R$ {preco:.2f} = R$ {subtotal_item:.2f}"
            
            total_itens += subtotal_item
        
        cupom += f"""
────────────────────────────────────────────────────────────
Subtotal:                              R$ {float(total_itens):.2f}
"""
        
        if self.desconto > 0:
            cupom += f"Desconto:                              R$ {float(self.desconto):.2f}\n"
        
        cupom += f"""TOTAL:                                 R$ {float(self.total):.2f}
────────────────────────────────────────────────────────────

Forma de Pagamento: {venda['forma_pagamento']}
Valor Pago: R$ {float(self.total):.2f}

╔════════════════════════════════════════════════════════════╗
║                     OBRIGADO PELA COMPRA!                 ║
║                      VOLTE SEMPRE! 👋                      ║
╚════════════════════════════════════════════════════════════╝
"""
        
        # Imprimir no console (simulação)
        print(cupom)
        
        # Em produção, enviar para impressora térmica via serial/USB
    
    def _mostrar_mensagem(self, texto: str, cor: str = AppTheme.PRIMARY) -> None:
        """Mostra mensagem de feedback ao usuário"""
        self.snackbar.content = ft.Text(texto, color="white")
        self.snackbar.bgcolor = cor
        self.snackbar.open = True
        self.page.update()
