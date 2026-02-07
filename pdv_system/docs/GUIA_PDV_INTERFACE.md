# 💳 INTERFACE PDV EM FLET - DOCUMENTAÇÃO

## 📋 Overview

A interface PDV (Ponto de Venda) foi desenvolvida em Flet com layout responsivo:
- **Esquerda (70%):** Carrinho com grid de produtos
- **Direita (30%):** Busca, totalizadores e botões de ação

---

## 🎨 Layout

### Desktop (1000px+)
```
┌────────────────────────────────────────────────┬──────────────────┐
│                                                │                  │
│         CARRINHO DE COMPRAS (70%)              │  BUSCA (30%)     │
│                                                │                  │
│  Item         Qtd    Preço      Total  Remov   │  🔍 Produto      │
│  ─────────────────────────────────────────     │                  │
│  Coca-Cola    2x     R$ 5,99    R$ 11,98  ✕   │  RESUMO          │
│  Agua Min.    3x     R$ 2,50    R$ 7,50   ✕   │  ────────        │
│  Salgado      1x     R$ 3,50    R$ 3,50   ✕   │  Subtotal: R$    │
│                                                │  Desconto: R$    │
│  [Scroll...]                                   │  ────────        │
│                                                │  TOTAL: R$       │
│                                                │                  │
│                                                │  [Botões Desc]   │
│                                                │  [FINALIZAR]     │
│                                                │  [CANCELAR]      │
│                                                │                  │
└────────────────────────────────────────────────┴──────────────────┘
```

### Mobile (<1000px)
```
┌────────────────────────────────┐
│     CARRINHO DE COMPRAS         │
│                                │
│  Item         Qtd   Preço      │
│  ─────────────────────────────  │
│  Coca-Cola    2x    R$ 11,98   │
│  Agua Min.    3x    R$ 7,50    │
│                                │
│                 [Flutuante →]   │
│                 [FINALIZAR]     │
│                 [CANCELAR]      │
│                                │
└────────────────────────────────┘
```

---

## 🔧 Componentes

### 1. Campo de Busca
```python
self.campo_busca = ft.TextField(
    label="🔍 Código ou Nome do Produto",
    autofocus=True,
    on_submit=lambda e: self._buscar_e_adicionar_produto(e.control.value),
)
```
- **Foco automático** ao abrir/iniciar nova venda
- **Enter submete** a busca
- Aceita **código** ou **nome** do produto
- Busca **case-insensitive**

### 2. Carrinho (ListView)
```python
self.lista_carrinho = ft.ListView(
    auto_scroll=True,
    expand=True,
)
```
- **Auto-scroll** ao adicionar itens
- **Edição de quantidade** inline
- **Botão de remoção** por item
- **Cálculo automático** de subtotais

### 3. Totalizadores
```
Subtotal:  R$ 22.98
Desconto:  R$ 2.30
────────────────────
TOTAL:     R$ 20.68
```

### 4. Botões de Ação
| Botão | Função | Cor |
|-------|--------|-----|
| 10% | Desconto 10% | Orange |
| 20% | Desconto 20% | Orange |
| R$50 | Desconto R$50 | Orange |
| FINALIZAR (F5) | Salva venda | Verde |
| CANCELAR (ESC) | Cancela venda | Vermelho |

---

## 🔄 Fluxo de Uso

### 1. Iniciar Venda
```
[PDV abre]
  ↓
[Venda nova criada em memória]
  ↓
[Campo de busca com foco automático]
```

### 2. Adicionar Produtos
```
[Usuário digita código/nome]
  ↓
[Pressiona ENTER ou clica Adicionar]
  ↓
[Sistema busca produto]
  ↓
[Verifica estoque]
  ↓
[Se OK] → Adiciona ao carrinho
[Se erro] → Mostra SnackBar
  ↓
[Campo limpo, foco restaurado]
  ↓
[Carrinho atualizado]
```

### 3. Editar Quantidade
```
[Usuário clica no campo QTD]
  ↓
[Edita quantidade]
  ↓
[Pressiona ENTER ou sai do campo]
  ↓
[Valida estoque]
  ↓
[Atualiza subtotal]
```

### 4. Aplicar Desconto
```
[Usuário clica botão de desconto]
  ↓
[Calcula percentual ou valor fixo]
  ↓
[Subtrai do total]
  ↓
[Atualiza display]
```

### 5. Finalizar Venda
```
[Usuário clica FINALIZAR ou F5]
  ↓
[Valida carrinho não vazio]
  ↓
[Adiciona itens à venda no DB]
  ↓
[Aplica desconto se houver]
  ↓
[Finaliza venda → decremente estoque]
  ↓
[Cria MovimentoFinanceiro automaticamente]
  ↓
[Simula impressão (console)]
  ↓
[Mostra sucesso]
  ↓
[Limpa carrinho, inicia nova venda]
```

---

## 💾 Lógica de Persistência

