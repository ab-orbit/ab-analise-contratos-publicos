# Análise Avançada do Comércio Exterior de Pernambuco (v2)

## Visão Geral

O notebook `pe_imp_exp_v2.ipynb` oferece uma análise **muito mais rica e profunda** que a versão original, focando em:

- **Cadeias de produção** completas
- **Perfis detalhados** por município e país
- **Fluxos completos** origem → produto → destino
- **Especialização produtiva** e clusters
- **Análises de valor agregado** (US$/kg)

## Estrutura do Notebook (75 células)

### Seções Básicas (herdadas + melhoradas)

1. **Setup e Carregamento** - Ambiente e funções utilitárias
2. **Qualidade dos Dados** - Validação de cobertura e integridade
3. **Painel Executivo** - KPIs, evolução temporal, YTD
4. **Geografia Econômica Básica** - Top municípios e concentração

### Novas Seções Analíticas Avançadas

#### 4.3 Perfil Detalhado Municipal
**O que cada município comercializa?**

```python
perfil_municipio("Recife - PE", "Exportação")
```

**Retorna:**
- Top produtos exportados/importados
- Top destinos/origens
- Fluxos completos: município → produto → país
- Métricas de diversificação

**Exemplo de uso:**
```python
# Compara especialização dos top 5 municípios
# Mostra: quais produtos cada um vende e para onde
```

---

#### 5.2 Perfil de Parceiros Comerciais
**O que cada país compra/vende de/para Pernambuco?**

```python
perfil_parceiro("China", "Exportação")
perfil_parceiro("China", "Importação")
```

**Análises:**
- O que a China compra de PE (por produto e município)
- O que a China vende para PE (por produto e município)
- Comparação entre top parceiros
- Identificação de municípios fornecedores/importadores

**Responde:**
- Quais produtos a China importa de Ipojuca?
- Quais municípios vendem açúcar para a Índia?
- O que PE compra dos EUA e onde entra no estado?

---

#### 6.3 Cadeias e Fluxos Completos
**Mapeamento de cadeias de valor**

```python
analise_cadeias_completas("Exportação", top_n=20)
```

**Outputs:**
- Top 20 cadeias: Município → Produto → País
- Participação de cada cadeia no total
- Valor agregado (US$/kg) por cadeia
- Matriz Produto x País (heatmap)

**Exemplo de insights:**
- Cadeia mais valiosa: "Ipojuca → SH87 (veículos) → EUA"
- Concentração: top 20 cadeias = X% do comércio total
- Oportunidades: cadeias com alto valor agregado

---

#### 6.4 Especialização e Clusters
**Vocações produtivas e complementariedades**

**Análises incluídas:**

1. **Location Quotient (LQ)**
   - Mede especialização relativa
   - LQ > 1: município especializado naquele produto
   - Identifica vocações locais

2. **Perfil de Diversificação**
   - Classifica municípios: focado vs diversificado
   - Usa HHI da pauta municipal
   - Visualização comparativa

3. **Análise de Complementariedade**
   - Identifica municípios com pautas complementares
   - Municípios que exportam para mesmos destinos mas produtos diferentes
   - Oportunidades de sinergia e articulação

---

## Exemplos Práticos de Uso

### Caso 1: Entender o perfil exportador de Recife

```python
perfil = perfil_municipio("Recife - PE", "Exportação", top_n=10)

print(perfil['resumo'])  # Visão geral
display(perfil['top_produtos'])  # Top 10 produtos
display(perfil['top_paises'])  # Top 10 destinos
display(perfil['fluxos_principais'])  # Top 20 fluxos produto→país
```

### Caso 2: Analisar relação comercial com a China

```python
# O que PE vende para a China
exp_china = perfil_parceiro("China", "Exportação")
# Quais municípios fornecem? Quais produtos?

# O que PE compra da China
imp_china = perfil_parceiro("China", "Importação")
# Onde entram esses produtos em PE?
```

### Caso 3: Identificar cadeias prioritárias

