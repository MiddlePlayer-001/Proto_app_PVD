# ✅ PROCESSO DE INSTALAÇÃO - PDV SYSTEM

## 🎯 RESUMO: Sim, você consegue instalar!

O aplicativo PDV System está **100% pronto para ser instalado** e usado. Não precisa fazer nada complexo.

---

## 📋 PASSOS PARA INSTALAR (Windows, Linux ou Mac)

### 1️⃣ **Pré-requisitos** (5 minutos)
- [ ] Tenha **Python 3.8+** instalado 
  - Baixe de: https://www.python.org/downloads/
  - **Importante:** Marque "Add Python to PATH" durante a instalação

**Verificar se Python está instalado:**
```bash
python --version
```

---

### 2️⃣ **Abra o Terminal/PowerShell**

**Windows:**
- Aperte `Win + R` → Digite `powershell` → Enter

**Linux/Mac:**
- Abra o Terminal normalmente

---

### 3️⃣ **Navegue até a Pasta do Projeto**

```bash
cd C:\Users\SeuUsuario\Downloads\aplicativo\pdv_system
```

(Substituir por seu caminho real)

---

### 4️⃣ **Crie um Ambiente Virtual**

```bash
python -m venv venv
```

**Isso cria uma pasta** `venv/` **com Python isolado (recomendado)**

---

### 5️⃣ **Ative o Ambiente Virtual**

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

Você verá: `(venv) C:\...>` no terminal

---

### 6️⃣ **Instale as Dependências**

```bash
pip install -r requirements.txt
```

**Tempo estimado:** 2-5 minutos (primeira vez)

O terminal mostrará:
```
Successfully installed flet-0.23.0 peewee-3.17.0 reportlab-4.0.7 ...
```

---

### 7️⃣ **Execute a Aplicação! 🚀**

```bash
python main.py
```

**O que vai acontecer:**
- ✓ Banco de dados será criado (`data/loja.db`)
- ✓ Interface gráfica abrirá em segundos
- ✓ Sistema já funciona com dados de exemplo!

---

## 🔁 PRÓXIMAS VEZES

Na próxima vez, basta:

```bash
cd C:\Users\SeuUsuario\Downloads\aplicativo\pdv_system
venv\Scripts\activate  # ou source venv/bin/activate no Linux/Mac
python main.py
```

Será **quase instantâneo** (não precisa instalar novamente).

---

## 🛑 ERROS COMUNS E SOLUÇÕES

| Erro | Solução |
|------|---------|
| `Python não reconhecido` | Reinstale Python marcando "Add to PATH" |
| `Permission denied` (Linux/Mac) | Use `chmod +x` nos scripts |
| `ModuleNotFoundError` | Execute `pip install -r requirements.txt` novamente |
| `venv não funciona` | Delete a pasta `venv/` e crie uma nova |

---

## 📊 ESTRUTURA DO PROJETO

```
pdv_system/
├── main.py                    ← Arquivo principal (execute este)
├── requirements.txt           ← Dependências para instalar
├── src/                       ← Código-fonte (não mexer)
├── data/                      ← Banco de dados (criado automaticamente)
├── dist/                      ← Executáveis compilados (opcional)
├── config/                    ← Configurações (.env.example)
└── docs/                      ← Documentação completa
```

---

## 🚀 ALTERNATIVA: INSTALADOR AUTOMÁTICO

Se não quiser usar terminal, use o instalador:

- Arquivo: `dist/INSTALLER.exe`
- Clique 2x → Escolha a pasta → Pronto!
- Levará 2-3 minutos na primeira vez
- Depois é só usar!

---

## ✅ CHECKLIST DE INSTALAÇÃO

- [ ] Python 3.8+ instalado e verificado
- [ ] Ambiente virtual criado e ativado
- [ ] Dependências instaladas com `pip install -r requirements.txt`
- [ ] Nenhum erro no terminal
- [ ] Banco de dados criado em `data/loja.db`
- [ ] Interface gráfica abrindo sem erros

---

## 📚 MAIS INFORMAÇÕES

- **Guia completo:** Veja `docs/README.md`
- **Arquitetura:** Veja `docs/ARCHITECTURE.md`
- **Deploy em produção:** Veja `docs/DEPLOYMENT_GUIDE.md`

---

## ❓ AINDA COM DÚVIDAS?

Antes de mais nada:
1. Verifique se Python está instalado: `python --version`
2. Verifique se dependências foram instaladas: `pip list`
3. Tente deletar `venv/` e começar do zero

Se mesmo assim não funcionar, verifique os logs em `docs/GUIA_LOGGING.md`

---

**Pronto! Seu PDV System está instalado e funcionando! 🎉**

