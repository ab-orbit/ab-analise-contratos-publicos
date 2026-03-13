# Instruções para Executar o Notebook pe_imp_exp_v2.ipynb

## Por que os gráficos não aparecem?

Os gráficos **NÃO estão pré-renderizados** no notebook. Eles serão gerados quando você **executar as células de código**.

### Status Atual

✓ **6 de 7 células de visualização** foram executadas (do notebook original)
○ **1 célula nova** ainda não foi executada
✓ **Nenhum erro de sintaxe** encontrado
✓ **Todas as dependências** estão na ordem correta

## Como Executar o Notebook

### Opção 1: Executar Tudo de Uma Vez (RECOMENDADO)

1. Abra o notebook no Jupyter
2. Vá em: **Kernel → Restart & Run All**
3. Aguarde a execução completa (pode levar 2-5 minutos)
4. Todos os gráficos serão gerados automaticamente

### Opção 2: Executar Célula por Célula

1. Abra o notebook no Jupyter
2. Clique na primeira célula de código
3. Pressione **Shift + Enter** para executar e avançar
4. Repita para cada célula
5. Os gráficos aparecerão conforme você executa

### Opção 3: Executar Apenas Seções Específicas

Se você já executou as células básicas e quer apenas rodar as análises avançadas:

1. Execute primeiro as células de setup (células 1-8)
2. Execute as células de dados básicos (células 9-23)
3. Depois execute qualquer seção específica de interesse

## Ordem de Execução Obrigatória

**IMPORTANTE:** Respeite a ordem das células! Algumas análises dependem de variáveis criadas anteriormente.

### Variáveis Críticas e Onde São Definidas:

| Variável | Célula | Necessária Para |
|----------|--------|-----------------|
| `df`, `df_raw`, `df_block` | 8 | Todas as análises |
| `exp_mun`, `imp_mun` | 26 | Análise municipal avançada |
| `exp_country`, `imp_country` | 37 | Análise de parceiros |
| `exp_sh2`, `imp_sh2` | 49 | Análise de produtos |
| `monthly` | 19 | Gráficos temporais |
| `ytd` | 21 | Comparações YTD |

## Células com Visualizações (Gráficos)

O notebook contém **7 células principais** com visualizações:

1. **Célula 2**: Setup dos estilos de gráficos (matplotlib/seaborn)
2. **Célula 23**: Evolução temporal (2 gráficos)
   - Exportações vs Importações mensal
   - Saldo mensal em barras
3. **Célula 28**: Top municípios (2 gráficos de barras)
   - Exportadores
   - Importadores
4. **Célula 47**: Top parceiros (2 gráficos de barras)
   - Destinos de exportação
   - Origens de importação
5. **Célula 51**: Top produtos SH2 (2 gráficos de barras)
   - Produtos exportados
   - Produtos importados
6. **Célula 60**: Matriz de fluxos (1 heatmap)
   - Produtos x Países
7. **Célula 66**: Especialização municipal (2 gráficos)
   - HHI por município
   - Distribuição por tipo

## Tempo Estimado de Execução

| Seção | Tempo Aproximado |
|-------|-----------------|
| Setup e carregamento | 10-15 segundos |
| Qualidade dos dados | 5-10 segundos |
| Painel executivo | 15-20 segundos |
| Análises municipais | 20-30 segundos |
| Análises de parceiros | 15-20 segundos |
| Análises de produtos | 15-20 segundos |
| Cadeias e clusters | 30-40 segundos |
| **TOTAL** | **2-3 minutos** |

## Requisitos de Execução

### Bibliotecas Necessárias

Todas já devem estar instaladas, mas se houver erro:

```bash
pip install pandas numpy matplotlib seaborn jupyter
```

### Dados

O notebook procura automaticamente o arquivo CSV em:
- `data/pe/comex/V_EXPORTACAO_E IMPORTACAO_POR MUNICIPIO_2024-01_2026-12_DT20260303.csv`
- `../../data/pe/comex/...`
- `../../../data/pe/comex/...`

Certifique-se de que o arquivo está em um desses locais.

## Troubleshooting

### Erro: "FileNotFoundError"
**Problema:** Arquivo de dados não encontrado
**Solução:** Verifique o caminho do arquivo CSV ou ajuste a função `resolve_data_path()`

### Erro: "NameError: name 'df' is not defined"
**Problema:** Tentou executar células fora de ordem
**Solução:** Execute "Restart & Run All" para garantir ordem correta

### Erro: "KeyError" ou "AttributeError"
**Problema:** Dados podem ter formato diferente do esperado
**Solução:** Verifique se o arquivo CSV é o mesmo usado no desenvolvimento

### Gráficos aparecem muito pequenos
**Solução:** Ajuste o parâmetro `figsize` nas células de visualização:
```python
fig, ax = plt.subplots(figsize=(20, 8))  # Aumenta o tamanho
```

### Gráficos não aparecem inline
**Solução:** Execute no início do notebook:
```python
%matplotlib inline
```

## Verificação Pós-Execução

Após executar todo o notebook, você deve ver:

✓ Mensagens de confirmação de carregamento
✓ Tabelas com dados agregados
✓ 7 visualizações gráficas completas
✓ Matriz de fluxos com heatmap
✓ Análises textuais de especialização

## Exportando Resultados

### Salvar o Notebook com Outputs

Após executar, salve o notebook:
- **File → Save and Checkpoint**

Isso manterá os gráficos visíveis quando reabrir.

### Exportar para HTML (com gráficos)

```bash
jupyter nbconvert --to html pe_imp_exp_v2.ipynb
```

### Exportar para PDF

```bash
jupyter nbconvert --to pdf pe_imp_exp_v2.ipynb
```

## Suporte

Se encontrar problemas:

1. Verifique se todas as bibliotecas estão instaladas
2. Confirme que o arquivo de dados está acessível
3. Tente "Kernel → Restart & Clear Output" seguido de "Run All"
4. Verifique se há mensagens de erro específicas nas células

---

**Última atualização:** 2026-03-03
**Versão do notebook:** v2 (75 células)
