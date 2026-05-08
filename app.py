import json
from collections import Counter

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Yidoca · Demo Scoring de Leads", layout="wide")


# ================================================================
# Estilos globales — paleta crema-navy editorial estilo calculadora
# ================================================================

def aplicar_estilos_yidoca() -> None:
    """Inyecta paleta, tipografía Inter y clases custom una sola vez."""
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
  --color-bg: #F6F2EA;
  --color-bg-elev: #FBF8F2;
  --color-surface: #FFFFFF;
  --color-ink: #141A24;
  --color-ink-muted: #5A6270;
  --color-ink-soft: #8A8F99;
  --color-rule: #E2DCCF;
  --color-rule-soft: #ECE6D8;
  --color-accent: #1E3A5F;
  --color-accent-deep: #0E1A33;
  --color-cream: #F1ECDF;
  --color-cream-soft: #A8AFBE;
  --color-gold: #B89968;
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* === Reset y overrides Streamlit === */

html, body, .stApp, [data-testid="stAppViewContainer"] {
  background-color: var(--color-bg) !important;
  font-family: var(--font-sans) !important;
  color: var(--color-ink);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.stApp {
  background-image:
    radial-gradient(ellipse at top left, rgba(30, 58, 95, 0.025), transparent 50%),
    radial-gradient(ellipse at bottom right, rgba(184, 153, 104, 0.018), transparent 50%);
  background-attachment: fixed;
}

[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }

.block-container {
  max-width: 1240px !important;
  padding-top: 2rem !important;
  padding-bottom: 4rem !important;
  padding-left: 2rem !important;
  padding-right: 2rem !important;
}

h1, h2, h3, h4, h5, h6, p, li, label {
  font-family: var(--font-sans) !important;
}

.stMarkdown p { line-height: 1.55; }

hr[data-testid="stDivider"], hr {
  border-top: 1px solid var(--color-rule) !important;
  margin: 3rem 0 !important;
  opacity: 0.6;
}

/* === Cabecera === */

.yidoca-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.625rem;
  border-bottom: 1px solid var(--color-rule);
  padding-bottom: 1.5rem;
  margin-bottom: 2.5rem;
}

.yidoca-header-title {
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  margin: 0;
  letter-spacing: 0.14em;
  color: var(--color-ink);
  line-height: 1;
}

.yidoca-header-mark {
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: var(--color-ink-soft);
}

.yidoca-subtitle {
  font-size: 1rem;
  font-weight: 400;
  color: var(--color-ink-muted);
  max-width: none;
  margin: 0 0 3rem 0;
  line-height: 1.55;
}

/* === Section kickers — eyebrow + línea continuándolo === */

.yidoca-kicker {
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  color: var(--color-ink-soft);
  margin: 4.5rem 0 1.875rem 0;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.yidoca-kicker::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--color-rule);
}

.yidoca-subkicker {
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  color: var(--color-ink-soft);
  margin: 6.5rem 0 1.5rem 0;
  display: flex;
  align-items: center;
  gap: 0.875rem;
}

.yidoca-subkicker::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--color-rule-soft);
}

/* === Prosa interpretativa === */

.yidoca-prose-lead {
  font-size: 1.0625rem;
  font-weight: 400;
  color: var(--color-ink);
  max-width: none;
  margin: 0 0 2.5rem 0;
  line-height: 1.55;
}

.yidoca-prose-lead strong {
  font-weight: 500;
  color: var(--color-ink);
}

/* === KPI cards (Capa 1) === */

.yidoca-kpi-card {
  background: var(--color-bg-elev);
  border: 1px solid var(--color-rule);
  border-radius: 10px;
  padding: 1.25rem 1.375rem 1.125rem;
  height: 100%;
  margin-bottom: 2rem;
}

.yidoca-kpi-number {
  font-size: 2.25rem;
  font-weight: 400;
  color: var(--color-ink);
  letter-spacing: -0.025em;
  line-height: 1.1;
  font-variant-numeric: tabular-nums;
}

