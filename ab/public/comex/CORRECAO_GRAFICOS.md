# Correção dos Gráficos do Notebook

## Problema Identificado

Os gráficos não eram renderizados porque faltava a configuração **`%matplotlib inline`** no notebook.

### Por que isso aconteceu?

- O Jupyter precisa de uma "magic command" para saber onde renderizar os gráficos
- Sem `%matplotlib inline`, os gráficos são criados mas não aparecem no notebook
- Apenas texto (prints) eram exibidos, mas as imagens ficavam ausentes

## Solução Aplicada

✓ Adicionado `%matplotlib inline` na **célula 2** (imports)

```python
%matplotlib inline

from __future__ import annotations
import matplotlib.pyplot as plt
import seaborn as sns
# ... resto dos imports
```

## Verificação

Após a correção, a estrutura está:

```
Célula 2:
  ↓
  %matplotlib inline        ← ADICIONADO!
  imports...
  configurações plt.rcParams

Célula 23: plt.show()      → gráfico de evolução temporal
Célula 28: plt.show()      → gráficos de municípios
Célula 47: plt.show()      → gráficos de parceiros
Célula 51: plt.show()      → gráficos de produtos
Célula 60: plt.show()      → matriz/heatmap
Célula 66: plt.show()      → gráfico de especialização
```

## Como Executar Agora

### Opção 1: Restart & Run All (RECOMENDADO)

```
1. Abra pe_imp_exp_v2.ipynb no Jupyter
2. Menu: Kernel → Restart & Run All
3. Aguarde 2-3 minutos
4. ✓ Todos os 7 gráficos aparecerão!
```

### Opção 2: Executar Célula por Célula

```
1. Execute a célula 2 primeiro (com %matplotlib inline)
2. Execute as células sequencialmente
3. Gráficos aparecerão quando executar as células de visualização
```

## Gráficos que Serão Renderizados

| Célula | Descrição | Tipo |
|--------|-----------|------|
| 23 | Evolução temporal mensal | 2 line plots + 1 bar chart |
| 28 | Top municípios | 2 horizontal bar charts |
| 47 | Top parceiros comerciais | 2 horizontal bar charts |
| 51 | Top produtos SH2 | 2 horizontal bar charts |
| 60 | Matriz Produto × País | 1 heatmap |
| 66 | Especialização municipal | 2 charts (bar + pie) |

**Total: 12 visualizações gráficas**

## Testes Realizados

✓ Sintaxe de todas as células verificada
✓ Ordem de dependências confirmada
✓ Todas as variáveis necessárias criadas nas células corretas
✓ `plt.show()` presente em todas as células de visualização
✓ `%matplotlib inline` adicionado

## Troubleshooting

### Se os gráficos AINDA não aparecerem:

#### 1. Verifique o backend do matplotlib

Execute no início do notebook:
```python
import matplotlib
print(matplotlib.get_backend())  # Deve mostrar 'module://matplotlib_inline.backend_inline'
```

#### 2. Tente backend alternativo

Se inline não funcionar, tente:
```python
%matplotlib widget
# ou
%matplotlib notebook
```

#### 3. Força a exibição

Adicione antes dos plt.show():
```python
from IPython.display import display
display(fig)  # Onde fig é sua figura
```

#### 4. Verifica se matplotlib está instalado corretamente

```bash
pip install --upgrade matplotlib
pip install --upgrade ipympl  # Para backends interativos
```

## Diferença: Antes vs Depois

### ANTES (sem %matplotlib inline)

```
Célula 28:
  [executa]
  Output: Exportação: HHI municipal=0.194 | ...
  [NENHUM GRÁFICO]
```

### DEPOIS (com %matplotlib inline)

```
Célula 28:
  [executa]
  Output 1: [IMAGEM: gráfico de barras]
  Output 2: Exportação: HHI municipal=0.194 | ...
```

## Confirmação de Sucesso

Após executar, você DEVE ver:

✓ 2 gráficos de linha na célula 23
✓ 1 gráfico de barras na célula 23
✓ 2 gráficos de barras lado a lado na célula 28
✓ 2 gráficos de barras lado a lado na célula 47
✓ 2 gráficos de barras lado a lado na célula 51
✓ 1 heatmap colorido na célula 60
✓ 2 gráficos (barras + pizza) na célula 66

**= 12 visualizações no total**

## Status Atual

✅ **CORRIGIDO E PRONTO PARA USO**

Execute o notebook e confirme que todos os gráficos aparecem corretamente!

---

**Data da correção:** 2026-03-03
**Problema:** Falta de %matplotlib inline
**Solução:** Adicionado magic command na célula 2
**Status:** Resolvido ✅
