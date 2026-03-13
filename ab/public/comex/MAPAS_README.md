# Visualizações Geográficas - Mapas de Comércio Exterior

## Nova Seção Adicionada: 4.4 Visualização Geográfica

Agora o notebook inclui **visualizações espaciais** do comércio exterior de Pernambuco!

## O que foi adicionado?

### 1. Verificação de Bibliotecas de Mapas

O notebook detecta automaticamente quais bibliotecas estão disponíveis:
- **Plotly** - Mapas interativos modernos
- **Folium** - Mapas web interativos
- **GeoPandas** - Análise geoespacial avançada

Se nenhuma estiver instalada, o notebook usa **matplotlib** (sempre disponível).

### 2. Coordenadas Geográficas

Cadastradas coordenadas de 21 municípios principais:
- Recife, Jaboatão, Olinda
- Ipojuca, Cabo de Santo Agostinho, Goiana
- Caruaru, Petrolina, Garanhuns
- E mais...

### 3. Mapas Incluídos

#### 3.1 Mapa de Bolhas Interativo (Plotly)

**Características:**
- 2 mapas lado a lado (exportação + importação)
- Tamanho das bolhas = valor comercializado
- Cor = intensidade do valor
- Interativo: passe o mouse para ver detalhes
- Zoom e pan disponíveis

**Instalação necessária:**
```bash
pip install plotly
```

#### 3.2 Mapa Estático (Matplotlib)

**Características:**
- Sempre funciona (não precisa instalar nada)
- 2 mapas lado a lado
- Bolhas proporcionais ao valor
- Top 5 municípios anotados
- Coloração por escala de valor

**Não precisa instalar nada!**

#### 3.3 Análise de Concentração Geográfica

**Análises incluídas:**

1. **Região Metropolitana do Recife (RMR)**
   - Calcula % do comércio total concentrado na RMR
   - Identifica dependência da região metropolitana

2. **Litoral vs Interior**
   - Compara municípios litorâneos vs interior
   - Mostra distribuição espacial do comércio

## Como Usar

### Executar os Mapas

1. **Abra o notebook**
   ```bash
   jupyter notebook pe_imp_exp_v2.ipynb
   ```

2. **Execute as células da seção 4.4**
   - Células incluem verificação automática de bibliotecas
   - Mapas são gerados automaticamente

3. **Se quiser mapas interativos** (opcional):
   ```bash
   pip install plotly
   ```
   Execute novamente: `Kernel → Restart & Run All`

### O que você verá

#### Com Plotly instalado:
- ✓ Mapa interativo com zoom e pan
- ✓ Hover mostra detalhes do município
- ✓ Cores e tamanhos dinâmicos

#### Sem Plotly (só matplotlib):
- ✓ Mapas estáticos funcionais
- ✓ Visualização clara da distribuição
- ✓ Top 5 municípios identificados

## Exemplos de Insights Visuais

### Mapa de Exportações
```
Você verá:
- Bolha GRANDE em Ipojuca (complexo de Suape)
- Bolhas médias em Recife, Goiana, Cabo
- Concentração no litoral
```

### Mapa de Importações
```
Você verá:
- Bolha ENORME em Recife (principal porto)
- Concentração muito forte na RMR
- Interior com baixa participação
```

### Análise de Concentração
```
Exemplo de output:

Exportação:
  Total PE: US$ 4,63 bi
  Total RMR: US$ 3,85 bi
  Concentração RMR: 83.2% do estado

Litoral vs Interior:
  Litoral: US$ 4,20 bi (90.7%)
  Interior: US$ 430 mi (9.3%)
```

## Estrutura das Células

| Célula | Tipo | Descrição |
|--------|------|-----------|
| 4.4.1 | Markdown | Introdução aos mapas |
| - | Code | Verifica bibliotecas disponíveis |
| - | Code | Define coordenadas dos municípios |
| 4.4.2 | Markdown | Intro mapa de bolhas |
| - | Code | Prepara dados para mapa |
| - | Code | Cria mapa interativo (Plotly) |
| 4.4.3 | Markdown | Intro mapa alternativo |
| - | Code | Cria mapa estático (Matplotlib) |
| 4.4.4 | Markdown | Intro análise espacial |
| - | Code | Análise concentração geográfica |

