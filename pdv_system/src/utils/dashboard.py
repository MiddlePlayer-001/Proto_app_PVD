"""
Dashboard - Resumo Financeiro para Tela Inicial
Exibe 3 Cards com totais do dia
"""

from datetime import date
from src.models.financeiro_repository import get_resumo_dia
from src.utils.formatadores import FormataçãoUtil


def obter_dados_dashboard(data: date = None) -> dict:
    """
    Obtém dados para exibição no dashboard
    
    Retorna um dicionário com os resumos formatados para exibição
    
    Args:
        data (date): Data para consulta (padrão: hoje)
        
    Returns:
        dict: {
            'total_vendas': '12.345,67',
            'total_despesas': '1.234,56',
            'saldo_liquido': '11.111,11',
            'data': '2026-02-06'
        }
    """
    resumo = get_resumo_dia(data)
    
    return {
        'total_vendas': FormataçãoUtil.formatar_moeda(float(resumo['total_vendas'])),
        'total_despesas': FormataçãoUtil.formatar_moeda(float(resumo['total_despesas'])),
        'saldo_liquido': FormataçãoUtil.formatar_moeda(float(resumo['saldo_liquido'])),
        'data': resumo['data'].strftime('%d/%m/%Y'),
        'quantidade_transacoes': resumo['quantidade_transacoes']
    }


if __name__ == '__main__':
    # Teste do dashboard
    from src.database.connection import init_db
    
    init_db()
    dados = obter_dados_dashboard()
    
    print("\n" + "="*60)
    print("DASHBOARD - RESUMO DO DIA")
    print("="*60)
    print(f"\nData: {dados['data']}")
    print(f"Transações: {dados['quantidade_transacoes']}")
    print("\n" + "-"*60)
    print(f"\n💰 Total de Vendas:  {dados['total_vendas']:>20}")
    print(f"💸 Total Despesas:   {dados['total_despesas']:>20}")
    print(f"📊 Saldo Líquido:    {dados['saldo_liquido']:>20}")
    print("\n" + "="*60 + "\n")