.yidoca-kpi-pct {
  font-size: 0.8125rem;
  font-weight: 500;
  color: var(--color-ink-muted);
  margin-top: 0.25rem;
  font-variant-numeric: tabular-nums;
  letter-spacing: 0.005em;
}

.yidoca-kpi-label {
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  color: var(--color-ink-soft);
  margin-top: 1rem;
  border-top: 1px solid var(--color-rule-soft);
  padding-top: 0.625rem;
}

/* === KPI mini (Capa 2 dimensiones) === */

.yidoca-kpi-mini {
  background: var(--color-bg-elev);
  border: 1px solid var(--color-rule);
  border-radius: 10px;
  padding: 0.875rem 1rem 0.75rem;
  height: 100%;
}

.yidoca-kpi-mini-number {
  font-size: 1.5rem;
  font-weight: 400;
  color: var(--color-ink);
  letter-spacing: -0.025em;
  line-height: 1.1;
  font-variant-numeric: tabular-nums;
}

.yidoca-kpi-mini-denom {
  font-size: 0.75em;
  color: var(--color-ink-soft);
  font-weight: 400;
}

.yidoca-kpi-mini-label {
  font-size: 0.625rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: var(--color-ink-soft);
  margin-top: 0.5rem;
  line-height: 1.25;
}

/* === Counter (Mostrando X de Y) === */

.yidoca-counter {
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  color: var(--color-ink-soft);
  margin: 0.5rem 0 1.25rem 0;
}

.yidoca-counter strong {
  color: var(--color-ink);
  font-weight: 600;
}

/* === Filtros: selectbox + text_input === */

.stSelectbox label, .stTextInput label {
  font-size: 0.75rem !important;
  font-weight: 600 !important;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: var(--color-ink-soft) !important;
}

.stSelectbox [data-baseweb="select"] > div {
  background: var(--color-bg-elev) !important;
  border: 1px solid var(--color-rule) !important;
  border-radius: 6px !important;
  font-family: var(--font-sans) !important;
  color: var(--color-ink) !important;
  min-height: 38px;
}

.stSelectbox [data-baseweb="select"] > div:hover {
  border-color: var(--color-ink-muted) !important;
}

.stTextInput input {
  font-family: var(--font-sans) !important;
  background: var(--color-bg-elev) !important;
  border: 1px solid var(--color-rule) !important;
  border-radius: 6px !important;
  color: var(--color-ink) !important;
  font-size: 0.9375rem !important;
}

.stTextInput input:focus {
  border-color: var(--color-accent) !important;
  box-shadow: 0 0 0 2px rgba(30, 58, 95, 0.1) !important;
}

.stTextInput input::placeholder {
  color: var(--color-ink-soft) !important;
}

/* === Dataframe === */

[data-testid="stDataFrame"] {
  font-family: var(--font-sans) !important;
  border: 1px solid var(--color-rule);
  border-radius: 10px;
  overflow: hidden;
}

/* === Plotly === */

.stPlotlyChart, .js-plotly-plot { background: transparent !important; }

/* === BLOQUE HÉROE — Detalle del lead === */

.yidoca-hero {
  background: var(--color-accent-deep);
  border-radius: 10px;
  padding: 2.5rem 2.5rem 2.25rem;
  position: relative;
  overflow: hidden;
  margin: 1rem 0 3.5rem 0;
}

.yidoca-hero-watermark {
  position: absolute;
  top: 1.125rem;
  right: 1.625rem;
  font-weight: 600;
  font-size: 0.75rem;
  text-transform: uppercase;
  color: var(--color-cream) !important;
  opacity: 0.18;
  letter-spacing: 0.18em;
  pointer-events: none;
}

.yidoca-hero-empresa {
  font-size: 1.625rem;
  font-weight: 500;
  color: var(--color-cream) !important;
  margin: 0;
  letter-spacing: -0.015em;
  line-height: 1.2;
  max-width: none;
}

