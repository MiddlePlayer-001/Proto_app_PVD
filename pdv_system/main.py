"""
=============================================================================
SISTEMA DE PDV (PONTO DE VENDA) DESKTOP PARA WINDOWS
=============================================================================

Versão: 1.0.0
Autor: PDV Team
Data de Criação: 2026

OBJETIVO:
---------
Sistema completo de Ponto de Venda (PDV) para Windows, desenvolvido em Python
com interface moderna usando Flet e banco de dados SQLite com Peewee ORM.

MÓDULOS PRINCIPAIS:
-------------------
1. database/     - Camada de conexão e modelos (Peewee ORM)
2. models/       - Repositórios (Data Access Layer)
3. services/     - Serviços de negócio (Business Logic Layer)
4. ui/          - Interface gráfica (Flet)
5. utils/       - Utilitários e configurações

FUNCIONALIDADES:
---------------
✓ Gerenciamento de Produtos (CRUD completo)
✓ Sistema de PDV com carrinho de compras
✓ Cálculo automático de troco
✓ Tabela unificada de transações financeiras
✓ Fechamento diário automático
✓ Geração de cupom não-fiscal em PDF
✓ Relatórios financeiros e de vendas
✓ Interface responsiva tema escuro
✓ Botões grandes para operação fácil

REQUISITOS:
-----------
- Python 3.8+
- Windows 7+
- Dependências em requirements.txt

USO:
----
1. Instalar dependências:
   pip install -r requirements.txt

2. Executar aplicação:
   python main.py

3. (PRIMEIRO USO) Inicializar banco de dados:
   python -c "from src.database import init_db; init_db()"

ARQUITETURA:
-----------
┌─────────────────────────────────────────┐
│           INTERFACE GRÁFICA (Flet)       │
└─────────────────────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│     CAMADA DE SERVIÇOS (Services)        │
│  - ProdutoService                        │
│  - VendaService                          │
│  - FinanceiroService                     │
│  - RelatorioService                      │
└─────────────────────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│     REPOSITÓRIOS (Data Access)           │
│  - ProdutoRepository                     │
│  - VendaRepository                       │
│  - TransacaoRepository                   │
│  - FechamentoDiaRepository               │
└─────────────────────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│   MODELOS (Peewee ORM & Database)        │
│  - Produto                               │
│  - Venda, ItemVenda                      │
│  - Transacao                             │
│  - FechamentoDia                         │
└─────────────────────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│      BANCO DE DADOS (SQLite)             │
│      data/loja.db                        │
└─────────────────────────────────────────┘

PADRÕES DE DESIGN UTILIZADOS:
-----------------------------
- MVC (Model-View-Controller): Separação clara entre UI, lógica e dados
- Repository Pattern: Abstração da camada de dados
- Service Pattern: Encapsulamento da lógica de negócio
- Singleton: Instância única do banco de dados
- Factory: Criação de objetos complexos

VARIÁVEIS DE AMBIENTE (.env):
------------------------------
DATABASE_PATH=./data/loja.db
STORE_NAME=Minha Loja
RECEIPT_WIDTH=58
TIMEZONE=UTC-3
DEBUG=False

LICENÇA:
--------
Este projeto é fornecido como exemplo educacional.

SUPORTE:
--------
Para dúvidas ou problemas, consulte a documentação do código.

=============================================================================
"""

import sys
from pathlib import Path

# Adicionar caminho do projeto ao sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

# Inicializar logger
try:
    from src.utils.logger import log_info, log_error
    log_info("=" * 70)
    log_info("INICIANDO PDV SYSTEM v1.0.0")
    log_info("=" * 70)
except ImportError as e:
    print(f"⚠️  Aviso ao inicializar logger: {e}")

# Inicializar banco de dados
try:
    from src.database import init_db
    print("🔧 Inicializando banco de dados...")
    if init_db():
        print("✅ Banco de dados pronto")
        log_info("Banco de dados inicializado com sucesso")
except (ImportError, OSError) as e:
    print(f"⚠️  Aviso ao inicializar banco: {e}")
    log_error(f"Erro ao inicializar banco de dados: {e}")

# Importar e executar aplicação Flet
try:
    from src.ui.main_app import main
    print("🚀 Iniciando aplicação...")
    log_info("Iniciando interface Flet")
    main()
except ImportError as e:
    print(f"❌ Erro ao iniciar aplicação: {e}")
    log_error(f"Erro crítico ao iniciar aplicação: {e}", exc_info=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    log_info("Encerrando PDV SYSTEM")
