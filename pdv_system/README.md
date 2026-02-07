# 🛒 Sistema PDV v1.0.0

Sistema profissional de Ponto de Venda (PDV) desenvolvido em Python com interface moderna usando **Flet** e banco de dados **SQLite**.

**Status:** ✅ Pronto para Produção | Testado | 0 Erros Críticos

---

## 📚 Documentação

Para informações detalhadas, consulte a documentação na pasta `docs/`:

- **[Leia Primeiro](docs/00_LEIA_PRIMEIRO.txt)** - Guia obrigatório para começar
- **[Arquitetura do Projeto](docs/ARCHITECTURE.md)** - Estrutura técnica completa
- **[Guia de Instalação](docs/COMO_INSTALAR.md)** - Passo a passo
- **[Documentação Completa](docs/README.md)** - Referência técnica completa
- **[Estrutura do Projeto](docs/ESTRUTURA_PROJETO.md)** - Organização dos diretórios
- **[Guia de Instalação Alternativo](docs/INSTALACAO.md)** - Método alternativo

---

## ⚡ Quick Start

### 1. Instalar Dependências
```bash
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

### 2. Executar
```bash
python main.py
```

---

## 🎯 Principais Recursos

- ✅ Interface PDV profissional e responsiva
- ✅ Gerenciamento completo de produtos
- ✅ Sistema de vendas com carrinho inteligente
- ✅ Controle de estoque automático
- ✅ Geração de cupom em PDF
- ✅ Controle financeiro integrado
- ✅ Arquitetura MVC profissional
- ✅ Suite de testes automatizados

---

## 🗂️ Estrutura do Projeto

```
pdv_system/
├── docs/                  # 📚 Documentação
├── src/                   # 💻 Código-fonte
│   ├── database/         # 🗄️ Camada de dados
│   ├── models/           # 📦 Repositórios (DAL)
│   ├── services/         # ⚙️ Lógica de negócio
│   ├── ui/               # 🎨 Interface Flet
│   └── utils/            # 🔧 Utilitários
├── data/                 # 📁 Banco de dados
├── config/               # ⚙️ Configurações
├── dist/                 # 📦 Executáveis
├── main.py               # 🚀 Ponto de entrada
└── requirements.txt      # 📋 Dependências
```

---

## 🛠️ Tecnologias

| Componente | Tecnologia |
|-----------|-----------|
| Interface | Flet 0.23.0 |
| Banco de Dados | SQLite + Peewee ORM 3.17.0 |
| Relatórios | ReportLab 4.0.7 |
| Linguagem | Python 3.8+ |

---

## 📞 Suporte

Para dúvidas ou problemas, consulte:
1. **docs/00_LEIA_PRIMEIRO.txt** - Guia inicial
2. **docs/ARCHITECTURE.md** - Arquitetura técnica
3. **docs/README.md** - Documentação técnica completa

---

**Versão:** 1.0.0
**Atualizado:** Fevereiro de 2026
**Mantém:** PDV Team