.yidoca-hero-meta {
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: var(--color-cream-soft) !important;
  margin: 0.625rem 0 0 0;
}

.yidoca-hero-score {
  text-align: center;
  margin: 2.25rem 0 1.5rem 0;
}

.yidoca-hero-score-number {
  font-size: clamp(3.25rem, 7vw, 5.5rem);
  font-weight: 400;
  letter-spacing: -0.045em;
  line-height: 1;
  font-variant-numeric: tabular-nums;
}

.yidoca-hero-score-denom {
  font-size: 0.45em;
  color: var(--color-cream-soft) !important;
  font-weight: 500;
  letter-spacing: -0.02em;
  margin-left: 0.05em;
}

.yidoca-hero-score-label {
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: var(--color-cream-soft) !important;
  margin-top: 0.625rem;
}

.yidoca-hero-section-kicker {
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  color: var(--color-cream-soft) !important;
  margin: 4.5rem 0 1.5rem 0;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.yidoca-hero-section-kicker::after {
  content: '';
  flex: 1;
  height: 1px;
  background: rgba(241, 236, 223, 0.12);
}

.yidoca-hero-dims {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0.75rem;
  margin: 0.5rem 0 1.5rem 0;
}

.yidoca-hero-dim {
  background: rgba(241, 236, 223, 0.04);
  border: 1px solid rgba(241, 236, 223, 0.12);
  border-radius: 8px;
  padding: 0.75rem 0.875rem 0.625rem;
}

.yidoca-hero-dim-number {
  font-size: 1.375rem;
  font-weight: 500;
  color: var(--color-cream) !important;
  letter-spacing: -0.02em;
  line-height: 1.1;
  font-variant-numeric: tabular-nums;
}

.yidoca-hero-dim-denom {
  font-size: 0.65em;
  color: var(--color-cream-soft) !important;
  font-weight: 400;
}

.yidoca-hero-dim-label {
  font-size: 0.625rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: var(--color-cream-soft) !important;
  margin-top: 0.4rem;
  line-height: 1.2;
}

.yidoca-hero-analisis {
  font-size: 1.0625rem;
  font-weight: 400;
  color: var(--color-cream) !important;
  line-height: 1.6;
  max-width: none;
  margin: 0;
  letter-spacing: 0.005em;
}

@media (max-width: 980px) {
  .yidoca-hero-dims { grid-template-columns: repeat(2, 1fr); }
}

/* === EXPANDER DE TRAZABILIDAD — primera clase === */

[data-testid="stExpander"] {
  background: var(--color-bg-elev) !important;
  border: 1px solid var(--color-rule) !important;
  border-radius: 10px !important;
  overflow: hidden;
  margin-top: 0.5rem;
}

[data-testid="stExpander"] details summary {
  padding: 1.75rem 1.875rem !important;
  list-style: none;
}

[data-testid="stExpander"] details summary,
[data-testid="stExpander"] details summary p {
  font-family: var(--font-sans) !important;
  font-size: 1.875rem !important;
  font-weight: 400 !important;
  letter-spacing: -0.02em !important;
  color: var(--color-ink) !important;
  line-height: 1.2 !important;
  margin: 0 !important;
}

/* Expander anidado — escalado abajo para no competir con los títulos de sección */
[data-testid="stExpander"] [data-testid="stExpander"] details summary {
  padding: 1.125rem 1.5rem !important;
}

[data-testid="stExpander"] [data-testid="stExpander"] details summary,
[data-testid="stExpander"] [data-testid="stExpander"] details summary p {
  font-size: 0.9375rem !important;
  font-weight: 500 !important;
  letter-spacing: 0 !important;
  line-height: 1.5 !important;
}

[data-testid="stExpander"] details summary:hover {
  background: rgba(232, 224, 207, 0.35);
}

[data-testid="stExpander"] details[open] > summary {
  border-bottom: 1px solid var(--color-rule-soft);
}

[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
  padding: 1.5rem !important;
}

.yidoca-trace-subkicker {
  font-size: 0.625rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  color: var(--color-ink-soft);
  margin: 3.75rem 0 1.125rem 0 !important;
  display: flex;
  align-items: center;
  gap: 0.625rem;
}

.yidoca-trace-subkicker:first-child { margin-top: 0 !important; }

.yidoca-trace-subkicker::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--color-rule-soft);
}

