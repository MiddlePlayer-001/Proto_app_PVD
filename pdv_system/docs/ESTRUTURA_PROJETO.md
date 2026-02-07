# 📁 ESTRUTURA DO PROJETO - PDV SYSTEM

## Estrutura Final Organizada

```
pdv_system/
│
├── 📄 ARQUIVOS RAIZ (ESSENCIAIS)
│   ├── main.py                    # Arquivo principal - executa a aplicação
│   ├── requirements.txt            # Dependências do projeto
│   ├── INSTALACAO.md              # Guia rápido de instalação ⭐ LEIA PRIMEIRO
│   └── .gitignore                 # Arquivos ignorados pelo Git (se aplicável)
│
├── 📂 src/                        # CÓDIGO-FONTE
│   ├── __init__.py
│   ├── database/                  # Camada de dados
│   │   ├── __init__.py
│   │   ├── connection.py          # Conexão com SQLite
│   │   └── models.py              # Modelos Peewee ORM
│   ├── models/                    # DAL - Data Access Layer (Repositórios)
│   │   ├── __init__.py
│   │   ├── produto_repository.py  # CRUD de Produtos
│   │   ├── venda_repository.py    # CRUD de Vendas
│   │   └── financeiro_repository.py # CRUD de Financeiro
│   ├── services/                  # Lógica de Negócio
│   │   ├── __init__.py
│   │   ├── produto_service.py     # Serviços de Produto
│   │   ├── venda_service.py       # Serviços de Venda
│   │   ├── financeiro_service.py  # Serviços Financeiros
│   │   └── relatorio_service.py   # Geração de Relatórios
│   ├── ui/                        # INTERFACE GRÁFICA (Flet)
│   │   ├── __init__.py
│   │   ├── main_app.py            # Aplicação principal
│   │   ├── pages/                 # Páginas da aplicação
│   │   ├── components/            # Componentes reutilizáveis
│   │   └── styles.py              # Temas e estilos
│   └── utils/                     # Utilitários
│       ├── __init__.py
│       ├── config.py              # Configurações da app
│       └── formatadores.py        # Formatação de dados
│
├── 📂 data/                       # DADOS
│   └── loja.db                    # Banco de dados SQLite
│
├── 📂 dist/                       # EXECUTÁVEIS COMPILADOS
│   ├── INSTALLER.exe              # Instalador auto-contido
│   └── PDV_System.exe             # Executável da aplicação
│
├── 📂 config/                     # CONFIGURAÇÕES
│   └── .env.example               # Template de variáveis de ambiente
│
└── 📂 docs/                       # DOCUMENTAÇÃO COMPLETA
    ├── README.md                  # Documentação principal
    ├── INSTALACAO.md              # Guia de instalação detalhado
    ├── DEPLOYMENT_GUIDE.md        # Guia de deploy em produção
    ├── ARCHITECTURE.md            # Arquitetura do sistema
    ├── GUIA_PDV_INTERFACE.md      # Guia de uso da interface
    ├── GUIA_PRINTER.md            # Integração com impressora
    ├── GUIA_LOGGING.md            # Sistema de logging
    ├── PRONTO_DISTRIBUIR.txt      # Status de produção
    ├── O_QUE_FAZ_INSTALLER.txt    # Explicação do instalador
    ├── CHECKLIST_ENTREGA.txt      # Checklist de entrega
    └── [Mais documentação...]
```

---

## 🎯 COMO USAR ESTA ESTRUTURA

### Para Desenvolvedores:
1. Clone o repositório: `git clone <repo>`
2. Siga o `INSTALACAO.md` para setup
3. Código-fonte em `src/` segue o padrão MVC
4. Veja `docs/ARCHITECTURE.md` para arquitetura

### Para Usuários Finais:
1. Baixe `dist/INSTALLER.exe`
2. Clique 2x para instalar (automático!)
3. Pronto! App já funciona

### Para Deploy em Produção:
1. Veja `docs/DEPLOYMENT_GUIDE.md`
2. Configure variáveis de ambiente em `config/.env`
3. Execute `python main.py`

---

## ✅ GARANTIAS DE LIMPEZA

- ✓ Sem arquivos soltos no diretório raiz (apenas essenciais)
- ✓ Documentação organizada em `docs/`
- ✓ Configurações centralizadas em `config/`
- ✓ Código fonte bem estruturado em `src/`
- ✓ Dados em `data/`
- ✓ Executáveis em `dist/`
- ✓ Sem cache Python (`__pycache__`)
- ✓ Sem pastas temporárias

---

**Ultima atualização:** Fevereiro 2026  
**Status:** ✅ Pronto para Produção
