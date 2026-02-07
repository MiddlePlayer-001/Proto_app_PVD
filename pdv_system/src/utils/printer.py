"""
Módulo de Impressão de Cupons Térmicos (58mm)
Gera PDF com ReportLab e abre automaticamente no Windows
"""

import os
import sys
import tempfile
import subprocess
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle, SimpleDocTemplate, Spacer
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT

from src.database.models import Venda, ItemVenda
from src.utils.config import STORE_NAME, RECEIPT_WIDTH
from src.utils.formatadores import FormataçãoUtil


class GeradorCupom:
    """Gera cupom térmico em PDF (58mm)"""
    
    def __init__(self, largura_mm=58):
        """
        Inicializa gerador de cupom
        
        Args:
            largura_mm (int): Largura do cupom em milímetros (padrão: 58mm)
        """
        self.largura_mm = largura_mm
        self.largura_points = largura_mm * mm
        self.margem = 2 * mm
        self.area_util = self.largura_points - (2 * self.margem)
    
    def _obter_venda(self, venda_id):
        """
        Obtém venda e itens do banco de dados
        
        Args:
            venda_id (int): ID da venda
            
        Returns:
            tuple: (Venda, list[ItemVenda]) ou None se não encontrada
        """
        try:
            venda = Venda.get(Venda.id == venda_id)
            itens = ItemVenda.select().where(ItemVenda.venda == venda)
            return venda, list(itens)
        except Venda.DoesNotExist as e:
            raise ValueError(f"Venda #{venda_id} não encontrada no banco de dados") from e
    
    def _criar_estilo_titulo(self):
        """Cria estilo para título"""
        return ParagraphStyle(
            name='Titulo',
            fontName='Helvetica-Bold',
            fontSize=10,
            alignment=TA_CENTER,
            spaceAfter=2,
            leading=10
        )
    
    def _criar_estilo_normal(self):
        """Cria estilo para texto normal"""
        return ParagraphStyle(
            name='Normal',
            fontName='Helvetica',
            fontSize=8,
            alignment=TA_CENTER,
            spaceAfter=1,
            leading=8
        )
    
    def _criar_estilo_item(self):
        """Cria estilo para itens da venda"""
        return ParagraphStyle(
            name='Item',
            fontName='Courier',
            fontSize=7,
            alignment=TA_LEFT,
            spaceAfter=1,
            leading=7
        )
    
    def gerar_pdf(self, venda_id, caminho_saida=None):
        """
        Gera PDF do cupom
        
        Args:
            venda_id (int): ID da venda
            caminho_saida (str): Caminho para salvar PDF (se None, usa temp)
            
        Returns:
            str: Caminho do arquivo PDF criado
        """
        # Obter dados da venda
        venda, itens = self._obter_venda(venda_id)
        
        if not itens:
            raise ValueError(f"Venda #{venda_id} não possui itens")
        
        # Definir caminho de saída
        if caminho_saida is None:
            temp_dir = tempfile.gettempdir()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"cupom_venda_{venda_id}_{timestamp}.pdf"
            caminho_saida = os.path.join(temp_dir, nome_arquivo)
        
        # Criar diretório se necessário
        Path(caminho_saida).parent.mkdir(parents=True, exist_ok=True)
        
        # Criar PDF
        self._criar_pdf_reportlab(venda, itens, caminho_saida)
        
        return caminho_saida
    
    def _criar_pdf_reportlab(self, venda, itens, caminho_saida):
        """
        Cria PDF usando ReportLab Platypus
        
        Args:
            venda (Venda): Objeto da venda
            itens (list): Lista de ItemVenda
            caminho_saida (str): Caminho para salvar
        """
        # Configurar tamanho da página (58mm de largura)
        largura = 58 * mm
        altura = 200 * mm  # Altura variável
        
        # Criar documento
        doc = SimpleDocTemplate(
            caminho_saida,
            pagesize=(largura, altura),
            rightMargin=2*mm,
            leftMargin=2*mm,
            topMargin=3*mm,
            bottomMargin=3*mm,
            title=f"Cupom Venda {venda.id}"
        )
        
        story = []
        
        # Estilos
        style_titulo = self._criar_estilo_titulo()
        style_normal = self._criar_estilo_normal()
        style_item = self._criar_estilo_item()
        
        # Título - Nome da loja
        story.append(Paragraph(STORE_NAME, style_titulo))
        story.append(Spacer(1, 2*mm))
        
        # Separador
        story.append(Paragraph("-" * 30, style_item))
        story.append(Spacer(1, 1*mm))
        
        # Data e hora
        data_hora = venda.data_hora.strftime("%d/%m/%Y %H:%M:%S")
        story.append(Paragraph(f"<b>Data:</b> {data_hora}", style_normal))
        story.append(Paragraph(f"<b>Cupom #:</b> {venda.id}", style_normal))
        story.append(Spacer(1, 2*mm))
        
        # Separador
        story.append(Paragraph("-" * 30, style_item))
        story.append(Spacer(1, 2*mm))
        
        # Cabeçalho da tabela de itens
        story.append(Paragraph("<b>ITENS</b>", style_normal))
        story.append(Spacer(1, 1*mm))
        
        # Dados dos itens
        dados_tabela = [["Descrição", "Qtd", "Preço", "Total"]]
        
        for item in itens:
            produto_nome = item.produto.nome[:20]  # Limitar a 20 caracteres
            qtd = str(item.quantidade)
            preco = FormataçãoUtil.formatar_moeda(float(item.preco_unitario))
            total = FormataçãoUtil.formatar_moeda(float(item.subtotal))
            
            dados_tabela.append([produto_nome, qtd, preco, total])
        
        # Criar tabela
        tabela = Table(
            dados_tabela,
            colWidths=[20*mm, 9*mm, 12*mm, 13*mm]
        )
        
        tabela.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Courier', 7),
            ('FONT', (0, 0), (-1, 0), 'Courier-Bold', 7),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        story.append(tabela)
        story.append(Spacer(1, 2*mm))
        
        # Separador
        story.append(Paragraph("-" * 30, style_item))
        story.append(Spacer(1, 2*mm))
        
        # Totalizadores
        subtotal = sum(float(item.subtotal) for item in itens)
        desconto = float(venda.desconto) if venda.desconto else Decimal('0')
        total = float(venda.total) if venda.total else subtotal - desconto
        
        story.append(Paragraph(
            f"<b>Subtotal:</b> {FormataçãoUtil.formatar_moeda(subtotal)}", 
            style_normal
        ))
        
        if desconto > 0:
            story.append(Paragraph(
                f"<b>Desconto:</b> -{FormataçãoUtil.formatar_moeda(desconto)}", 
                style_normal
            ))
        
        story.append(Spacer(1, 1*mm))
        story.append(Paragraph("-" * 30, style_item))
        story.append(Spacer(1, 1*mm))
        
        # Total em destaque
        story.append(Paragraph(
            f"<font size=10><b>TOTAL: {FormataçãoUtil.formatar_moeda(total)}</b></font>", 
            style_titulo
        ))
        
        story.append(Spacer(1, 2*mm))
        
        # Forma de pagamento
        forma_pagamento = venda.forma_pagamento or "NÃO ESPECIFICADA"
        story.append(Paragraph(f"<b>Pagamento:</b> {forma_pagamento}", style_normal))
        
        story.append(Spacer(1, 3*mm))
        
        # Rodapé
        story.append(Paragraph("-" * 30, style_item))
        story.append(Spacer(1, 1*mm))
        story.append(Paragraph("Obrigado pela compra!", style_normal))
        story.append(Paragraph(datetime.now().strftime("%d/%m/%Y %H:%M"), style_normal))
        
        # Construir PDF
        doc.build(story)
    
    def abrir_pdf(self, caminho_pdf):
        """
        Abre PDF com o programa padrão do Windows
        
        Args:
            caminho_pdf (str): Caminho do arquivo PDF
            
        Raises:
            OSError: Se arquivo não existir ou erro ao abrir
            NotImplementedError: Se sistema operacional não for Windows
        """
        if not os.path.exists(caminho_pdf):
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho_pdf}")
        
        if sys.platform != 'win32':
            raise NotImplementedError("Função de abertura automática é suportada apenas em Windows")
        
        try:
            # Usar comando 'start' do Windows para abrir com programa padrão
            os.startfile(caminho_pdf)
        except OSError as _e:
            # Fallback: usar subprocess
            try:
                subprocess.Popen(['start', caminho_pdf], shell=True)
            except Exception as e2:
                raise OSError(f"Erro ao abrir PDF: {e2}") from e2