.yidoca-trace-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.875rem 1.5rem;
}

.yidoca-trace-fact {
  font-size: 0.875rem;
  color: var(--color-ink);
  line-height: 1.5;
  margin: 0;
  padding: 0.375rem 0;
}

.yidoca-trace-fact-label {
  color: var(--color-ink-soft);
  font-weight: 500;
  margin-right: 0.4em;
}

.yidoca-trace-quote {
  font-size: 0.9375rem;
  font-weight: 400;
  color: var(--color-ink-muted);
  line-height: 1.65;
  border-left: 2px solid var(--color-rule);
  padding: 0.25rem 0 0.25rem 1rem;
  margin: 0.5rem 0 1.25rem 0;
  max-width: none;
  font-style: italic;
}

@media (max-width: 720px) {
  .yidoca-trace-row { grid-template-columns: 1fr; }
}

/* === Footer === */

.yidoca-footer {
  border-top: 1px solid var(--color-rule);
  margin-top: 4rem;
  padding-top: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 1.5rem;
}

.yidoca-footer-note {
  font-size: 0.75rem;
  color: var(--color-ink-soft);
  margin: 0;
  letter-spacing: 0.005em;
  max-width: 60ch;
  font-weight: 400;
}

.yidoca-footer-mark {
  font-size: 0.6875rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: var(--color-ink-muted);
}

/* === st.info (filtros sin resultados) === */

.stAlert {
  background: var(--color-bg-elev) !important;
  border: 1px solid var(--color-rule) !important;
  border-radius: 8px !important;
  color: var(--color-ink-muted) !important;
}
</style>
        """,
        unsafe_allow_html=True,
    )


aplicar_estilos_yidoca()


# ================================================================
# Carga de datos — sin cambios funcionales
# ================================================================

@st.cache_data
def cargar_resultados(ruta: str = "resultados.json") -> list[dict]:
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data
def cargar_leads_originales(ruta: str = "leads.csv") -> pd.DataFrame:
    return pd.read_csv(ruta)


resultados = cargar_resultados()
validos = [r for r in resultados if r.get("puntuacion_total") is not None]
df_originales = cargar_leads_originales()

# Conteos por categoría
categorias = Counter(r["categoria"] for r in validos)
n_claro = categorias.get("Encaje claro", 0)
n_parcial = categorias.get("Encaje parcial", 0)
n_debil = categorias.get("Encaje débil", 0)
n_no = categorias.get("No encaje", 0)
total = len(validos)
pct_claros = (n_claro / total * 100) if total else 0


# ================================================================
# Helpers de render
# ================================================================

def aplicar_tema_plotly(fig):
    """Aplica paleta y tipografía de la casa a una figura Plotly."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#141A24", size=12),
        xaxis=dict(
            showgrid=False,
            linecolor="#E2DCCF",
            tickfont=dict(color="#5A6270", size=12),
            title_font=dict(color="#5A6270", size=11),
        ),
        yaxis=dict(
            showgrid=False,
            linecolor="#E2DCCF",
            tickfont=dict(color="#5A6270", size=12),
            title_font=dict(color="#5A6270", size=11),
        ),
    )
    fig.update_traces(marker_color="#1E3A5F", textfont=dict(color="#141A24", size=12))
    return fig


def color_por_puntuacion(p: int) -> str:
    """Escala tierra editorial — tonos calibrados para legibilidad sobre fondo navy."""
    if p >= 13:
        return "#8FA77B"   # verde oliva claro — Encaje claro
    if p >= 9:
        return "#C4A77B"   # oro claro — Encaje parcial
    if p >= 5:
        return "#B89281"   # terracota claro — Encaje débil
    return "#A8A39B"       # piedra clara — No encaje


