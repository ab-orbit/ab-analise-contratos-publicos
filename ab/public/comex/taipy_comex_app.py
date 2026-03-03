from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from taipy.gui import Gui, notify

MONTH_MAP = {
    "01": 1,
    "02": 2,
    "03": 3,
    "04": 4,
    "05": 5,
    "06": 6,
    "07": 7,
    "08": 8,
    "09": 9,
    "10": 10,
    "11": 11,
    "12": 12,
}

MONTH_LABELS = {
    1: "Jan",
    2: "Fev",
    3: "Mar",
    4: "Abr",
    5: "Mai",
    6: "Jun",
    7: "Jul",
    8: "Ago",
    9: "Set",
    10: "Out",
    11: "Nov",
    12: "Dez",
}

GLOBAL_REGIONS = {
    "Africa",
    "Europa",
    "Oceania",
    "America do Sul",
    "America do Norte",
    "Oriente Medio",
    "America Central e Caribe",
    "Asia (Exclusive Oriente Medio)",
}

PLOT_TEMPLATE = "plotly_white"


def _normalize_text(value: str) -> str:
    text = str(value)
    text = text.replace("\r", "").replace("\xa0", " ").strip()
    replacements = {
        "Á": "A",
        "À": "A",
        "Ã": "A",
        "Â": "A",
        "É": "E",
        "Ê": "E",
        "Í": "I",
        "Ó": "O",
        "Ô": "O",
        "Õ": "O",
        "Ú": "U",
        "Ç": "C",
        "á": "a",
        "à": "a",
        "ã": "a",
        "â": "a",
        "é": "e",
        "ê": "e",
        "í": "i",
        "ó": "o",
        "ô": "o",
        "õ": "o",
        "ú": "u",
        "ç": "c",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return text


def br_money(x: float) -> str:
    if pd.isna(x):
        return "-"
    if abs(x) >= 1e9:
        return f"US$ {x/1e9:,.2f} bi".replace(",", "X").replace(".", ",").replace("X", ".")
    if abs(x) >= 1e6:
        return f"US$ {x/1e6:,.1f} mi".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"US$ {x:,.0f}".replace(",", ".")


def br_int(x: int) -> str:
    return f"{int(x):,}".replace(",", ".")


def resolve_data_path() -> Path:
    current = Path(__file__).resolve()
    candidates = [
        current.parents[3]
        / "data/pe/comex/V_EXPORTACAO_E IMPORTACAO_POR MUNICIPIO_2024-01_2026-12_DT20260303.csv",
        Path("data/pe/comex/V_EXPORTACAO_E IMPORTACAO_POR MUNICIPIO_2024-01_2026-12_DT20260303.csv").resolve(),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("CSV de comex nao encontrado.")


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    path = resolve_data_path()
    raw = pd.read_csv(path, sep=";", encoding="utf-8-sig", dtype=str)
    raw = raw.rename(
        columns={
            "Mês": "Mes",
            "País": "Pais",
            "Município": "Municipio",
            "Código SH4": "Codigo SH4",
            "Descrição SH4": "Descricao SH4",
            "Código SH2": "Codigo SH2",
            "Descrição SH2": "Descricao SH2",
            "Código Seção": "Codigo Secao",
            "Descrição Seção": "Descricao Secao",
            "Bloco Econômico": "Bloco Economico",
            "Quilograma Líquido": "Quilograma Liquido",
        }
    )

    for col in raw.columns:
        raw[col] = raw[col].astype("string").map(_normalize_text)

    raw["Ano"] = pd.to_numeric(raw["Ano"], errors="coerce").astype("Int64")
    raw["Valor US$ FOB"] = pd.to_numeric(raw["Valor US$ FOB"], errors="coerce")
    raw["Quilograma Liquido"] = pd.to_numeric(raw["Quilograma Liquido"], errors="coerce")

    raw["MesNum"] = raw["Mes"].str.extract(r"^(\d{2})")[0].map(MONTH_MAP)
    raw["MesNome"] = raw["MesNum"].map(MONTH_LABELS)
    raw["Data"] = pd.to_datetime(
        dict(year=raw["Ano"].astype("float"), month=raw["MesNum"].astype("float"), day=1), errors="coerce"
    )

    raw = raw.dropna(subset=["Fluxo", "Ano", "MesNum", "Valor US$ FOB"])

    key_cols = [c for c in raw.columns if c != "Bloco Economico"]
    dedup = raw.drop_duplicates(subset=key_cols).copy()

    block = raw.copy()
    block["is_global_region"] = block["Bloco Economico"].isin(GLOBAL_REGIONS)
    block = (
        block.sort_values(["is_global_region", "Bloco Economico"], ascending=[True, True])
        .drop_duplicates(subset=key_cols, keep="first")
        .drop(columns="is_global_region")
    )

    return dedup, block


def filter_df(df: pd.DataFrame, fluxo: list[str], anos: list[int], municipios: list[str], paises: list[str]) -> pd.DataFrame:
    out = df.copy()
    if fluxo:
        out = out[out["Fluxo"].isin(fluxo)]
    if anos:
        out = out[out["Ano"].isin(anos)]
    if municipios:
        out = out[out["Municipio"].isin(municipios)]
    if paises:
        out = out[out["Pais"].isin(paises)]
    return out


def _series_temporal(filtered: pd.DataFrame) -> pd.DataFrame:
    return (
        filtered.groupby(["Data", "Fluxo"], as_index=False)["Valor US$ FOB"]
        .sum()
        .sort_values("Data")
    )


def _ranking(filtered: pd.DataFrame, dim: str, metrica: str, top_n: int) -> pd.DataFrame:
    if filtered.empty:
        return pd.DataFrame(columns=[dim, "Metrica"])

    if metrica == "US$/kg":
        rank = (
            filtered.groupby(dim, as_index=False)
            .agg(valor=("Valor US$ FOB", "sum"), kg=("Quilograma Liquido", "sum"))
            .assign(Metrica=lambda d: np.where(d["kg"] > 0, d["valor"] / d["kg"], np.nan))
            .dropna(subset=["Metrica"])
            .sort_values("Metrica", ascending=False)
            .head(top_n)
        )
        return rank

    rank = (
        filtered.groupby(dim, as_index=False)[metrica]
        .sum()
        .sort_values(metrica, ascending=False)
        .head(top_n)
        .rename(columns={metrica: "Metrica"})
    )
    return rank


def _hhi(filtered: pd.DataFrame, dim: str) -> float:
    x = filtered.groupby(dim, as_index=False)["Valor US$ FOB"].sum()
    if x.empty:
        return float("nan")
    shares = x["Valor US$ FOB"] / x["Valor US$ FOB"].sum()
    return float((shares**2).sum())


def _lorenz_curve(filtered: pd.DataFrame, dim: str) -> pd.DataFrame:
    x = filtered.groupby(dim, as_index=False)["Valor US$ FOB"].sum().sort_values("Valor US$ FOB")
    if x.empty:
        return pd.DataFrame({"pop": [0, 1], "valor": [0, 1]})

    x["cum_pop"] = np.arange(1, len(x) + 1) / len(x)
    x["cum_val"] = x["Valor US$ FOB"].cumsum() / x["Valor US$ FOB"].sum()
    curve = pd.concat(
        [
            pd.DataFrame({"pop": [0.0], "valor": [0.0]}),
            pd.DataFrame({"pop": x["cum_pop"], "valor": x["cum_val"]}),
        ],
        ignore_index=True,
    )
    return curve


def _kpis(filtered: pd.DataFrame, dim: str) -> dict[str, str]:
    exp = filtered.loc[filtered["Fluxo"].eq("Exportacao"), "Valor US$ FOB"].sum()
    imp = filtered.loc[filtered["Fluxo"].eq("Importacao"), "Valor US$ FOB"].sum()
    saldo = exp - imp
    hhi = _hhi(filtered, dim)

    if filtered.empty:
        cobertura = "-"
    else:
        cobertura = f"{filtered['Data'].min():%m/%Y} a {filtered['Data'].max():%m/%Y}"

    return {
        "kpi_export": br_money(exp),
        "kpi_import": br_money(imp),
        "kpi_saldo": br_money(saldo),
        "kpi_hhi": f"{hhi:.3f}" if not pd.isna(hhi) else "-",
        "kpi_registros": br_int(len(filtered)),
        "kpi_cobertura": cobertura,
    }


def _insight(filtered: pd.DataFrame, rank_df: pd.DataFrame, dim: str, metrica: str, top_n: int) -> str:
    if filtered.empty:
        return "Sem dados para os filtros aplicados."

    top_name = "-"
    top_metric = "-"
    if not rank_df.empty:
        top_name = str(rank_df.iloc[0][dim])
        if metrica == "US$/kg":
            top_metric = f"{float(rank_df.iloc[0]['Metrica']):.2f}"
        else:
            top_metric = br_money(float(rank_df.iloc[0]["Metrica"]))

    top_flux = filtered.groupby("Fluxo", as_index=False)["Valor US$ FOB"].sum().sort_values("Valor US$ FOB", ascending=False)
    fluxo_lider = str(top_flux.iloc[0]["Fluxo"]) if not top_flux.empty else "-"

    return (
        f"No recorte atual, {fluxo_lider} domina o valor movimentado. "
        f"No ranking de {dim}, o 1o colocado e {top_name} ({top_metric}, metrica {metrica}). "
        f"Recomendacao: compare Top {top_n} com o heatmap mensal para separar padrao estrutural de picos pontuais."
    )


def _opportunity_matrix(filtered: pd.DataFrame, dim: str, top_n: int):
    years = sorted(filtered["Ano"].dropna().astype(int).unique().tolist())
    if len(years) < 2:
        return px.scatter(title="Matriz de oportunidade requer pelo menos 2 anos")

    prev_year = years[-2]
    curr_year = years[-1]

    base = (
        filtered[filtered["Ano"].isin([prev_year, curr_year])]
        .groupby([dim, "Ano"], as_index=False)["Valor US$ FOB"]
        .sum()
        .pivot(index=dim, columns="Ano", values="Valor US$ FOB")
        .fillna(0)
        .reset_index()
    )
    if prev_year not in base.columns or curr_year not in base.columns:
        return px.scatter(title="Matriz de oportunidade indisponivel")

    base = base.rename(columns={prev_year: "valor_prev", curr_year: "valor_curr"})
    base = base[base["valor_curr"] > 0].copy()
    if base.empty:
        return px.scatter(title="Sem entidades com valor no ano corrente")

    total_curr = base["valor_curr"].sum()
    base["share_curr"] = base["valor_curr"] / total_curr
    base["growth"] = np.where(base["valor_prev"] > 0, (base["valor_curr"] / base["valor_prev"]) - 1, np.nan)
    base["growth"] = base["growth"].replace([np.inf, -np.inf], np.nan).fillna(0)
    base = base.sort_values("valor_curr", ascending=False).head(max(25, top_n))

    fig = px.scatter(
        base,
        x="share_curr",
        y="growth",
        size="valor_curr",
        hover_name=dim,
        color="growth",
        color_continuous_scale="RdYlGn",
        template=PLOT_TEMPLATE,
        title=f"Matriz de oportunidade ({curr_year} vs {prev_year}): share x crescimento",
    )
    fig.add_hline(y=0, line_dash="dash", line_color="#6c757d")
    fig.update_layout(xaxis_title="Participacao no ano corrente", yaxis_title="Crescimento YoY")
    return fig


def _regime_map(filtered: pd.DataFrame):
    ts = (
        filtered.groupby(["Data", "Fluxo"], as_index=False)["Valor US$ FOB"]
        .sum()
        .sort_values(["Fluxo", "Data"])
    )
    if ts.empty:
        return px.scatter(title="Sem dados para mapa de regime")

    rows = []
    for fluxo, g in ts.groupby("Fluxo"):
        g = g.sort_values("Data").copy()
        g["ret"] = g["Valor US$ FOB"].pct_change().replace([np.inf, -np.inf], np.nan).fillna(0)
        vol = float(g["ret"].std())
        x = np.arange(len(g))
        slope = float(np.polyfit(x, g["Valor US$ FOB"], 1)[0]) if len(g) > 1 else 0.0
        rows.append(
            {
                "Fluxo": fluxo,
                "Volatilidade": vol,
                "Tendencia": slope,
                "Valor Atual": float(g["Valor US$ FOB"].iloc[-1]),
            }
        )
    regime = pd.DataFrame(rows)
    fig = px.scatter(
        regime,
        x="Volatilidade",
        y="Tendencia",
        size="Valor Atual",
        color="Fluxo",
        template=PLOT_TEMPLATE,
        title="Mapa de regime: volatilidade x tendencia por fluxo",
        color_discrete_sequence=["#005f73", "#bb3e03"],
    )
    fig.add_hline(y=0, line_dash="dash", line_color="#6c757d")
    fig.update_layout(xaxis_title="Volatilidade mensal (desvio de retornos)", yaxis_title="Tendencia linear do valor FOB")
    return fig


def _sankey_chain(filtered: pd.DataFrame):
    chain = (
        filtered.groupby(["Municipio", "Codigo SH2", "Pais"], as_index=False)["Valor US$ FOB"]
        .sum()
        .sort_values("Valor US$ FOB", ascending=False)
    )
    if chain.empty:
        return go.Figure()

    top_m = chain.groupby("Municipio", as_index=False)["Valor US$ FOB"].sum().nlargest(8, "Valor US$ FOB")["Municipio"]
    top_sh2 = chain.groupby("Codigo SH2", as_index=False)["Valor US$ FOB"].sum().nlargest(10, "Valor US$ FOB")["Codigo SH2"]
    top_p = chain.groupby("Pais", as_index=False)["Valor US$ FOB"].sum().nlargest(10, "Valor US$ FOB")["Pais"]

    chain = chain[
        chain["Municipio"].isin(top_m)
        & chain["Codigo SH2"].isin(top_sh2)
        & chain["Pais"].isin(top_p)
    ].copy()
    if chain.empty:
        return go.Figure()

    nodes = (
        [f"M: {x}" for x in sorted(chain["Municipio"].unique())]
        + [f"SH2: {x}" for x in sorted(chain["Codigo SH2"].unique())]
        + [f"P: {x}" for x in sorted(chain["Pais"].unique())]
    )
    node_idx = {n: i for i, n in enumerate(nodes)}

    link_m_sh2 = (
        chain.groupby(["Municipio", "Codigo SH2"], as_index=False)["Valor US$ FOB"]
        .sum()
    )
    link_sh2_p = (
        chain.groupby(["Codigo SH2", "Pais"], as_index=False)["Valor US$ FOB"]
        .sum()
    )

    sources = [node_idx[f"M: {r.Municipio}"] for r in link_m_sh2.itertuples(index=False)]
    targets = [node_idx[f"SH2: {r._1}"] for r in link_m_sh2.itertuples(index=False)]
    values = [float(r._2) for r in link_m_sh2.itertuples(index=False)]

    sources += [node_idx[f"SH2: {r._0}"] for r in link_sh2_p.itertuples(index=False)]
    targets += [node_idx[f"P: {r._1}"] for r in link_sh2_p.itertuples(index=False)]
    values += [float(r._2) for r in link_sh2_p.itertuples(index=False)]

    fig = go.Figure(
        data=[
            go.Sankey(
                node=dict(
                    pad=14,
                    thickness=12,
                    line=dict(color="#d9e6ef", width=0.8),
                    label=nodes,
                    color=["#0a9396"] * len(nodes),
                ),
                link=dict(source=sources, target=targets, value=values, color="rgba(187,62,3,0.28)"),
            )
        ]
    )
    fig.update_layout(template=PLOT_TEMPLATE, title="Sankey da cadeia comercial: Municipio -> SH2 -> Pais", height=560)
    return fig


def make_views(filtered: pd.DataFrame, block_filtered: pd.DataFrame, dim: str, metrica: str, top_n: int):
    if filtered.empty:
        empty = px.scatter(title="Sem dados para os filtros aplicados")
        return {
            "fig_ts": empty,
            "fig_rank": empty,
            "fig_heatmap": empty,
            "fig_treemap": empty,
            "fig_bubble": empty,
            "fig_lorenz": empty,
            "fig_opportunity": empty,
            "fig_regime": empty,
            "fig_sankey": go.Figure(),
            "block_table": pd.DataFrame(),
            "kpis": _kpis(filtered, dim),
            "insight_text": "Sem dados para os filtros aplicados.",
        }

    ts = _series_temporal(filtered)
    fig_ts = px.area(
        ts,
        x="Data",
        y="Valor US$ FOB",
        color="Fluxo",
        line_group="Fluxo",
        template=PLOT_TEMPLATE,
        title="Pulso temporal do comercio exterior",
        color_discrete_sequence=["#005f73", "#bb3e03"],
    )
    fig_ts.update_layout(legend_title_text="Fluxo", yaxis_title="US$ FOB", xaxis_title="Data")

    rank_df = _ranking(filtered, dim, metrica, top_n)
    fig_rank = px.bar(
        rank_df.sort_values("Metrica", ascending=True),
        x="Metrica",
        y=dim,
        orientation="h",
        template=PLOT_TEMPLATE,
        title=f"Top {top_n} por {dim} ({metrica})",
        color="Metrica",
        color_continuous_scale="Tealgrn",
    )
    fig_rank.update_layout(coloraxis_showscale=False)

    hm = (
        filtered.groupby(["Ano", "MesNum"], as_index=False)["Valor US$ FOB"]
        .sum()
        .pivot(index="Ano", columns="MesNum", values="Valor US$ FOB")
        .fillna(0)
    )
    hm = hm.reindex(columns=range(1, 13), fill_value=0)
    hm.columns = [MONTH_LABELS[c] for c in hm.columns]
    fig_heatmap = px.imshow(
        hm,
        aspect="auto",
        color_continuous_scale=["#fefae0", "#ee9b00", "#9b2226"],
        template=PLOT_TEMPLATE,
        title="Heatmap sazonal: valor FOB por mes e ano",
    )
    fig_heatmap.update_layout(xaxis_title="Mes", yaxis_title="Ano", coloraxis_colorbar_title="US$ FOB")

    mix = (
        filtered.groupby(["Codigo Secao", "Descricao Secao", "Codigo SH2"], as_index=False)["Valor US$ FOB"]
        .sum()
        .sort_values("Valor US$ FOB", ascending=False)
        .head(max(40, top_n * 3))
    )
    fig_treemap = px.treemap(
        mix,
        path=["Descricao Secao", "Codigo SH2"],
        values="Valor US$ FOB",
        color="Valor US$ FOB",
        color_continuous_scale="YlOrBr",
        template=PLOT_TEMPLATE,
        title="Arquitetura da pauta: secao > SH2",
    )

    muni_bubble = (
        filtered.groupby(["Municipio", "Fluxo"], as_index=False)["Valor US$ FOB"]
        .sum()
        .pivot(index="Municipio", columns="Fluxo", values="Valor US$ FOB")
        .fillna(0)
        .reset_index()
    )
    if "Exportacao" not in muni_bubble.columns:
        muni_bubble["Exportacao"] = 0.0
    if "Importacao" not in muni_bubble.columns:
        muni_bubble["Importacao"] = 0.0
    muni_bubble["Total"] = muni_bubble["Exportacao"] + muni_bubble["Importacao"]
    muni_bubble = muni_bubble.sort_values("Total", ascending=False).head(50)

    fig_bubble = px.scatter(
        muni_bubble,
        x="Importacao",
        y="Exportacao",
        size="Total",
        hover_name="Municipio",
        color="Total",
        color_continuous_scale="IceFire",
        template=PLOT_TEMPLATE,
        title="Mapa de posicionamento municipal: exporta vs importa",
    )
    fig_bubble.update_layout(xaxis_title="Importacao (US$)", yaxis_title="Exportacao (US$)")

    lc = _lorenz_curve(filtered, dim)
    fig_lorenz = px.line(
        lc,
        x="pop",
        y="valor",
        template=PLOT_TEMPLATE,
        title=f"Curva de concentracao (Lorenz) por {dim}",
    )
    fig_lorenz.add_scatter(x=[0, 1], y=[0, 1], mode="lines", name="Equidade", line={"dash": "dash", "color": "#6c757d"})
    fig_lorenz.update_layout(xaxis_title="Participacao acumulada de entidades", yaxis_title="Participacao acumulada de valor")
    fig_opportunity = _opportunity_matrix(filtered, dim, top_n)
    fig_regime = _regime_map(filtered)
    fig_sankey = _sankey_chain(filtered)

    block_df = (
        block_filtered.groupby(["Fluxo", "Bloco Economico"], as_index=False)["Valor US$ FOB"]
        .sum()
        .sort_values(["Fluxo", "Valor US$ FOB"], ascending=[True, False])
    )
    block_top = block_df.groupby("Fluxo", group_keys=False).head(8)

    return {
        "fig_ts": fig_ts,
        "fig_rank": fig_rank,
        "fig_heatmap": fig_heatmap,
        "fig_treemap": fig_treemap,
        "fig_bubble": fig_bubble,
        "fig_lorenz": fig_lorenz,
        "fig_opportunity": fig_opportunity,
        "fig_regime": fig_regime,
        "fig_sankey": fig_sankey,
        "block_table": block_top,
        "kpis": _kpis(filtered, dim),
        "insight_text": _insight(filtered, rank_df, dim, metrica, top_n),
    }


def update_views(state):
    filtered = filter_df(df_main, state.fluxo_sel, state.anos_sel, state.municipios_sel, state.paises_sel)
    block_filtered = filter_df(df_block, state.fluxo_sel, state.anos_sel, state.municipios_sel, state.paises_sel)

    if filtered.empty:
        notify(state, "warning", "Sem dados para os filtros selecionados.")

    views = make_views(filtered, block_filtered, state.dim_sel, state.metrica_sel, state.top_n)

    state.filtered_rows = len(filtered)
    state.fig_ts = views["fig_ts"]
    state.fig_rank = views["fig_rank"]
    state.fig_heatmap = views["fig_heatmap"]
    state.fig_treemap = views["fig_treemap"]
    state.fig_bubble = views["fig_bubble"]
    state.fig_lorenz = views["fig_lorenz"]
    state.fig_opportunity = views["fig_opportunity"]
    state.fig_regime = views["fig_regime"]
    state.fig_sankey = views["fig_sankey"]
    state.block_table = views["block_table"]
    state.insight_text = views["insight_text"]

    k = views["kpis"]
    state.kpi_export = k["kpi_export"]
    state.kpi_import = k["kpi_import"]
    state.kpi_saldo = k["kpi_saldo"]
    state.kpi_hhi = k["kpi_hhi"]
    state.kpi_registros = k["kpi_registros"]
    state.kpi_cobertura = k["kpi_cobertura"]


def on_change(state, var_name, var_value):
    update_views(state)


df_main, df_block = load_data()

fluxo_options = sorted(df_main["Fluxo"].dropna().unique().tolist())
ano_options = sorted(df_main["Ano"].dropna().unique().astype(int).tolist())
municipio_options = sorted(df_main["Municipio"].dropna().unique().tolist())
pais_options = sorted(df_main["Pais"].dropna().unique().tolist())

metric_options = ["Valor US$ FOB", "Quilograma Liquido", "US$/kg"]
dim_options = ["Municipio", "Pais", "Codigo SH2", "Descricao Secao"]

fluxo_sel = fluxo_options
anos_sel = ano_options
municipios_sel = []
paises_sel = []
metrica_sel = "Valor US$ FOB"
dim_sel = "Municipio"
top_n = 12
filtered_rows = 0

kpi_export = "-"
kpi_import = "-"
kpi_saldo = "-"
kpi_hhi = "-"
kpi_registros = "-"
kpi_cobertura = "-"

fig_ts = px.scatter(title="Carregando...")
fig_rank = px.scatter(title="Carregando...")
fig_heatmap = px.scatter(title="Carregando...")
fig_treemap = px.scatter(title="Carregando...")
fig_bubble = px.scatter(title="Carregando...")
fig_lorenz = px.scatter(title="Carregando...")
fig_opportunity = px.scatter(title="Carregando...")
fig_regime = px.scatter(title="Carregando...")
fig_sankey = go.Figure()
block_table = pd.DataFrame()
insight_text = ""

_initial_filtered = filter_df(df_main, fluxo_sel, anos_sel, municipios_sel, paises_sel)
_initial_block_filtered = filter_df(df_block, fluxo_sel, anos_sel, municipios_sel, paises_sel)
_initial_views = make_views(_initial_filtered, _initial_block_filtered, dim_sel, metrica_sel, top_n)

filtered_rows = len(_initial_filtered)
fig_ts = _initial_views["fig_ts"]
fig_rank = _initial_views["fig_rank"]
fig_heatmap = _initial_views["fig_heatmap"]
fig_treemap = _initial_views["fig_treemap"]
fig_bubble = _initial_views["fig_bubble"]
fig_lorenz = _initial_views["fig_lorenz"]
fig_opportunity = _initial_views["fig_opportunity"]
fig_regime = _initial_views["fig_regime"]
fig_sankey = _initial_views["fig_sankey"]
block_table = _initial_views["block_table"]
insight_text = _initial_views["insight_text"]

_initial_k = _initial_views["kpis"]
kpi_export = _initial_k["kpi_export"]
kpi_import = _initial_k["kpi_import"]
kpi_saldo = _initial_k["kpi_saldo"]
kpi_hhi = _initial_k["kpi_hhi"]
kpi_registros = _initial_k["kpi_registros"]
kpi_cobertura = _initial_k["kpi_cobertura"]

page = """
<|part|class_name=hero|
# COMEX PE Command Center
Analise interativa de alta definicao para importacao e exportacao por municipio, parceiro e pauta.
|>

## Filtros analiticos
<|layout|columns=1 1 1 1|gap=10px|
<|{fluxo_sel}|selector|lov={fluxo_options}|dropdown|multiple|label=Fluxo|on_change=on_change|>
<|{anos_sel}|selector|lov={ano_options}|dropdown|multiple|label=Ano|on_change=on_change|>
<|{municipios_sel}|selector|lov={municipio_options}|dropdown|multiple|label=Municipio|on_change=on_change|>
<|{paises_sel}|selector|lov={pais_options}|dropdown|multiple|label=Pais|on_change=on_change|>
|>

<|layout|columns=1 1 1|gap=10px|
<|{metrica_sel}|selector|lov={metric_options}|dropdown|label=Metrica de ranking|on_change=on_change|>
<|{dim_sel}|selector|lov={dim_options}|dropdown|label=Dimensao de ranking|on_change=on_change|>
<|{top_n}|slider|min=5|max=30|step=1|label=Top N|on_change=on_change|>
|>

## Cockpit executivo
<|layout|columns=1 1 1 1 1 1|gap=8px|
<|part|class_name=kpi-card|
**Exportacoes**  
<|{kpi_export}|text|>
|>
<|part|class_name=kpi-card|
**Importacoes**  
<|{kpi_import}|text|>
|>
<|part|class_name=kpi-card|
**Saldo**  
<|{kpi_saldo}|text|>
|>
<|part|class_name=kpi-card|
**HHI**  
<|{kpi_hhi}|text|>
|>
<|part|class_name=kpi-card|
**Registros**  
<|{kpi_registros}|text|>
|>
<|part|class_name=kpi-card|
**Cobertura**  
<|{kpi_cobertura}|text|>
|>
|>

## Visoes exploratorias
<|layout|columns=1 1|gap=12px|
<|chart|figure={fig_ts}|height=420px|>
<|chart|figure={fig_heatmap}|height=420px|>
|>

<|layout|columns=1 1|gap=12px|
<|chart|figure={fig_rank}|height=460px|>
<|chart|figure={fig_treemap}|height=460px|>
|>

<|layout|columns=1 1|gap=12px|
<|chart|figure={fig_bubble}|height=460px|>
<|chart|figure={fig_lorenz}|height=460px|>
|>

## Advanced intelligence
<|layout|columns=1 1|gap=12px|
<|chart|figure={fig_opportunity}|height=460px|>
<|chart|figure={fig_regime}|height=460px|>
|>

<|chart|figure={fig_sankey}|height=560px|>

## Geoeconomia por blocos
<|{block_table}|table|width=100%|>

## Insight orientado a acao
<|part|class_name=insight-box|
<|{insight_text}|text|raw|>
|>
"""


if __name__ == "__main__":
    app = Gui(page, css_file=str(Path(__file__).with_name("taipy_comex_app.css")))
    app.run(title="Comex PE - Wow Explorer", dark_mode=False, use_reloader=True, port="auto")
