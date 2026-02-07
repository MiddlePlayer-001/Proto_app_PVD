"""
Serviço de Relatórios e Cupom Fiscal
"""
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm, mm
from reportlab.pdfgen import canvas
from datetime import datetime, date
from decimal import Decimal
from src.database.models import Venda


class RelatorioService:
    """Serviço de geração de relatórios"""

    LARGURA_58MM = 58  # Papel térmico padrão de 58mm
    LARGURA_80MM = 80  # Papel térmico de 80mm

    @staticmethod
    def gerar_cupom_venda(venda_id: int, nome_loja: str = "Minha Loja",
                         largura_mm: int = 58) -> BytesIO:
        """
        Gera um cupom em PDF simples (não-fiscal) com ReportLab
        
        Args:
            venda_id: ID da venda
            nome_loja: Nome da loja
            largura_mm: Largura do papel (58 ou 80mm)
        
        Returns:
            BytesIO com conteúdo do PDF
        """
        try:
            venda = Venda.get_by_id(venda_id)
            
            # Dimensões do papel
            if largura_mm == 80:
                largura = 80 * mm
            else:
                largura = 58 * mm
            
            altura = 297 * mm  # Altura padrão A4
            
            # Criar buffer PDF
            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=(largura, altura))
            
            # Fonte padrão
            c.setFont("Helvetica-Bold", 10)
            x = largura / 2
            y = altura - 1 * cm
            
            # Cabeçalho
            c.drawCentredString(x, y, nome_loja)
            y -= 0.5 * cm
            
            c.setFont("Helvetica", 8)
            c.drawCentredString(x, y, "COMPROVANTE DE VENDA")
            y -= 0.4 * cm
            
            # Linha separadora
            c.setLineWidth(0.5)
            c.line(0.3 * cm, y, largura - 0.3 * cm, y)
            y -= 0.3 * cm
            
            # Informações da venda
            c.setFont("Helvetica", 8)
            c.drawString(0.3 * cm, y, f"Venda: #{venda.numero}")
            y -= 0.3 * cm
            
            data_str = venda.data_hora.strftime("%d/%m/%Y %H:%M:%S")
            c.drawString(0.3 * cm, y, f"Data: {data_str}")
            y -= 0.4 * cm
            
            # Linha separadora
            c.setLineWidth(0.5)
            c.line(0.3 * cm, y, largura - 0.3 * cm, y)
            y -= 0.3 * cm
            
            # Itens da venda
            c.setFont("Helvetica-Bold", 8)
            c.drawString(0.3 * cm, y, "Descrição")
            c.drawRightString(largura - 0.3 * cm, y, "Valor")
            y -= 0.3 * cm
            
            c.setLineWidth(0.3)
            c.line(0.3 * cm, y, largura - 0.3 * cm, y)
            y -= 0.2 * cm
            
            c.setFont("Helvetica", 7)
            
            for item in venda.itens:
                # Descrição do produto
                desc = f"{item.produto.codigo} - {item.produto.nome}"
                desc_truncado = desc[:30] if len(desc) > 30 else desc
                c.drawString(0.3 * cm, y, desc_truncado)
                y -= 0.25 * cm
                
                # Quantidade e preço
                qtd_preco = f"{item.quantidade}x R${float(item.preco_unitario):.2f}"
                c.drawRightString(largura - 0.3 * cm, y, qtd_preco)
                y -= 0.25 * cm
                
                # Subtotal
                subtotal = f"Subtotal: R${float(item.subtotal):.2f}"
                c.drawRightString(largura - 0.3 * cm, y, subtotal)
                y -= 0.3 * cm
            
            # Linha separadora
            c.setLineWidth(0.5)
            c.line(0.3 * cm, y, largura - 0.3 * cm, y)
            y -= 0.3 * cm
            
            # Totais
            c.setFont("Helvetica-Bold", 9)
            
            if venda.desconto > 0:
                desconto_str = f"Desconto: -R${float(venda.desconto):.2f}"
                c.drawRightString(largura - 0.3 * cm, y, desconto_str)
                y -= 0.35 * cm
            
            total_str = f"TOTAL: R${float(venda.total - venda.desconto):.2f}"
            c.drawRightString(largura - 0.3 * cm, y, total_str)
            y -= 0.4 * cm
            
            # Pagamento
            c.setFont("Helvetica", 8)
            pagto_str = f"Pagamento: {venda.forma_pagamento}"
            c.drawString(0.3 * cm, y, pagto_str)
            y -= 0.3 * cm
            
            valor_pago_str = f"Valor Pago: R${float(venda.valor_pago):.2f}"
            c.drawString(0.3 * cm, y, valor_pago_str)
            y -= 0.3 * cm
            
            if venda.troco > 0:
                troco_str = f"Troco: R${float(venda.troco):.2f}"
                c.drawString(0.3 * cm, y, troco_str)
            
            y -= 0.5 * cm
            
            # Rodapé
            c.setLineWidth(0.5)
            c.line(0.3 * cm, y, largura - 0.3 * cm, y)
            y -= 0.3 * cm
            
            c.setFont("Helvetica-Oblique", 7)
            c.drawCentredString(x, y, "Obrigado pela compra!")
            y -= 0.3 * cm
            c.drawCentredString(x, y, f"Emitido: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            
            # Finalizar PDF
            c.save()
            buffer.seek(0)
            return buffer
            
        except Exception as e:
            raise ValueError(f"Erro ao gerar cupom: {str(e)}") from e

    @staticmethod
    def gerar_relatorio_dia(data_dia: date = None, nome_loja: str = "Minha Loja") -> BytesIO:
        """
        Gera um relatório diário em PDF
        
        Args:
            data_dia: Data do relatório (padrão: hoje)
            nome_loja: Nome da loja
        
        Returns:
            BytesIO com conteúdo do PDF
        """
        if data_dia is None:
            data_dia = date.today()
        
        try:
            inicio = datetime.combine(data_dia, datetime.min.time())
            fim = datetime.combine(data_dia, datetime.max.time())
            
            vendas = Venda.select().where(
                (Venda.processada == 1) &
                (Venda.data_hora >= inicio) &
                (Venda.data_hora <= fim)
            ).order_by(Venda.numero)
            
            # Criar PDF
            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            
            # Cabeçalho
            c.setFont("Helvetica-Bold", 16)
            c.drawString(1 * cm, 27 * cm, nome_loja)
            
            c.setFont("Helvetica", 10)
            c.drawString(1 * cm, 26.2 * cm, f"Relatório de Vendas - {data_dia.strftime('%d/%m/%Y')}")
            
            # Dados das vendas
            y = 25 * cm
            c.setFont("Helvetica-Bold", 10)
            c.drawString(1 * cm, y, "Venda")
            c.drawString(3 * cm, y, "Hora")
            c.drawString(5 * cm, y, "Itens")
            c.drawString(7 * cm, y, "Total")
            c.drawString(9 * cm, y, "Desconto")
            c.drawString(11 * cm, y, "Líquido")
            c.drawString(13 * cm, y, "Forma")
            
            y -= 0.5 * cm
            c.setLineWidth(0.5)
            c.line(1 * cm, y, 20 * cm, y)
            y -= 0.3 * cm
            
            c.setFont("Helvetica", 9)
            
            total_vendas = Decimal('0')
            total_descontos = Decimal('0')
            total_liquido = Decimal('0')
            
            for venda in vendas:
                numero_str = f"#{venda.numero}"
                hora_str = venda.data_hora.strftime("%H:%M")
                qtd_itens = len(list(venda.itens))
                
                c.drawString(1 * cm, y, numero_str)
                c.drawString(3 * cm, y, hora_str)
                c.drawString(5 * cm, y, str(qtd_itens))
                c.drawRightString(7 * cm, y, f"R${float(venda.total):.2f}")
                c.drawRightString(9 * cm, y, f"-R${float(venda.desconto):.2f}")
                c.drawRightString(11 * cm, y, f"R${float(venda.total - venda.desconto):.2f}")
                c.drawString(13 * cm, y, venda.forma_pagamento)
                
                total_vendas += venda.total
                total_descontos += venda.desconto
                total_liquido += (venda.total - venda.desconto)
                
                y -= 0.35 * cm
            
            # Totalizadores
            y -= 0.3 * cm
            c.setLineWidth(0.5)
            c.line(1 * cm, y, 20 * cm, y)
            y -= 0.3 * cm
            
            c.setFont("Helvetica-Bold", 10)
            c.drawRightString(7 * cm, y, f"TOTAL: R${float(total_vendas):.2f}")
            c.drawRightString(9 * cm, y, f"-R${float(total_descontos):.2f}")
            c.drawRightString(11 * cm, y, f"R${float(total_liquido):.2f}")
            
            # Resumo
            y -= 0.7 * cm
            c.setFont("Helvetica", 10)
            c.drawString(1 * cm, y, f"Quantidade de vendas: {len(list(vendas))}")
            y -= 0.35 * cm
            c.drawString(1 * cm, y, f"Valor médio por venda: R${float(total_liquido / len(list(vendas))):.2f}" if len(list(vendas)) > 0 else "")
            
            c.save()
            buffer.seek(0)
            return buffer
            
        except Exception as e:
            raise ValueError(f"Erro ao gerar relatório: {str(e)}") from e