# ================================================================
# Diccionarios y cálculos derivados — usados por ambas secciones
# ================================================================

PATRON_LABELS = {
    "ideal_cliente": "Cliente ideal",
    "sistema_comercial_roto": "Sistema comercial roto",
    "buen_encaje_timing_largo": "Buen encaje, timing largo",
    "decisor_equivocado": "Decisor equivocado",
    "fuera_icp_tamano": "Fuera de ICP por tamaño",
    "fuera_icp_sector": "Fuera de ICP por sector",
    "dolor_generico_sin_diagnostico": "Dolor genérico sin diagnóstico",
    "presupuesto_insuficiente": "Presupuesto insuficiente",
    "decision_por_moda": "Decisión por moda",
    "conflicto_interes": "Conflicto de interés",
}

DIMENSIONES_INFO = {
    "encaje_icp": {
        "label": "Encaje ICP",
        "implicacion": "estás invirtiendo tiempo en empresas que estructuralmente no son tu cliente.",
    },
    "madurez_problema": {
        "label": "Madurez del problema",
        "implicacion": "tus leads aún no reconocen el problema que resuelves: necesitan educación previa, no propuesta.",
    },
    "capacidad_decision": {
        "label": "Capacidad de decisión",
        "implicacion": "estás conversando con quien no decide. Hay que escalar antes de seguir invirtiendo tiempo.",
    },
    "timing": {
        "label": "Timing",
        "implicacion": "encuentras decisores correctos pero pierdes el momento: falta urgencia o disparador.",
    },
    "capacidad_presupuestaria": {
        "label": "Capacidad presupuestaria",
        "implicacion": "hay encaje y dolor pero no hay presupuesto disponible: el ciclo se alarga o muere en el cierre.",
    },
}

DIM_KEYS = list(DIMENSIONES_INFO.keys())

# Conteo de patrones (descendente)
patrones_counter = Counter(r["patron_detectado"] for r in validos)
patrones_ordenados = patrones_counter.most_common()
patron_top, n_top = patrones_ordenados[0]
pct_top = (n_top / total * 100) if total else 0
label_top = PATRON_LABELS.get(patron_top, patron_top)

# Promedios por dimensión + identificación de la más débil
promedios = {
    dim: sum(r["dimensiones"][dim] for r in validos) / total
    for dim in DIM_KEYS
} if total else {dim: 0 for dim in DIM_KEYS}
dim_mas_baja = min(promedios, key=promedios.get)
prom_mas_baja = promedios[dim_mas_baja]
label_baja = DIMENSIONES_INFO[dim_mas_baja]["label"]
implicacion_baja = DIMENSIONES_INFO[dim_mas_baja]["implicacion"]


# ================================================================
# Helpers de render — hoisted para usarse en cualquier sección
# ================================================================

def render_kpi_card(n: int, label: str) -> str:
    pct = (n / total * 100) if total else 0
    return (
        '<div class="yidoca-kpi-card">'
        f'<div class="yidoca-kpi-number">{n}</div>'
        f'<div class="yidoca-kpi-pct">{pct:.1f}% del total</div>'
        f'<div class="yidoca-kpi-label">{label}</div>'
        '</div>'
    )


def render_kpi_mini(valor: float, label: str) -> str:
    return (
        '<div class="yidoca-kpi-mini">'
        f'<div class="yidoca-kpi-mini-number">{valor:.2f}'
        '<span class="yidoca-kpi-mini-denom">/3</span></div>'
        f'<div class="yidoca-kpi-mini-label">{label}</div>'
        '</div>'
    )


# ================================================================
# Cabecera
# ================================================================

st.markdown(
    """
    <div class="yidoca-header">
      <p class="yidoca-header-title">Demo · Scoring de Leads</p>
      <span class="yidoca-header-mark">Yidoca</span>
    </div>
    <p class="yidoca-subtitle">Análisis diagnóstico de tu pipeline comercial.</p>
    """,
    unsafe_allow_html=True,
)


