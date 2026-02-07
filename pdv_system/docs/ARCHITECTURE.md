"""
Guia de Arquitetura do Sistema PDV
====================================

Este documento descreve a arquitetura do sistema de PDV,
os padrões de design utilizados e como estender o código.
"""

# CAMADAS DA ARQUITETURA
# =======================

"""
┌────────────────────────────────────────────────────────────────┐
│                      INTERFACE (UI)                            │
│  - Flet (Framework Multiplataforma)                           │
│  - Componentes Reutilizáveis                                  │
│  - Tema Escuro com Material Design                            │
│  src/ui/                                                       │
│    ├── main_app.py       (Aplicação Principal)                │
│    ├── pages/            (Páginas da Aplicação)               │
│    ├── components/       (Componentes Reutilizáveis)          │
│    └── styles.py         (Estilos e Temas)                    │
└────────────────────────────────────────────────────────────────┘
                              ↕
┌────────────────────────────────────────────────────────────────┐
│                   SERVIÇOS (BUSINESS LOGIC)                    │
│  - Validação de Regras de Negócio                             │
│  - Orquestração de Operações                                  │
│  - Serviços Transversais                                      │
│  src/services/                                                 │
│    ├── produto_service.py                                     │
│    ├── venda_service.py                                       │
│    ├── financeiro_service.py                                  │
│    └── relatorio_service.py                                   │
└────────────────────────────────────────────────────────────────┘
                              ↕
┌────────────────────────────────────────────────────────────────┐
│                   REPOSITÓRIOS (DATA ACCESS)                   │
│  - Queries CRUD                                               │
│  - Operações de Banco                                         │
│  - Abstração do ORM                                           │
│  src/models/                                                   │
│    ├── produto_repository.py                                  │
│    ├── venda_repository.py                                    │
│    └── financeiro_repository.py                               │
└────────────────────────────────────────────────────────────────┘
                              ↕
┌────────────────────────────────────────────────────────────────┐
│               MODELOS (DATABASE LAYER)                         │
│  - Peewee ORM                                                 │
│  - Definição de Tabelas                                       │
│  - Relacionamentos                                            │
│  src/database/                                                 │
│    ├── connection.py     (Conexão SQLite)                     │
│    └── models.py         (Modelos Peewee)                     │
└────────────────────────────────────────────────────────────────┘
                              ↕
┌────────────────────────────────────────────────────────────────┐
│                   BANCO DE DADOS                               │
│  - SQLite (data/loja.db)                                      │
│  - Índices para Performance                                   │
│  - Constraints de Integridade                                 │
└────────────────────────────────────────────────────────────────┘

Fluxo de Dados:
User → UI → Services → Repositories → Models → Database → Models → Repositories → Services → UI → User

"""

# PADRÕES DE DESIGN
# ====================

"""
1. MVC (Model-View-Controller)
   - Model: Modelos Peewee em database/models.py
   - View: Interface Flet em ui/
   - Controller: Serviços em services/

2. Repository Pattern
   - Abstração da camada de dados
   - Operações CRUD centralizadas
   - Facilita testes (mock dos repositórios)
   
3. Service Pattern
   - Encapsulamento de lógica de negócio
   - Validações e orquestração
   - Reutilização entre múltiplos controladores

4. Singleton
   - Instância única do banco de dados
   - Gerenciada em src/database/connection.py
   - Conexão reutilizável em toda a aplicação

5. Dependency Injection (Implícito)
   - Serviços instanciam seus repositórios
   - Fácil para substituir implementações

"""

# FLUXO DE UMA OPERAÇÃO COMPLETA
# ==================================

"""
Exemplo: Criando um novo produto

1. UI (flet button click)
   └─> ProdutoService.criar_produto(nome, codigo, preco...)

2. Service (validação de negócio)
   ├─> Valida regras (preço > 0, código único)
   └─> ProdutoRepository.criar(...)

3. Repository (operação de banco)
   ├─> Prepara dados
   └─> Produto.create() (Peewee ORM)

4. Database (persistência)
   ├─> INSERT INTO produtos (...)
   └─> Retorna ID

5. Volta pela cadeia
   └─> Repository → Service → UI (atualiza tela)

"""

