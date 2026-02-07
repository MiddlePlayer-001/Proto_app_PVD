# 📝 GUIA: Sistema de Logging PDV

## 🎯 O que foi implementado?

Um sistema robusto de logging estruturado que rastreia TODAS as operações críticas do PDV:

✅ **Transações de vendas** - Início, itens adicionados, finalizações  
✅ **Operações de estoque** - Ajustes, validações, decrementos  
✅ **Movimentações financeiras** - Registros de transações  
✅ **Erros e exceções** - Com stack trace completo  
✅ **Performance** - Alertas para operações lentas  

---

## 📂 Arquivos de Log

Os logs são salvos em `logs/` na raiz do projeto:

```
pdv_system/
└── logs/
    ├── pdv_system.log       # Todos os logs (rotativo, máx 10MB)
    └── pdv_errors.log       # Apenas erros (rotativo, máx 5MB)
```

### Exemplos de conteúdo:

**pdv_system.log:**
```
06/02/2026 10:15:32 - pdv_system - INFO - ======================================================================
06/02/2026 10:15:32 - pdv_system - INFO - INICIANDO PDV SYSTEM v1.0.0
06/02/2026 10:15:32 - pdv_system - INFO - ======================================================================
06/02/2026 10:15:33 - pdv_system - INFO - Banco de dados inicializado com sucesso
06/02/2026 10:15:35 - pdv_system - INFO - [VENDA #1] INICIADA | Forma: Dinheiro
06/02/2026 10:15:38 - pdv_system - DEBUG - Item adicionado à venda #1: PROD001 x 2
06/02/2026 10:15:42 - pdv_system - INFO - Produto criado: PROD002 - Kleenex (Estoque: 50)
06/02/2026 10:15:45 - pdv_system - INFO - [VENDA #1] FINALIZADA | Total: R$ 125.50, Troco: R$ 24.50
```

**pdv_errors.log:**
```
06/02/2026 10:16:22 - pdv_system - ERROR - Estoque insuficiente ao adicionar PROD001 | estoque_disponivel=5, quantidade_solicitada=10
06/02/2026 10:16:25 - pdv_system - ERROR - Erro ao criar venda: Venda ou Produto não encontrado | ...
```

---

## 🔧 Como Usar

### 1. **Em um Service/Repository**

```python
from src.utils.logger import log_info, log_error, log_debug, log_venda

# Log de informação
log_info("Operação realizada com sucesso")

# Log de erro
try:
    fazer_algo()
except Exception as e:
    log_error(f"Erro: {e}", exc_info=True)

# Log de debug (só em desenvolvimento)
log_debug("Valor da variável: " + str(valor))

# Log específico de venda
log_venda(numero_venda=1, acao="INICIADA", detalhes="Forma: Dinheiro")
```

### 2. **Com Informações Adicionais**

```python
log_info("Venda criada", usuario="João", forma="PIX")
# Output: INFO - Venda criada | {'usuario': 'João', 'forma': 'PIX'}

log_error("Erro crítico", exc_info=True, venda_id=123)
# Também exibe stack trace completo
```

### 3. **Padrões Recomendados**

#### Para Vendas:
```python
log_venda(numero=venda.numero, acao="FINALIZADA", detalhes=f"Total: R$ {total:.2f}")
```

#### Para Estoque:
```python
log_info(f"Estoque ajustado para {produto.codigo}: {abs(qtd)} un. (Total: {novo_estoque})")
```

#### Para Erros:
```python
log_error(f"Falha ao processar: {erro}", exc_info=True, operacao="finalizar_venda")
```

---

## 📊 Níveis de Log

| Nível | Uso | Arquivo |
|-------|-----|---------|
| **DEBUG** | Rastreamento detalhado (desativar em produção) | pdv_system.log |
| **INFO** | Operações normais importantes | pdv_system.log |
| **WARNING** | Situações incomuns (performance lenta) | pdv_system.log |
| **ERROR** | Erros que não interrompem a app | ambos |
| **CRITICAL** | Erros que interrompem a app | ambos |

---

## 🔍 Consultando Logs

### 1. **Em Tempo Real**
```bash
# Windows PowerShell
Get-Content logs/pdv_system.log -Wait
```

### 2. **Últimas 100 linhas**
```bash
# Windows
type logs\pdv_system.log | tail -100
```

### 3. **Erros do dia**
```bash
# Buscar erros
Select-String "ERROR" logs/pdv_errors.log
```

### 4. **Vendas específicas**
```bash
# Buscar venda #5
Select-String "\[VENDA #5\]" logs/pdv_system.log
```

---

## ⚙️ Configuração

### Alterar Nível de Log

Editar em `src/utils/logger.py`:

```python
# Linha ~40
file_handler.setLevel(logging.DEBUG)  # Alterar para INFO em produção

console_handler.setLevel(logging.INFO)  # Aumentar para WARNING se muito verbose
```

### Desativar Logs em Arquivo

```python
# Comentar handlers em _initialize():
# file_handler = RotatingFileHandler(...)
# self.logger.addHandler(file_handler)
```

---

## 📌 Checklist: O que registrar?

- ✅ Criação de vendas
- ✅ Adição de itens ao carrinho
- ✅ Validações de estoque
- ✅ Finalização de vendas
- ✅ Cancelamento de vendas
- ✅ Ajustes de estoque
- ✅ Erros e exceções
- ✅ Startup/shutdown da aplicação

---

## 🚀 Exemplo Completo de Uso

```python
from src.utils.logger import log_info, log_error, log_venda

def exemplo_venda():
    try:
        log_venda(numero=1, acao="INICIADA", detalhes="Dinheiro")
        
        # Adicionar itens
        log_info("Item adicionado: PROD001 x 2")
        
        # Finalizar
        total = 100.00
        troco = 50.00
        log_venda(numero=1, acao="FINALIZADA", detalhes=f"Total: R$ {total:.2f}, Troco: R$ {troco:.2f}")
        
    except ValueError as e:
        log_error(f"Erro na venda: {e}", exc_info=True)
```

**Output em pdv_system.log:**
```
INFO - [VENDA #1] INICIADA - Dinheiro
INFO - Item adicionado: PROD001 x 2
INFO - [VENDA #1] FINALIZADA - Total: R$ 100.00, Troco: R$ 50.00
```

---

## 💡 Benefícios

✅ **Auditoria completa** - Rastreie cada operação  
✅ **Debugging rápido** - Encontre erros facilmente  
✅ **Performance monitoring** - Veja operações lentas  
✅ **Conformidade** - Registros para prestação de contas  
✅ **Segurança** - Identifique padrões suspeitos  

---

## 📞 Suporte

Dúvidas? Verifique:
- `src/utils/logger.py` - Implementação
- `src/models/venda_repository.py` - Exemplo de uso em repositório
- `src/services/venda_service.py` - Exemplo de uso em serviço

