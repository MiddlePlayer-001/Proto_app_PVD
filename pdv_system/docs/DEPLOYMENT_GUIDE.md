# 🚀 GUIA DE DEPLOY PARA PRODUÇÃO - PDV SYSTEM v1.0.0

**Status:** ✅ **PRONTO PARA PRODUÇÃO** (6/6 testes passando - 0 erros críticos)

---

## 📋 Resumo do Projeto

**Sistema de Ponto de Venda (PDV)** em Python com Interface Gráfica Multiplataforma
- **Linguagem:** Python 3.8+
- **UI Framework:** Flet 0.23.0 (Desktop/Web)
- **Database:** SQLite com Peewee ORM
- **Relatórios:** ReportLab (PDF)
- **Ambiente:** Windows/Linux/macOS

---

## 📦 Dependências (requirements.txt)

```
flet==0.23.0
flet-core==0.23.0
flet-runtime==0.23.0
peewee==3.17.0
reportlab==4.0.7
python-dotenv==1.2.1
```

---

## 🔧 Instalação em Produção

### 1️⃣ Pré-requisitos
- Python 3.8 ou superior instalado
- pip ou conda para gerenciamento de pacotes
- ~500MB de espaço em disco

### 2️⃣ Clone/Download do Repositório
```bash
# Via Git
git clone <seu-repositorio> pdv_system
cd pdv_system

# Ou via arquivo ZIP
unzip pdv_system.zip
cd pdv_system
```

### 3️⃣ Criar Ambiente Virtual (Recomendado)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4️⃣ Instalar Dependências
```bash
pip install -r requirements.txt
```

**Tempo estimado:** 3-5 minutos

### 5️⃣ Validar Instalação
```bash
python validar_sistema.py
```

**Esperado:** `Resultado: 6/6 testes passaram`

---

## 🗄️ Configuração Inicial

### 1. Banco de Dados
```bash
# Criar banco com tabelas
python exemplos_dados.py
```

**Isso vai:**
- ✅ Criar arquivo `pdv_system.db` (SQLite)
- ✅ Criar 5 tabelas (produtos, vendas, itens, transações, fechamentos)
- ✅ Popular dados de exemplo

### 2. Variáveis de Ambiente (Opcional)
```bash
# Criar arquivo .env
cp .env.example .env

# Editar com suas configurações
# STORE_NAME=Minha Loja PDV
# RECEIPT_WIDTH=58mm
# TIMEZONE=UTC-3
```

---

## 🚀 Iniciar Aplicação

### Modo Desktop (Flet)
```bash
python main.py
```

**A aplicação abrirá em uma janela nativa do sistema**

### Modo Web (Opcional)
```bash
python -m flet run main.py --web
```

Acesse em: `http://localhost:8000`

---

## 📂 Estrutura de Arquivos Essenciais

```
pdv_system/
├── main.py                    # Arquivo principal
├── requirements.txt           # Dependências
├── validar_sistema.py        # Validação
├── exemplos_dados.py         # Populate BD
├── .env                       # Config ambiente (criar)
├── pdv_system.db             # Banco (auto-criado)
│
├── src/
│   ├── database/
│   │   ├── connection.py      # Conexão SQLite
│   │   ├── models.py          # Modelos ORM
│   │
│   ├── models/                # Repositórios (CRUD)
│   │   ├── produto_repository.py
│   │   ├── venda_repository.py
│   │   └── financeiro_repository.py
│   │
│   ├── services/              # Lógica de negócio
│   │   ├── produto_service.py
│   │   ├── venda_service.py
│   │   ├── financeiro_service.py
│   │   └── relatorio_service.py
│   │
│   ├── utils/
│   │   ├── config.py          # Configurações
│   │   ├── formatadores.py    # Formatação (R$, %, data)
│   │   ├── validadores.py     # Validações
│   │   ├── printer.py         # Geração de PDFs
│   │   ├── dashboard.py       # Dashboard
│   │
│   └── ui/
│       ├── main_app.py        # Aplicação principal
│       ├── pdv_view.py        # Interface PDV
│       ├── styles.py          # Temas/Cores
└── test_*.py                  # Testes (opcional)
```

---

## ✅ Checklist de Deploy