### Ao Finalizar Venda
1. **Venda** salva em `vendas` table
2. **ItemVenda** salvo para cada item
3. **Estoque** decrementado em Produto
4. **Transacao** criada **AUTOMATICAMENTE**
   - tipo: ENTRADA
   - categoria: VENDA
   - valor: total com desconto
   - venda_id: FK para Venda

### Validações
- ✅ Produto deve existir e estar ativo
- ✅ Quantidade ≤ estoque
- ✅ Estoque decrementado apenas ao finalizar
- ✅ Desconto ≤ total
- ✅ Carrinho não vazio ao finalizar

---

## 📱 Responsividade

```python
if self.page.width and self.page.width > 1000:
    # Desktop: layout lado a lado (70% + 30%)
else:
    # Mobile: botões flutuantes (Stack)
```

---

## 🎯 Atalhos de Teclado

| Tecla | Ação |
|-------|------|
| **F5** | FINALIZAR venda |
| **ESC** | CANCELAR venda |
| **ENTER** | Buscar/adicionar produto |

---

## 📊 Exemplo de Cupom Impresso

```
╔════════════════════════════════════════════════════════════╗
║                      PDV - CUPOM DE VENDA                 ║
╚════════════════════════════════════════════════════════════╝

Venda Nº: 1
Data/Hora: 2026-02-06 14:32:41
────────────────────────────────────────────────────────────

ITENS:
Coca-Cola 2L
  2 x R$ 5.99 = R$ 11.98
Agua Mineral 1,5L
  3 x R$ 2.50 = R$ 7.50
Salgado Misto
  1 x R$ 3.50 = R$ 3.50
────────────────────────────────────────────────────────────
Subtotal:                              R$ 22.98
Desconto:                              R$ 2.30
TOTAL:                                 R$ 20.68
────────────────────────────────────────────────────────────

Forma de Pagamento: Dinheiro
Valor Pago: R$ 20.68

╔════════════════════════════════════════════════════════════╗
║                     OBRIGADO PELA COMPRA!                 ║
║                      VOLTE SEMPRE! 👋                      ║
╚════════════════════════════════════════════════════════════╝
```

---

## 🔌 Integração com Serviços

### VendaService
- `iniciar_venda()` - Cria venda nova
- `adicionar_item_carrinho()` - Adiciona item
- `remover_item_carrinho()` - Remove item
- `aplicar_desconto()` - Desconto
- `finalizar_venda()` - Finaliza (cria Transacao)
- `cancelar_venda()` - Cancela

### ProdutoService
- `buscar_produtos()` - Busca por termo
- `obter_produto()` - Busca por ID
- `obter_valor_total_estoque()` - Valuation

### FinanceiroService
- `criar_fechamento()` - Fechamento diário (futuro)
- `obter_resumo_dia()` - Resumo do dia (futuro)

---

## 🛠️ Classe PDVView

### Atributos
```python
self.venda_id          # ID da venda atual
self.itens_carrinho    # Dict {produto_id: item}
self.total             # Total com desconto
self.desconto          # Valor de desconto
```

### Métodos Principais
```python
criar_interface()               # Cria UI
_buscar_e_adicionar_produto()  # Busca e adiciona
_atualizar_carrinho()          # Atualiza visualização
_finalizar_venda()             # Finaliza e salva
_cancelar_venda()              # Cancela
_simular_impressao()           # Imprime cupom
```

---

## 🧪 Como Testar

### 1. Executar teste de lógica
```bash
python test_pdv_interface.py
```

### 2. Executar interface (após OK no teste)
```bash
python main.py
```

### 3. Navegar para PDV
- Click em "💳 Vendas/PDV"

### 4. Teste manual
```
1. Digite "COK" no campo de busca
2. Pressione ENTER
3. Digite "AGU" → ENTER
4. Click em desconto "10%"
5. Click em "FINALIZAR"
6. Veja cupom no console
7. Verifique banco: estoque decrementado
8. Verifique banco: transação criada
```

---

## 📦 Arquivos

| Arquivo | Descrição |
|---------|-----------|
| `src/ui/pdv_view.py` | Classe PDVView (interface completa) |
| `src/ui/main_app.py` | Integração com Flet (atualizado) |
| `test_pdv_interface.py` | Testes de lógica |

---

## ✅ Checklist

- [x] Layout 70% esquerda (carrinho) + 30% direita (busca/total)
- [x] Campo de busca com foco automático
- [x] Grid de produtos no carrinho
- [x] Edição de quantidade inline
- [x] Botões de remoção
- [x] Display grande de TOTAL
- [x] Atalhos de desconto (10%, 20%, R$50)
- [x] Botão FINALIZAR com verificações
- [x] Botão CANCELAR
- [x] Verificação de estoque
- [x] Decremento automático ao finalizar
- [x] Criação automática de Transacao
- [x] Simulação de impressão
- [x] SnackBar com mensagens
- [x] Responsividade (desktop/mobile)
- [x] Testes validando lógica

---

**Status:** ✅ **IMPLEMENTADO E TESTADO**

Versão: 1.0.0 | Data: 06/02/2026