# ESTRUTURA DE MODELOS
# ========================

"""
Produto (Tabela: produtos)
├─ id (PK)
├─ nome (UNIQUE, INDEX)
├─ codigo (UNIQUE, INDEX)
├─ preco_custo
├─ preco_venda
├─ estoque
├─ ativo
├─ descricao
├─ criado_em
└─ atualizado_em
   Relacionamentos:
   └─> ItemVenda (1:N)

Venda (Tabela: vendas)
├─ id (PK)
├─ numero (UNIQUE, INDEX)
├─ data_hora (INDEX)
├─ total
├─ desconto
├─ valor_pago
├─ troco
├─ forma_pagamento
├─ processada (INDEX)
└─ observacoes
   Relacionamentos:
   ├─> ItemVenda (1:N)
   └─> Transacao (1:N)

ItemVenda (Tabela: itens_venda)
├─ id (PK)
├─ venda_id (FK, INDEX)
├─ produto_id (FK, INDEX)
├─ quantidade
├─ preco_unitario
└─ subtotal

Transacao (Tabela: transacoes)
├─ id (PK)
├─ tipo (ENTRADA/SAIDA, INDEX)
├─ categoria (VENDA/DESPESA, INDEX)
├─ descricao
├─ valor
├─ data_transacao (INDEX)
├─ venda_id (FK, opcional)
└─ observacoes

FechamentoDia (Tabela: fechamento_dia)
├─ id (PK)
├─ data (UNIQUE, INDEX)
├─ total_vendas
├─ total_despesas
├─ total_entradas
├─ saldo
├─ quantidade_transacoes
└─ observacoes

"""

# COMO ESTENDER O SISTEMA
# ==========================

"""
1. Adicionar Nova Funcionalidade

a) Criar o Repositório (src/models/nova_feature_repository.py)
   ├─ Operações CRUD em um modelo Peewee
   ├─ Queries específicas
   └─ Lógica de acesso a dados

b) Criar o Serviço (src/services/nova_feature_service.py)
   ├─ Validar dados de entrada
   ├─ Chamar repositório
   ├─ Retornar dados serializados
   └─ Tratar exceções

c) Atualizar a UI (src/ui/pages/nova_feature.py)
   ├─ Criar formulário
   ├─ Chamar serviço
   ├─ Atualizar tela
   └─ Feedback do usuário

2. Adicionar Novo Modelo

a) Definir em src/database/models.py
   ├─ Herdar de BaseModel
   ├─ Definir campos
   ├─ Definir índices
   └─ Meta.table_name

b) Criar repositório específico (src/models/xxx_repository.py)
   └─ CRUD e queries customizadas

c) Criar serviço (src/services/xxx_service.py)
   └─ Lógica de negócio

3. Adicionar Nova Página na UI

a) Criar arquivo src/ui/pages/nova_pagina.py
b) Importar em main_app.py
c) Adicionar rota
d) Implementar componentes Flet

4. Adicionar Validação

src/utils/validadores.py
├─ Adicionar método estático validar_xxx()
└─ Usar em services/

5. Adicionar Formatação

src/utils/formatadores.py
├─ Adicionar método estático formatar_xxx()
└─ Usar em UI

"""

# TRATAMENTO DE ERROS
# ======================

"""
Padrão utilizado:

1. No Repository/Model
   └─> Deixar exceção propagar

2. No Service
   ├─> Capturar exceção do repository
   ├─> Validar regras de negócio
   └─> Raise ValueError com mensagem clara

3. Na UI
   ├─> Capturar exceção do service
   ├─> Exibir snackbar ou dialog
   └─> Log no console (se DEBUG)

Exemplo:
try:
    service.criar_produto(...)
except ValueError as e:
    # Exibir erro para usuário
    mostrar_erro(str(e))
except Exception as e:
    # Erro inesperado
    log.error(f"Erro crítico: {e}")
    mostrar_erro("Erro inesperado")

"""