- [ ] Python 3.8+ instalado (`python --version`)
- [ ] Dependências instaladas (`pip show flet peewee`)
- [ ] Banco criado (`python exemplos_dados.py`)
- [ ] Validação passou (`python validar_sistema.py`)
- [ ] Arquivo `.env` configurado (opcional)
- [ ] Aplicação executa (`python main.py`)

---

## 🔍 Testes

### Executar Testes
```bash
# Validação do sistema
python validar_sistema.py

# Teste do fluxo de vendas
python test_fluxo_venda.py

# Teste da interface PDV
python test_pdv_interface.py

# Teste do módulo printer
python test_printer.py
```

**Esperado:** ✅ Todos os testes passam

---

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'flet'"
```bash
pip install --upgrade flet
pip install flet==0.23.0
```

### Erro: "banco de dados está bloqueado"
```bash
# Feche a aplicação
# Delete pdv_system.db se necessário
rm pdv_system.db  # Linux/Mac
del pdv_system.db # Windows
python exemplos_dados.py
```

### Erro: "Permissão negada ao criar arquivos"
- Verifique permissões da pasta
- Execute como administrador (Windows)
- Use `chmod 755` (Linux/Mac)

### Interface não abre
```bash
# Teste a instalação do Flet
python -c "import flet; print(flet.__version__)"

# Se não funcionar:
pip uninstall flet -y
pip install flet==0.23.0
```

---

## 📊 Monitoramento em Produção

### Logs
```bash
# Redirecionar output
python main.py > pdv.log 2>&1

# No Windows (PowerShell)
python main.py | Tee-Object -FilePath pdv.log
```

### Backup do Banco
```bash
# Copiar banco regularmente
cp pdv_system.db pdv_system.db.backup_$(date +%Y%m%d_%H%M%S)

# No Windows
copy pdv_system.db pdv_system.db.backup
```

---

## 🔐 Segurança

1. **Banco de Dados**
   - Arquivo `pdv_system.db` contém dados sensíveis
   - Fazer backup regularmente
   - Controlar acesso ao arquivo

2. **Variáveis de Ambiente**
   - Nunca commitar `.env` em repositório
   - Adicionar `.env` ao `.gitignore`
   - Usar valores diferentes por ambiente

3. **Atualizações**
   - Manter Python atualizado
   - Revisar atualizações do Flet/Peewee
   - Testar em dev antes de produção

---

## 📈 Performance

- **Tempo de inicialização:** ~3-5 segundos
- **Memória:** ~80-120MB em repouso
- **Banco de Dados:** Índices automáticos no SQLite
- **Concorrência:** SQLite suporta 1 escrita simultânea

---

## 📞 Suporte

### Arquivo de Troubleshooting
Consulte `RESOLUCAO_FINAL.md` para histórico de correções

### Comandos Úteis
```bash
# Verificar estrutura do BD
python -c "from src.database.models import *; print([m.__name__ for m in [Produto, Venda, ItemVenda, Transacao, FechamentoDia]])"

# Listar versões de dependências
pip list | grep -E "flet|peewee|reportlab"

# Limpar cache Python
find . -type d -name __pycache__ -exec rm -r {} +
find . -name "*.pyc" -delete
```

---

## 🎯 Próximos Passos

1. **Configurar em Produção**
   - Ajustar variáveis em `.env`
   - Configurar banco compartilhado se necessário
   - Testar com dados reais

2. **Distribuir Aplicação**
   - Para EXE Windows: use PyInstaller
   - Para distribução: criar instalador
   - Adicionar shortcut no menu Iniciar

3. **Manutenção Contínua**
   - Backup automático do banco
   - Logs de auditoria
   - Plano de atualização

---

## 📝 Informações Técnicas

| Componente | Versão | Status |
|-----------|--------|--------|
| Python | 3.8+ | ✅ Testado |
| Flet | 0.23.0 | ✅ Testado |
| Peewee | 3.17.0 | ✅ Testado |
| ReportLab | 4.0.7 | ✅ Testado |
| SQLite | Nativo | ✅ OK |

---

**Data de Deploy:** Fevereiro 6, 2026  
**Status:** ✅ **PRONTO PARA PRODUÇÃO**  
**Validação:** 6/6 testes passando  
**Erros Críticos:** 0  

🎉 **Seu sistema está pronto para ir ao ar!**