```python
cadeias = analise_cadeias_completas("Exportação", top_n=30)

# Filtrar cadeias de alto valor agregado
cadeias_premium = cadeias[cadeias['usd_kg'] > 5.0]

# Ver concentração
print(f"Top 30 = {cadeias['share_total'].sum():.1f}% do total")
```

### Caso 4: Mapear especializações

```python
espec = calcular_especializacao("Exportação")

# Municípios especializados em açúcar (SH17)
espec_acucar = espec[espec['Código SH2'] == '17']
# LQ alto = especialização forte

# Ver diversificação
perfil_diversif  # Tabela com HHI e classificação
```

---

## Principais Diferenças vs Versão Original

| Aspecto | Versão Original | Versão v2 |
|---------|----------------|-----------|
| Células | 23 | 75 |
| Análise municipal | Agregada (top N) | Perfil completo individual |
| Análise de parceiros | Lista de países | Perfil produto x município |
| Cadeias | Não tinha | Fluxos completos município→produto→país |
| Especialização | Não tinha | Location Quotient + clusters |
| Complementariedade | Não tinha | Análise de sinergias municipais |
| Valor agregado | Básico | Análise detalhada por cadeia |
| Matrizes | Não tinha | Matriz produto x país (heatmap) |

---

## Casos de Uso

### Para Gestores Públicos
- Identificar vocações produtivas regionais
- Mapear oportunidades de articulação intermunicipal
- Priorizar cadeias para políticas de fomento
- Entender dependências e vulnerabilidades

### Para Pesquisadores
- Estudar especialização produtiva
- Analisar complementariedades territoriais
- Mapear inserção internacional por território
- Avaliar complexidade econômica local

### Para Setor Privado
- Identificar potenciais parceiros locais
- Mapear concorrentes por produto/destino
- Descobrir oportunidades de mercado
- Entender cadeias de valor existentes

### Para Analistas de Comércio Exterior
- Detalhar fluxos específicos
- Comparar perfis comerciais
- Identificar padrões e anomalias
- Gerar relatórios customizados

---

## Como Usar

1. **Execute as células sequencialmente** ou use "Restart & Run All"

2. **Para análise específica de um município:**
   ```python
   perfil_municipio("Seu Município - PE", "Exportação")
   ```

3. **Para análise de um país parceiro:**
   ```python
   perfil_parceiro("Nome do País", "Exportação")
   ```

4. **Para explorar uma cadeia específica:**
   ```python
   # Filtre o DataFrame de cadeias
   cadeias[cadeias['Código SH2'] == 'XX']
   ```

5. **Para análises customizadas:**
   - As funções são modulares
   - Você pode modificar parâmetros (top_n, min_valor, etc.)
   - Pode filtrar e reagrupar os DataFrames resultantes

---

## Requisitos

```python
pandas >= 1.3
numpy >= 1.20
matplotlib >= 3.3
seaborn >= 0.11
```

---

## Estrutura de Dados

O notebook trabalha com três DataFrames principais:

- `df`: Dados deduplicados para totais (sem duplicação de blocos)
- `df_block`: Dados com um bloco por transação (para análise de blocos)
- `df_raw`: Dados originais completos

Principais colunas:
- `Município`, `País`, `Fluxo` (Exportação/Importação)
- `Código SH2`, `Descrição SH2` (produto)
- `Valor US$ FOB`, `Quilograma Líquido`
- `Bloco Econômico`, `Data`, `Ano`, `MesNum`

---

## Próximas Expansões Possíveis

1. **Análise de complexidade econômica** (índice de complexidade de produtos)
2. **Análise temporal de cadeias** (evolução de fluxos ao longo do tempo)
3. **Análise de resiliência** (vulnerabilidade a choques por concentração)
4. **Network analysis** (grafos de relacionamento município-país-produto)
5. **Análise setorial NCM** (aprofundamento por seções e capítulos)
6. **Benchmark internacional** (comparação com outros estados)

---

## Contato e Contribuições

Para dúvidas, sugestões ou relatórios de problemas, consulte a documentação do projeto.