# PERFORMANCE
# ============

"""
1. Índices (database/models.py)
   ├─ Campos únicos: codigo, numero
   ├─ Campos de busca: nome, codigo
   ├─ Campos de range: data_hora
   └─ Campos de filtro: ativo, tipo

2. Paginação
   - Não implementada ainda
   - Planejar para grandes volumes
   - Usar limit/offset nos repositories

3. Cache
   - Não implementado
   - Avaliar para consultas frequentes
   - Invalidar ao atualizar

4. Connection Pool
   - SQLite não suporta nativamente
   - Está ok para desktop
   - Usar WAL mode (já configurado)

5. Lazy Loading
   - Peewee carrega relacionamentos sob demanda
   - Prefetch quando necessário (select_related)

"""

# TESTES
# =======

"""
Estrutura de testes (a implementar):

tests/
├── test_models.py        # Testes de modelo
├── test_repositories.py  # Testes de repositório
├── test_services.py      # Testes de serviço
└── test_utils.py         # Testes de utilitários

Exemplo de teste:
def test_criar_produto():
    service = ProdutoService()
    produto = service.criar_produto(
        nome="Teste",
        codigo="TEST",
        preco_venda=10.0
    )
    assert produto['id'] is not None
    assert produto['nome'] == "Teste"

"""

# SEGURANÇA
# ===========

"""
1. SQL Injection
   ✓ Prevenido: Usando Peewee ORM
   ✓ Não usar string formatting em queries

2. Validação de Entrada
   ✓ ValidadorUtil: validação em services
   ✓ Tipos de dados: Python garante tipos
   ✓ Range/valores: Verificar em service

3. Acesso a Dados
   - Sem autenticação (versão atual)
   - Planejar para multi-usuário
   - Auditoria de operações

4. Banco de Dados
   ✓ Foreign keys ativadas
   ✓ Constraints de integridade
   ✓ WAL mode para segurança

"""

# LOGS
# =====

"""
Sistema de logs (a implementar):

import logging

logger = logging.getLogger(__name__)

# Em services:
logger.info(f"Produto criado: {produto_id}")
logger.error(f"Erro ao criar: {e}")

# Em main.py:
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

"""

# ROADMAP DE DESENVOLVIMENTO
# ============================

"""
Versão 1.0 (Atual)
✓ CRUD de produtos
✓ Sistema de vendas
✓ Carrinho de compras
✓ Cálculo de troco
✓ Transações financeiras
✓ Fechamento diário
✓ Cupom em PDF

Versão 1.1
- [ ] Autenticação de usuários
- [ ] Múltiplos operadores
- [ ] Auditoria de operações
- [ ] Backup automático

Versão 1.2
- [ ] Tabelas de cliente/CPF
- [ ] Histórico de compras
- [ ] Desconto por cliente
- [ ] Crediário/fiado

Versão 1.3
- [ ] Integração com impressora térmica
- [ ] Leitor de código de barras
- [ ] Integração com sistemas de pagamento
- [ ] API para mobile

Versão 2.0
- [ ] Sistema multi-loja
- [ ] Sincronização em nuvem
- [ ] Mobile app
- [ ] Dashboard analytics

"""

# CONTRIBUINDO
# ==============

"""
Para adicionar um novo repositório:

1. Criar arquivo src/models/xyz_repository.py
2. Implementar métodos CRUD
3. Adicionar em src/models/__init__.py
4. Criar teste em tests/test_repositories.py
5. Documentar em ARCHITECTURE.md

Para adicionar um novo serviço:

1. Criar arquivo src/services/xyz_service.py
2. Instanciar repositórios necessários
3. Implementar lógica de negócio
4. Validar entrada com ValidadorUtil
5. Retornar dados estruturados
6. Adicionar em src/services/__init__.py

Para adicionar uma página na UI:

1. Criar src/ui/pages/xyz.py
2. Importar em ui/main_app.py
3. Adicionar rota em route_change()
4. Usar componentes de styles.py
5. Testar responsividade

"""

print(__doc__)