# ================================================================
# Sección 1 — Visión agregada (KPIs + categorías + patrones + dimensiones)
# ================================================================

with st.expander("Visión agregada", expanded=False):

    st.markdown(
        f'<p class="yidoca-prose-lead">De tus <strong>{total}</strong> leads, '
        f'<strong>{pct_claros:.0f}%</strong> encajan claramente con tu propuesta. '
        f'El resto consume tiempo de tu equipo sin probabilidad real de cierre.</p>',
        unsafe_allow_html=True,
    )


    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(render_kpi_card(n_claro, "Encaje claro"), unsafe_allow_html=True)
    col2.markdown(render_kpi_card(n_parcial, "Encaje parcial"), unsafe_allow_html=True)
    col3.markdown(render_kpi_card(n_debil, "Encaje débil"), unsafe_allow_html=True)
    col4.markdown(render_kpi_card(n_no, "No encaje"), unsafe_allow_html=True)

    st.markdown(
        '<p class="yidoca-subkicker">Distribución por categoría</p>',
        unsafe_allow_html=True,
    )

    ORDEN_CATEGORIAS = ["Encaje claro", "Encaje parcial", "Encaje débil", "No encaje"]
    df_categorias = pd.DataFrame({
        "Categoría": ORDEN_CATEGORIAS,
        "Leads": [n_claro, n_parcial, n_debil, n_no],
    })
    fig = px.bar(
        df_categorias,
        x="Categoría",
        y="Leads",
        text="Leads",
        category_orders={"Categoría": ORDEN_CATEGORIAS},
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(
        xaxis_tickangle=0,
        showlegend=False,
        margin=dict(l=20, r=20, t=10, b=20),
        xaxis_title=None,
        yaxis_title="Nº de leads",
        height=380,
    )
    fig = aplicar_tema_plotly(fig)
    st.plotly_chart(fig, use_container_width=True)

    # Patrones detectados — sub-bloque dentro de Visión agregada
    st.markdown(
        '<p class="yidoca-subkicker">Patrones detectados</p>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<p class="yidoca-prose-lead">El patrón más frecuente es '
        f'<strong>«{label_top}»</strong> con <strong>{n_top}</strong> leads ({pct_top:.0f}%). '
        f'El cuello de botella sistemático está en la dimensión <strong>{label_baja}</strong> '
        f'(promedio {prom_mas_baja:.2f}/3): {implicacion_baja}</p>',
        unsafe_allow_html=True,
    )

    col_tabla, col_grafico = st.columns(2)

    with col_tabla:
        st.markdown(
            '<p class="yidoca-subkicker">Distribución por patrón</p>',
            unsafe_allow_html=True,
        )
        df_patrones = pd.DataFrame([
            {
                "Patrón": PATRON_LABELS.get(p, p),
                "Leads": n,
                "%": f"{n / total * 100:.1f}%",
            }
            for p, n in patrones_ordenados
        ])
        st.dataframe(df_patrones, hide_index=True, use_container_width=True)

    with col_grafico:
        st.markdown(
            '<p class="yidoca-subkicker">Visualización</p>',
            unsafe_allow_html=True,
        )
        df_patrones_chart = pd.DataFrame({
            "Patrón": [PATRON_LABELS.get(p, p) for p, _ in patrones_ordenados],
            "Leads": [n for _, n in patrones_ordenados],
        }).sort_values("Leads")
        fig_patrones = px.bar(
            df_patrones_chart,
            x="Leads",
            y="Patrón",
            orientation="h",
            text="Leads",
        )
        fig_patrones.update_traces(textposition="outside", cliponaxis=False)
        fig_patrones.update_layout(
            showlegend=False,
            height=400,
            margin=dict(l=20, r=40, t=10, b=20),
            xaxis_title="Nº de leads",
            yaxis_title=None,
        )
        fig_patrones = aplicar_tema_plotly(fig_patrones)
        st.plotly_chart(fig_patrones, use_container_width=True)

    st.markdown(
        '<p class="yidoca-subkicker">Calidad por dimensión (promedio sobre 3)</p>',
        unsafe_allow_html=True,
    )

    cols_dim = st.columns(5)
    for col, dim in zip(cols_dim, DIM_KEYS):
        col.markdown(
            render_kpi_mini(promedios[dim], DIMENSIONES_INFO[dim]["label"]),
            unsafe_allow_html=True,
        )


# ================================================================
# Sección 2 — Análisis por Lead (con expander anidado de info original)
# ================================================================

with st.expander("Análisis por Lead", expanded=False):

    st.markdown(
        '<p class="yidoca-prose-lead">Listado completo con análisis estratégico por lead. '
        'Filtra por categoría o patrón para profundizar.</p>',
        unsafe_allow_html=True,
    )

    # Filtros en una fila
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        cat_sel = st.selectbox(
            "Filtrar por categoría",
            ["Todas", "Encaje claro", "Encaje parcial", "Encaje débil", "No encaje"],
        )
    with col_f2:
        patrones_disponibles = [PATRON_LABELS.get(p, p) for p, _ in patrones_ordenados]
        pat_sel = st.selectbox("Filtrar por patrón", ["Todos"] + patrones_disponibles)
    with col_f3:
        busq = st.text_input("Buscar empresa", placeholder="texto a buscar...")

    busq_lower = busq.strip().lower()

    def pasa_filtros(lead: dict) -> bool:
        if cat_sel != "Todas" and lead["categoria"] != cat_sel:
            return False
        if pat_sel != "Todos":
            label_lead = PATRON_LABELS.get(lead["patron_detectado"], lead["patron_detectado"])
            if label_lead != pat_sel:
                return False
        if busq_lower and busq_lower not in lead["empresa"].lower():
            return False
        return True

    validos_filtrados = [r for r in validos if pasa_filtros(r)]

    st.markdown(
        f'<p class="yidoca-counter">Mostrando <strong>{len(validos_filtrados)}</strong> '
        f'de <strong>{total}</strong> leads</p>',
        unsafe_allow_html=True,
    )

    if not validos_filtrados:
        st.info("No hay leads que coincidan con los filtros")
    else:
        df_leads = pd.DataFrame([
            {
                "Empresa": r["empresa"],
                "Puntuación": r["puntuacion_total"],
                "Categoría": r["categoria"],
                "Patrón": PATRON_LABELS.get(r["patron_detectado"], r["patron_detectado"]),
            }
            for r in validos_filtrados
        ])
        st.dataframe(
            df_leads,
            hide_index=True,
            use_container_width=True,
            column_config={
                "Empresa": st.column_config.TextColumn("Empresa", width="large"),
                "Puntuación": st.column_config.NumberColumn(
                    "Puntuación", format="%d/15", width="small"
                ),
                "Categoría": st.column_config.TextColumn("Categoría", width="medium"),
                "Patrón": st.column_config.TextColumn("Patrón", width="medium"),
            },
        )

        # Detalle de un lead — respeta los filtros activos
        st.markdown(
            '<p class="yidoca-subkicker">Detalle de un lead</p>',
            unsafe_allow_html=True,
        )
        empresas_filtradas = [r["empresa"] for r in validos_filtrados]
        empresa_sel = st.selectbox(
            "Lead para ver el análisis completo:",
            empresas_filtradas,
        )
        lead_sel = next(r for r in validos_filtrados if r["empresa"] == empresa_sel)

        puntuacion = lead_sel["puntuacion_total"]
        color_punt = color_por_puntuacion(puntuacion)
        label_patron = PATRON_LABELS.get(
            lead_sel["patron_detectado"], lead_sel["patron_detectado"]
        )

        # Bloque héroe — todo el panel de detalle como un único HTML
        dim_cards_html = "".join(
            f'<div class="yidoca-hero-dim">'
            f'<div class="yidoca-hero-dim-number">{lead_sel["dimensiones"][dim]}'
            f'<span class="yidoca-hero-dim-denom">/3</span></div>'
            f'<div class="yidoca-hero-dim-label">{DIMENSIONES_INFO[dim]["label"]}</div>'
            '</div>'
            for dim in DIM_KEYS
        )

        st.markdown(
            f"""
            <div class="yidoca-hero">
              <span class="yidoca-hero-watermark">Yidoca</span>
              <h2 class="yidoca-hero-empresa">{lead_sel["empresa"]}</h2>
              <p class="yidoca-hero-meta">{lead_sel["categoria"]}  ·  {label_patron}</p>

              <div class="yidoca-hero-score">
                <div class="yidoca-hero-score-number" style="color: {color_punt};">
                  {puntuacion}<span class="yidoca-hero-score-denom">/15</span>
                </div>
                <div class="yidoca-hero-score-label">Puntuación total</div>
              </div>

              <p class="yidoca-hero-section-kicker">Dimensiones</p>
              <div class="yidoca-hero-dims">{dim_cards_html}</div>

              <p class="yidoca-hero-section-kicker">Análisis estratégico</p>
              <p class="yidoca-hero-analisis">{lead_sel["razonamiento_breve"]}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Expander anidado: información original
        with st.expander("Información Original — Base del Análisis", expanded=False):
            match_original = df_originales[df_originales["empresa"] == empresa_sel]
            if match_original.empty:
                st.markdown(
                    '<p class="yidoca-trace-fact">Información original no disponible.</p>',
                    unsafe_allow_html=True,
                )
            else:
                lead_original = match_original.iloc[0]
                st.markdown(
                    f"""
                    <p class="yidoca-trace-subkicker">Datos de la empresa</p>
                    <div class="yidoca-trace-row">
                      <p class="yidoca-trace-fact"><span class="yidoca-trace-fact-label">Sector</span>{lead_original['sector']}</p>
                      <p class="yidoca-trace-fact"><span class="yidoca-trace-fact-label">Tamaño</span>{lead_original['tamano_empleados']} empleados</p>
                      <p class="yidoca-trace-fact"><span class="yidoca-trace-fact-label">Facturación</span>{lead_original['facturacion_estimada']}</p>
                    </div>

                    <p class="yidoca-trace-subkicker">Contacto</p>
                    <div class="yidoca-trace-row">
                      <p class="yidoca-trace-fact"><span class="yidoca-trace-fact-label">Nombre</span>{lead_original['contacto_nombre']}</p>
                      <p class="yidoca-trace-fact"><span class="yidoca-trace-fact-label">Rol</span>{lead_original['contacto_rol']}</p>
                    </div>

                    <p class="yidoca-trace-subkicker">Origen</p>
                    <div class="yidoca-trace-row">
                      <p class="yidoca-trace-fact"><span class="yidoca-trace-fact-label">Canal</span>{lead_original['canal_origen']}</p>
                      <p class="yidoca-trace-fact"><span class="yidoca-trace-fact-label">Primer contacto</span>{lead_original['fecha_primer_contacto']}</p>
                    </div>

                    <p class="yidoca-trace-subkicker">Dolor declarado</p>
                    <p class="yidoca-trace-quote">{lead_original['dolor_declarado']}</p>

                    <p class="yidoca-trace-subkicker">Notas del SDR</p>
                    <p class="yidoca-trace-quote">{lead_original['notas_sdr']}</p>
                    """,
                    unsafe_allow_html=True,
                )


# ================================================================
# Footer
# ================================================================

st.markdown(
    """
    <div class="yidoca-footer">
      <p class="yidoca-footer-note">
        Modelo de evaluación. Análisis basado en información declarada por el lead.
        Demo Yidoca.
      </p>
      <span class="yidoca-footer-mark">Yidoca</span>
    </div>
    """,
    unsafe_allow_html=True,
)
