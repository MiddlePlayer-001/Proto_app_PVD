# 🚀 INSTALAÇÃO - PDV SYSTEM v1.0.0

## ⚡ INSTALAÇÃO RÁPIDA (5 minutos)

### Windows

```bash
# 1. Abrir PowerShell ou CMD como Administrador

# 2. Ir para a pasta do projeto
cd caminho\para\pdv_system

# 3. Criar ambiente virtual
python -m venv venv

# 4. Ativar ambiente virtual
venv\Scripts\activate

# 5. Instalar dependências
pip install -r requirements.txt

# 6. Executar a aplicação
python main.py
```

### Linux / macOS

```bash
# 1. Abrir terminal

# 2. Ir para a pasta do projeto
cd caminho/para/pdv_system

# 3. Criar ambiente virtual
python3 -m venv venv

# 4. Ativar ambiente virtual
source venv/bin/activate

# 5. Instalar dependências
pip install -r requirements.txt

# 6. Executar a aplicação
python main.py
```

---

## ✅ PRÉ-REQUISITOS

- **Python 3.8+** instalado
- **pip** (gerenciador de pacotes Python)
- ~500MB de espaço em disco

**Para verificar se Python está instalado:**
```bash
python --version
```

---

## 📦 O QUE VAI SER INSTALADO

- **Flet 0.23.0** - Interface gráfica desktop
- **Peewee 3.17.0** - ORM para banco de dados
- **ReportLab 4.0.7** - Geração de PDFs
- **python-dotenv 1.2.1** - Gerenciamento de configurações

---

## 🎯 PRIMEIRA EXECUÇÃO

1. A aplicação criará automaticamente o banco de dados (`data/loja.db`)
2. Dados de exemplo serão carregados
3. A interface gráfica abrirá

---

## 🔄 PRÓXIMAS EXECUÇÕES

Simplesmente execute:
```bash
python main.py
```

Na próxima vez, será quase instantâneo (não precisa instalar dependências novamente).

---

## 🐛 SOLUÇÃO DE PROBLEMAS

### Python não encontrado
Reinstale Python de https://www.python.org/ (marque "Add Python to PATH")

### Permissão negada no Linux/Mac
```bash
chmod +x setup.sh
```

### Problema com venv
Deletar a pasta `venv/` e criar uma nova:
```bash
rm -rf venv
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
```

---

## 📚 MAIS INFORMAÇÕES

Veja a documentação completa em `docs/README.md`