## Personalização

### Adicionar mais municípios

Edite o dicionário `municipios_coords`:
```python
municipios_coords = {
    "Seu Município - PE": (latitude, longitude),
    # Ex: "Salgueiro - PE": (-8.0742, -39.1198)
}
```

### Mudar número de municípios no mapa

```python
# Padrão: top 20
map_data_exp = preparar_dados_mapa("Exportação", top_n=30)  # top 30
```

### Mudar cores do mapa

**Plotly:**
```python
colorscale="Viridis"  # Pode ser: "Blues", "Greens", "Reds", "Portland", etc.
```

**Matplotlib:**
```python
cmap="viridis"  # Pode ser: "plasma", "inferno", "coolwarm", etc.
```

## Análises Possíveis com os Mapas

### 1. Identificação de Clusters
Visualmente identifica concentrações geográficas:
- Polo de Suape (Ipojuca + Cabo)
- Corredor metropolitano (RMR)
- Polos isolados (Caruaru, Petrolina)

### 2. Análise de Acessibilidade
Municípios litorâneos dominam (acesso a portos):
- Ipojuca - Porto de Suape
- Recife - Porto do Recife
- Goiana - Proximidade com portos

### 3. Oportunidades de Interiorização
Identifica potencial de expansão:
- Interior com baixa participação
- Oportunidades em municípios conectados
- Necessidade de infraestrutura logística

### 4. Planejamento de Políticas Públicas
Visualização ajuda a:
- Priorizar investimentos em infraestrutura
- Identificar municípios negligenciados
- Planejar corredores de exportação

## Limitações e Melhorias Futuras

### Limitações Atuais

1. **Coordenadas simplificadas**
   - Usa centroide aproximado dos municípios
   - Não reflete área exata do município

2. **Sem shapefile**
   - Não mostra fronteiras municipais
   - Apenas pontos (municípios)

3. **Mapas estáticos básicos**
   - Matplotlib é funcional mas simples
   - Faltam features geográficas (rios, rodovias)

### Melhorias Possíveis

1. **Adicionar Shapefiles**
   ```python
   import geopandas as gpd
   # Carrega shapefile de PE
   gdf = gpd.read_file("pernambuco_municipios.shp")
   # Cria mapa coroplético real
   ```

2. **Mapas de Calor**
   ```python
   # Densidade de operações comerciais
   # Heatmap de concentração
   ```

3. **Fluxos Origem-Destino**
   ```python
   # Linhas conectando municípios a portos
   # Setas mostrando direção do fluxo
   ```

4. **Integração com Folium**
   ```python
   # Mapas web totalmente interativos
   # Exportáveis para HTML
   ```

## Troubleshooting

### Erro: "Plotly não instalado"
**Solução:**
```bash
pip install plotly
```
Depois: `Kernel → Restart & Run All`

### Erro: "Município sem coordenadas"
**Solução:** Adicione as coordenadas manualmente:
```python
municipios_coords["Novo Município - PE"] = (lat, lon)
```

### Mapas não aparecem
**Solução:**
1. Verifique se %matplotlib inline está na célula 2
2. Execute: `Kernel → Restart & Run All`
3. Aguarde a execução completa

### Erro: "Data not found"
**Solução:**
- Certifique-se que células anteriores foram executadas
- Variável `df` deve estar definida

## Recursos Adicionais

### Para Mapas Avançados

**GeoPandas:**
```bash
pip install geopandas
```

**Folium:**
```bash
pip install folium
```

**Plotly Express:**
```bash
pip install plotly-express
```

### Fontes de Shapefiles

- **IBGE:** https://www.ibge.gov.br/geociencias/downloads-geociencias.html
- **Portal Brasileiro de Dados Abertos**
- **Natural Earth Data:** https://www.naturalearthdata.com/

## Conclusão

As visualizações geográficas adicionam uma **dimensão espacial crítica** à análise:

✓ Identifica concentrações territoriais
✓ Revela padrões espaciais do comércio
✓ Facilita comunicação com stakeholders não-técnicos
✓ Suporta planejamento de políticas públicas

**Execute o notebook e explore os mapas!**

---

**Seção:** 4.4 Visualização Geográfica
**Células adicionadas:** 10
**Total de células:** 88
**Status:** ✅ Funcional