def gerar_cupom(venda_id, abrir_automatico=True, caminho_saida=None):
    """
    Função principal para gerar cupom térmico
    
    Gera um PDF formatado para impressora térmica (58mm) a partir de uma venda
    no banco de dados. O PDF contém:
    - Nome da loja
    - Data e hora da venda
    - Lista de itens com quantidade, preço e total
    - Subtotal, desconto (se houver) e total
    - Forma de pagamento
    
    Args:
        venda_id (int): ID da venda no banco de dados
        abrir_automatico (bool): Se True, abre o PDF automaticamente no Windows
        caminho_saida (str): Caminho para salvar PDF (se None, usa pasta temporária)
        
    Returns:
        str: Caminho do arquivo PDF gerado
        
    Raises:
        ValueError: Se venda_id não encontrada ou venda sem itens
        FileNotFoundError: Se arquivo PDF não puder ser salvo
        NotImplementedError: Se sistema não for Windows e abrir_automatico=True
        
    Exemplo:
        >>> # Gerar e abrir automaticamente
        >>> caminho = gerar_cupom(venda_id=5)
        >>> print(f"Cupom salvo em: {caminho}")
        
        >>> # Gerar sem abrir
        >>> caminho = gerar_cupom(venda_id=5, abrir_automatico=False)
        
        >>> # Salvar em local específico
        >>> caminho = gerar_cupom(
        ...     venda_id=5,
        ...     caminho_saida="/home/user/cupom.pdf"
        ... )
    """
    try:
        # Criar gerador
        gerador = GeradorCupom(largura_mm=int(RECEIPT_WIDTH))
        
        # Gerar PDF
        caminho_pdf = gerador.gerar_pdf(venda_id, caminho_saida)
        
        print(f"✅ Cupom gerado: {caminho_pdf}")
        
        # Abrir se solicitado
        if abrir_automatico:
            try:
                gerador.abrir_pdf(caminho_pdf)
                print("Abrindo PDF para impressão...")
            except NotImplementedError:
                print(f"Abertura automática não suportada neste SO. Abra manualmente: {caminho_pdf}")
            except OSError as e:
                print(f"Erro ao abrir PDF: {e}")
        
        return caminho_pdf
        
    except ValueError as e:
        print(f"Erro: {e}")
        raise
    except Exception as e:
        print(f"❌ Erro ao gerar cupom: {e}")
        raise


# Aliases para compatibilidade
def gerar_cupom_pdf(venda_id, abrir=True):
    """Alias para gerar_cupom()"""
    return gerar_cupom(venda_id, abrir_automatico=abrir)


if __name__ == '__main__':
    # Script de teste - Execute para testar geração de cupom
    # Uso: python -m src.utils.printer <venda_id> [--no-open]
    
    if len(sys.argv) < 2:
        print("Uso: python -m src.utils.printer <venda_id> [--no-open]")
        print("\nExemplo:")
        print("  python -m src.utils.printer 1")
        print("  python -m src.utils.printer 1 --no-open")
        sys.exit(1)
    
    try:
        venda_id = int(sys.argv[1])
        abrir = '--no-open' not in sys.argv
        
        caminho = gerar_cupom(venda_id, abrir_automatico=abrir)
        print(f"\n✅ Sucesso! Cupom: {caminho}")
        
    except ValueError as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)
