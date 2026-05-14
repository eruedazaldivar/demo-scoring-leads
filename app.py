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

/* === Pattern cards — Capa 2 (patrones detectados) === */

.yidoca-pattern-card {
  background: var(--color-bg-elev);
  border: 1px solid var(--color-rule);
  border-left: 4px solid var(--color-rule);
  border-radius: 10px;
  padding: 1.5rem 1.75rem;
  margin-bottom: 1rem;
}

.yidoca-pattern-card-critico { border-left-color: #B85C50; }
.yidoca-pattern-card-atencion { border-left-color: #B89968; }
.yidoca-pattern-card-info { border-left-color: #5A7A92; }

.yidoca-pattern-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
}

.yidoca-pattern-header-left {
  display: flex;
  align-items: flex-start;
  gap: 0.875rem;
  flex: 1;
  min-width: 0;
}

.yidoca-pattern-icon {
  font-size: 1.25rem;
  line-height: 1.1;
  flex-shrink: 0;
  margin-top: 0.125rem;
}

.yidoca-pattern-icon-critico { color: #B85C50; }
.yidoca-pattern-icon-atencion { color: #B89968; }
.yidoca-pattern-icon-info { color: #5A7A92; }

.yidoca-pattern-name {
  font-family: var(--font-sans) !important;
  font-size: 1.125rem !important;
  font-weight: 500 !important;
  color: var(--color-ink) !important;
  margin: 0 0 0.25rem 0 !important;
  letter-spacing: -0.01em !important;
  line-height: 1.3 !important;
}

.yidoca-pattern-meta {
  font-size: 0.75rem !important;
  color: var(--color-ink-muted) !important;
  margin: 0 !important;
  letter-spacing: 0.005em !important;
}

.yidoca-pattern-badge {
  font-size: 0.625rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  padding: 0.3rem 0.75rem;
  border-radius: 999px;
  flex-shrink: 0;
  white-space: nowrap;
  align-self: flex-start;
}

.yidoca-pattern-badge-critico {
  background: rgba(184, 92, 80, 0.12);
  color: #B85C50;
}

.yidoca-pattern-badge-atencion {
  background: rgba(184, 153, 104, 0.18);
  color: #8B7344;
}

.yidoca-pattern-badge-info {
  background: rgba(90, 122, 146, 0.12);
  color: #5A7A92;
}

.yidoca-pattern-divider {
  height: 1px;
  background: var(--color-rule-soft);
  margin: 1.25rem 0;
}

.yidoca-pattern-body {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.yidoca-pattern-block-eyebrow {
  font-size: 0.625rem !important;
  font-weight: 600 !important;
  text-transform: uppercase;
  letter-spacing: 0.16em !important;
  color: var(--color-ink-soft) !important;
  margin: 0 0 0.5rem 0 !important;
}

.yidoca-pattern-block-text {
  font-size: 0.875rem !important;
  color: var(--color-ink) !important;
  line-height: 1.55 !important;
  margin: 0 !important;
}

.yidoca-pattern-placeholder {
  color: var(--color-ink-soft) !important;
  font-style: italic;
}

@media (max-width: 720px) {
  .yidoca-pattern-body { grid-template-columns: 1fr; gap: 1rem; }
}

/* === Panel detalle (Capa 3, columna derecha) === */

.yidoca-panel-detalle {
  background: var(--color-bg-elev);
  border: 1px solid var(--color-rule);
  border-radius: 10px;
  padding: 1.75rem 1.875rem;
}

.yidoca-panel-empresa {
  font-family: var(--font-sans) !important;
  font-size: 1.375rem !important;
  font-weight: 500 !important;
  color: var(--color-ink) !important;
  margin: 0 0 0.5rem 0 !important;
  letter-spacing: -0.01em !important;
  line-height: 1.25 !important;
}

.yidoca-panel-meta {
  font-size: 0.6875rem !important;
  font-weight: 600 !important;
  text-transform: uppercase;
  letter-spacing: 0.16em !important;
  color: var(--color-ink-soft) !important;
  margin: 0 0 1.5rem 0 !important;
}

/* Header row: empresa + score [2fr / 1fr] */
.yidoca-panel-header-row {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
  align-items: center;
  padding: 0 0 1.75rem 0;
  border-bottom: 1px solid var(--color-rule-soft);
  margin-bottom: 1.25rem;
}

.yidoca-panel-header-right {
  text-align: right;
}

@media (max-width: 900px) {
  .yidoca-panel-header-row { grid-template-columns: 1fr; gap: 0.75rem; }
  .yidoca-panel-header-right { text-align: left; }
}

/* Análisis + Perfil row [3fr / 2fr] */
.yidoca-analisis-perfil-row {
  display: grid;
  grid-template-columns: 3fr 2fr;
  gap: 2.5rem;
  margin-top: 0.5rem;
}

@media (max-width: 900px) {
  .yidoca-analisis-perfil-row { grid-template-columns: 1fr; gap: 1.5rem; }
}

.yidoca-panel-score-number {
  font-family: var(--font-sans);
  font-size: clamp(2.75rem, 6vw, 4rem);
  font-weight: 400;
  letter-spacing: -0.04em;
  line-height: 1;
  font-variant-numeric: tabular-nums;
}

.yidoca-panel-score-denom {
  font-size: 0.45em;
  color: var(--color-ink-soft);
  font-weight: 500;
  letter-spacing: -0.02em;
  margin-left: 0.05em;
}

.yidoca-panel-score-label {
  font-size: 0.625rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: var(--color-ink-soft);
  margin-top: 0.625rem;
}

.yidoca-panel-section-kicker {
  font-size: 0.625rem !important;
  font-weight: 600 !important;
  text-transform: uppercase;
  letter-spacing: 0.16em !important;
  color: var(--color-ink-soft) !important;
  margin: 1.75rem 0 1rem 0 !important;
  display: flex;
  align-items: center;
  gap: 0.625rem;
}

.yidoca-panel-section-kicker::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--color-rule-soft);
}

.yidoca-dim-bars {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1.25rem 1.5rem;
  margin: 0.5rem 0 0 0;
}

@media (max-width: 1100px) {
  .yidoca-dim-bars { grid-template-columns: repeat(2, 1fr); gap: 1rem; }
}

.yidoca-dim-bar-row {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.yidoca-dim-bar-header {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.yidoca-dim-bar-label {
  font-size: 0.625rem !important;
  text-transform: uppercase;
  letter-spacing: 0.1em !important;
  color: var(--color-ink-soft) !important;
  font-weight: 600 !important;
  line-height: 1.3 !important;
  margin: 0 !important;
}

.yidoca-dim-bar-value {
  font-size: 1.125rem;
  color: var(--color-ink);
  font-variant-numeric: tabular-nums;
  font-weight: 400;
  letter-spacing: -0.02em;
  line-height: 1;
}

.yidoca-dim-bar-track {
  height: 6px;
  background: var(--color-rule-soft);
  border-radius: 3px;
  overflow: hidden;
}

.yidoca-dim-bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 300ms cubic-bezier(0.4, 0, 0.2, 1);
}

.yidoca-bottleneck-card {
  background: var(--color-bg);
  border: 1px solid var(--color-rule);
  border-radius: 8px;
  padding: 1rem 1.25rem;
  margin-top: 1.25rem;
}

.yidoca-bottleneck-eyebrow {
  font-size: 0.625rem !important;
  font-weight: 600 !important;
  text-transform: uppercase;
  letter-spacing: 0.16em !important;
  color: var(--color-ink-soft) !important;
  margin: 0 0 0.375rem 0 !important;
}

.yidoca-bottleneck-name {
  font-family: var(--font-sans) !important;
  font-size: 1rem !important;
  font-weight: 500 !important;
  color: var(--color-ink) !important;
  margin: 0 0 0.25rem 0 !important;
  letter-spacing: -0.005em !important;
}

.yidoca-bottleneck-detail {
  font-size: 0.75rem !important;
  color: var(--color-ink-muted) !important;
  margin: 0 !important;
  font-style: italic;
}

.yidoca-panel-analisis {
  font-size: 0.9375rem !important;
  color: var(--color-ink) !important;
  line-height: 1.6 !important;
  margin: 0 !important;
}

.yidoca-perfil-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem 1.5rem;
}

.yidoca-perfil-cell {
  border-top: 1px solid var(--color-rule-soft);
  padding-top: 0.625rem;
}

.yidoca-perfil-eyebrow {
  font-size: 0.625rem !important;
  font-weight: 600 !important;
  text-transform: uppercase;
  letter-spacing: 0.14em !important;
  color: var(--color-ink-soft) !important;
  margin: 0 0 0.25rem 0 !important;
}

.yidoca-perfil-value {
  font-size: 0.875rem !important;
  color: var(--color-ink) !important;
  font-weight: 500 !important;
  margin: 0 !important;
  letter-spacing: -0.005em !important;
}

.yidoca-placeholder {
  background: var(--color-bg-elev);
  border: 1px dashed var(--color-rule);
  border-radius: 10px;
  padding: 3rem 2rem;
  text-align: center;
}

.yidoca-placeholder-eyebrow {
  font-size: 0.6875rem !important;
  font-weight: 600 !important;
  text-transform: uppercase;
  letter-spacing: 0.18em !important;
  color: var(--color-ink-soft) !important;
  margin: 0 0 0.875rem 0 !important;
}

.yidoca-placeholder-text {
  font-size: 0.9375rem !important;
  color: var(--color-ink-muted) !important;
  margin: 0 !important;
  line-height: 1.55 !important;
}

/* === Bloque RECOMENDACIÓN (Capa 3, al final del panel detalle) === */

.yidoca-recomendacion-block {
  background: var(--color-bg);
  border-left: 3px solid var(--color-gold);
  border-radius: 4px;
  padding: 1.25rem 1.5rem;
  margin-top: 1.75rem;
}

.yidoca-recomendacion-eyebrow {
  font-size: 0.625rem !important;
  font-weight: 600 !important;
  text-transform: uppercase;
  letter-spacing: 0.18em !important;
  color: var(--color-gold) !important;
  margin: 0 0 0.625rem 0 !important;
}

.yidoca-recomendacion-text {
  font-size: 0.9375rem !important;
  color: var(--color-ink) !important;
  line-height: 1.6 !important;
  font-style: italic;
  margin: 0 !important;
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

# Severidad por patrón — guía la composición visual de las cards de patrones (Capa 2)
PATRON_SEVERIDAD = {
    "decisor_equivocado": "critico",
    "fuera_icp_tamano": "critico",
    "fuera_icp_sector": "critico",
    "presupuesto_insuficiente": "critico",
    "dolor_generico_sin_diagnostico": "atencion",
    "decision_por_moda": "atencion",
    "conflicto_interes": "atencion",
    "buen_encaje_timing_largo": "atencion",
    "ideal_cliente": "info",
    "sistema_comercial_roto": "info",
}

SEVERITY_INFO = {
    "critico": {"label": "Crítico", "icon": "⚠"},
    "atencion": {"label": "Atención", "icon": "⚠"},
    "info": {"label": "Info", "icon": "ℹ"},
}

# Texto del bloque "Diagnóstico" en cada card de patrón
PATRON_DESCRIPCIONES = {
    "ideal_cliente": "Encaje sin fisuras: ICP, problema reconocido, decisor accesible, momentum y presupuesto. La conversación de cierre depende de la propuesta, no del calentamiento.",
    "sistema_comercial_roto": "El lead identifica síntomas que apuntan al método comercial: ratios de cierre cayendo, rotación alta o cuotas perdidas. El dolor está articulado y el problema apunta a nuestro lenguaje.",
    "buen_encaje_timing_largo": "Encaje correcto pero sin disparador inmediato. El cliente está listo para una conversación, no para firmar. Pipeline largo, no descartable.",
    "decisor_equivocado": "El dolor existe pero la conversación va con quien no decide. Antes de invertir más tiempo, validar el acceso al decisor real.",
    "fuera_icp_tamano": "La empresa queda fuera del rango de tamaño que atiendes. Aunque haya dolor, el ticket que sostiene el modelo no encaja.",
    "fuera_icp_sector": "El sector queda fuera del foco de la propuesta. Aunque la conversación sea cordial, el match estructural no se construye con el tiempo.",
    "dolor_generico_sin_diagnostico": "La necesidad se expresa en términos generales (\"queremos vender más\") sin diagnóstico propio del cliente. Falta madurez antes de poder proponer.",
    "presupuesto_insuficiente": "Encaje en otras dimensiones pero la capacidad económica no soporta el ticket. El ciclo se alarga o no llega al cierre.",
    "decision_por_moda": "Interés activado por hype tecnológico (IA, automatización) sin un problema concreto detrás. La compra busca legitimación, no resolver.",
    "conflicto_interes": "La empresa opera en un espacio adyacente o competitivo. La conversación tiene fricción estructural difícil de neutralizar.",
}

# Dimensión clave a la que apunta cada patrón
PATRON_DIMENSION_AFECTADA = {
    "ideal_cliente": "Todas las dimensiones",
    "sistema_comercial_roto": "Madurez del problema",
    "buen_encaje_timing_largo": "Timing",
    "decisor_equivocado": "Capacidad de decisión",
    "fuera_icp_tamano": "Encaje ICP",
    "fuera_icp_sector": "Encaje ICP",
    "dolor_generico_sin_diagnostico": "Madurez del problema",
    "presupuesto_insuficiente": "Capacidad presupuestaria",
    "decision_por_moda": "Madurez del problema",
    "conflicto_interes": "Encaje ICP",
}

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

def render_kpi_card(value: str, sublabel: str, label: str) -> str:
    """KPI card flexible: value como HTML interno (puede incluir spans con estilo)."""
    return (
        '<div class="yidoca-kpi-card">'
        f'<div class="yidoca-kpi-number">{value}</div>'
        f'<div class="yidoca-kpi-pct">{sublabel}</div>'
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


def color_por_categoria(categoria: str) -> str:
    """Color del score grande sobre fondo crema, según categoría textual."""
    return {
        "Encaje claro": "#3D5A3F",
        "Encaje parcial": "#A88858",
        "Encaje débil": "#8B6F5C",
        "No encaje": "#7A716A",
    }.get(categoria, "#7A716A")


def color_dim_value(v: int) -> str:
    """Color del relleno de la barra de dimensión según valor 0-3."""
    if v >= 3:
        return "#3D5A3F"
    if v >= 2:
        return "#A88858"
    if v >= 1:
        return "#8B6F5C"
    return "#7A716A"


def render_dimension_bar(label: str, valor: int) -> str:
    """HTML de una barra horizontal: label + valor X/3 + barra rellena proporcional."""
    pct = int((valor / 3) * 100) if valor else 0
    color = color_dim_value(valor)
    return (
        '<div class="yidoca-dim-bar-row">'
        '<div class="yidoca-dim-bar-header">'
        f'<span class="yidoca-dim-bar-label">{label}</span>'
        f'<span class="yidoca-dim-bar-value">{valor}/3</span>'
        '</div>'
        '<div class="yidoca-dim-bar-track">'
        f'<div class="yidoca-dim-bar-fill" style="width: {pct}%; background-color: {color};"></div>'
        '</div>'
        '</div>'
    )


def render_panel_detalle(lead_sel: dict, lead_original) -> str:
    """HTML del panel derecho persistente. El expander de trazabilidad va aparte."""
    empresa = lead_sel["empresa"]
    categoria = lead_sel["categoria"]
    label_patron = PATRON_LABELS.get(lead_sel["patron_detectado"], lead_sel["patron_detectado"])
    color_score = color_por_categoria(categoria)
    score_100 = round(lead_sel["puntuacion_total"] * 100 / 15)
    recomendacion = lead_sel.get("recomendacion", "Recomendación no disponible.")

    bottleneck_dim = min(lead_sel["dimensiones"], key=lead_sel["dimensiones"].get)
    bottleneck_label = DIMENSIONES_INFO[bottleneck_dim]["label"]
    bottleneck_value = lead_sel["dimensiones"][bottleneck_dim]

    bars_html = "".join(
        render_dimension_bar(DIMENSIONES_INFO[dim]["label"], lead_sel["dimensiones"][dim])
        for dim in DIM_KEYS
    )

    if lead_original is not None:
        sector = lead_original.get("sector", "—")
        empleados = lead_original.get("tamano_empleados", "—")
        facturacion = lead_original.get("facturacion_estimada", "—")
        primer_contacto = lead_original.get("fecha_primer_contacto", "—")
    else:
        sector = empleados = facturacion = primer_contacto = "—"

    return (
        '<div class="yidoca-panel-detalle">'
        # HEADER ROW: empresa+meta (2fr) | score (1fr)
        '<div class="yidoca-panel-header-row">'
        '<div class="yidoca-panel-header-left">'
        f'<h2 class="yidoca-panel-empresa">{empresa}</h2>'
        f'<p class="yidoca-panel-meta">{categoria}  ·  {label_patron}</p>'
        '</div>'
        '<div class="yidoca-panel-header-right">'
        f'<div class="yidoca-panel-score-number" style="color: {color_score};">'
        f'{score_100}<span class="yidoca-panel-score-denom">/100</span>'
        '</div>'
        '<div class="yidoca-panel-score-label">Score sobre 100</div>'
        '</div>'
        '</div>'
        # DIMENSIONES (grid 5 columnas)
        '<p class="yidoca-panel-section-kicker">Dimensiones</p>'
        f'<div class="yidoca-dim-bars">{bars_html}</div>'
        # CUELLO DE BOTELLA card
        '<div class="yidoca-bottleneck-card">'
        '<p class="yidoca-bottleneck-eyebrow">Cuello de botella</p>'
        f'<p class="yidoca-bottleneck-name">{bottleneck_label}</p>'
        f'<p class="yidoca-bottleneck-detail">{bottleneck_value}/3 — la dimensión más débil de este lead</p>'
        '</div>'
        # ANÁLISIS + PERFIL row [3fr / 2fr]
        '<div class="yidoca-analisis-perfil-row">'
        '<div class="yidoca-analisis-block">'
        '<p class="yidoca-panel-section-kicker">Análisis estratégico</p>'
        f'<p class="yidoca-panel-analisis">{lead_sel["razonamiento_breve"]}</p>'
        '</div>'
        '<div class="yidoca-perfil-block">'
        '<p class="yidoca-panel-section-kicker">Perfil de empresa</p>'
        '<div class="yidoca-perfil-grid">'
        '<div class="yidoca-perfil-cell">'
        '<p class="yidoca-perfil-eyebrow">Sector</p>'
        f'<p class="yidoca-perfil-value">{sector}</p>'
        '</div>'
        '<div class="yidoca-perfil-cell">'
        '<p class="yidoca-perfil-eyebrow">Empleados</p>'
        f'<p class="yidoca-perfil-value">{empleados}</p>'
        '</div>'
        '<div class="yidoca-perfil-cell">'
        '<p class="yidoca-perfil-eyebrow">Facturación</p>'
        f'<p class="yidoca-perfil-value">{facturacion}</p>'
        '</div>'
        '<div class="yidoca-perfil-cell">'
        '<p class="yidoca-perfil-eyebrow">Primer contacto</p>'
        f'<p class="yidoca-perfil-value">{primer_contacto}</p>'
        '</div>'
        '</div>'
        '</div>'
        '</div>'
        '<div class="yidoca-recomendacion-block">'
        '<p class="yidoca-recomendacion-eyebrow">Recomendación</p>'
        f'<p class="yidoca-recomendacion-text">{recomendacion}</p>'
        '</div>'
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


    score_medio_100 = round(sum(r["puntuacion_total"] for r in validos) / total * 100 / 15) if total else 0
    n_friccion = sum(1 for r in validos if r["categoria"] != "Encaje claro")

    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

    kpi1.markdown(
        render_kpi_card(str(total), "en pipeline", "Leads activos"),
        unsafe_allow_html=True,
    )
    kpi2.markdown(
        render_kpi_card(str(score_medio_100), "de 100", "Score medio"),
        unsafe_allow_html=True,
    )
    kpi3.markdown(
        render_kpi_card(
            f'<span style="font-size: 1.25rem; font-weight: 500; letter-spacing: -0.005em;">{label_baja}</span>',
            f"{prom_mas_baja:.1f}/3 promedio",
            "Cuello de botella",
        ),
        unsafe_allow_html=True,
    )
    kpi4.markdown(
        render_kpi_card(
            f'{n_friccion}<span style="font-size: 1.5rem; color: var(--color-ink-soft); font-weight: 400;">/{total}</span>',
            "leads requieren atención",
            "Con fricción",
        ),
        unsafe_allow_html=True,
    )

    with kpi5:
        fig_donut = px.pie(
            names=["Encaje claro", "Encaje parcial", "Encaje débil", "No encaje"],
            values=[n_claro, n_parcial, n_debil, n_no],
            color_discrete_sequence=["#3D5A3F", "#A88858", "#8B6F5C", "#7A716A"],
            hole=0.6,
        )
        fig_donut.update_traces(
            textinfo="value",
            textfont=dict(family="Inter, sans-serif", size=12, color="#F1ECDF"),
            sort=False,
            marker=dict(line=dict(color="#F6F2EA", width=1)),
            hovertemplate="<b>%{label}</b><br>%{value} leads (%{percent})<extra></extra>",
        )
        fig_donut.update_layout(
            showlegend=False,
            margin=dict(l=10, r=10, t=10, b=10),
            height=200,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", color="#141A24"),
        )
        st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})
        st.markdown(
            '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.25rem 0.5rem; '
            'font-size: 0.625rem; color: var(--color-ink-muted); '
            'text-transform: uppercase; letter-spacing: 0.06em; padding: 0 0.5rem;">'
            '<div><span style="display:inline-block;width:8px;height:8px;background:#3D5A3F;margin-right:6px;border-radius:2px;"></span>Claro</div>'
            '<div><span style="display:inline-block;width:8px;height:8px;background:#A88858;margin-right:6px;border-radius:2px;"></span>Parcial</div>'
            '<div><span style="display:inline-block;width:8px;height:8px;background:#8B6F5C;margin-right:6px;border-radius:2px;"></span>Débil</div>'
            '<div><span style="display:inline-block;width:8px;height:8px;background:#7A716A;margin-right:6px;border-radius:2px;"></span>No encaje</div>'
            '</div>',
            unsafe_allow_html=True,
        )

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

    def render_pattern_card(patron_key: str, n_count: int) -> str:
        label = PATRON_LABELS.get(patron_key, patron_key)
        severidad = PATRON_SEVERIDAD.get(patron_key, "info")
        sev_info = SEVERITY_INFO[severidad]
        descripcion = PATRON_DESCRIPCIONES.get(patron_key, "—")
        dim_afectada = PATRON_DIMENSION_AFECTADA.get(patron_key, "—")
        leads_label = "lead impactado" if n_count == 1 else "leads impactados"
        return (
            f'<div class="yidoca-pattern-card yidoca-pattern-card-{severidad}">'
            '<div class="yidoca-pattern-header">'
            '<div class="yidoca-pattern-header-left">'
            f'<span class="yidoca-pattern-icon yidoca-pattern-icon-{severidad}">{sev_info["icon"]}</span>'
            '<div>'
            f'<h3 class="yidoca-pattern-name">{label}</h3>'
            f'<p class="yidoca-pattern-meta">Dimensión afectada: {dim_afectada} · {n_count} {leads_label}</p>'
            '</div>'
            '</div>'
            f'<span class="yidoca-pattern-badge yidoca-pattern-badge-{severidad}">{sev_info["label"]}</span>'
            '</div>'
            '<div class="yidoca-pattern-divider"></div>'
            '<div class="yidoca-pattern-body">'
            '<div class="yidoca-pattern-block">'
            '<p class="yidoca-pattern-block-eyebrow">Diagnóstico</p>'
            f'<p class="yidoca-pattern-block-text">{descripcion}</p>'
            '</div>'
            '<div class="yidoca-pattern-block">'
            '<p class="yidoca-pattern-block-eyebrow">Recomendación</p>'
            '<p class="yidoca-pattern-block-text yidoca-pattern-placeholder">[Pendiente — sub-sesión de prompt engineering]</p>'
            '</div>'
            '</div>'
            '</div>'
        )

    # Agrupar patrones por severidad respetando el orden por leads impactados desc
    SEVERITY_ORDER = ["critico", "atencion", "info"]
    EXPANDER_TITLES = {
        "critico": "Bloqueos estructurales",
        "atencion": "Fricción cualitativa",
        "info": "Señales positivas",
    }
    cards_by_severity = {sev: [] for sev in SEVERITY_ORDER}
    for patron_key, n_count in patrones_ordenados:
        if n_count < 1:
            continue
        sev = PATRON_SEVERIDAD.get(patron_key, "info")
        cards_by_severity[sev].append((patron_key, n_count))

    for sev in SEVERITY_ORDER:
        cards_list = cards_by_severity[sev]
        if not cards_list:
            continue
        title = f"{EXPANDER_TITLES[sev]} ({len(cards_list)})"
        with st.expander(title, expanded=False):
            st.markdown(
                "".join(render_pattern_card(p, n) for p, n in cards_list),
                unsafe_allow_html=True,
            )

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

    # BLOQUE A — Filtros + Tabla (ancho completo)
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
        busq = st.text_input("Buscar empresa o sector", placeholder="texto a buscar...")

    busq_lower = busq.strip().lower()

    def pasa_filtros(lead: dict) -> bool:
        if cat_sel != "Todas" and lead["categoria"] != cat_sel:
            return False
        if pat_sel != "Todos":
            label_lead = PATRON_LABELS.get(lead["patron_detectado"], lead["patron_detectado"])
            if label_lead != pat_sel:
                return False
        if busq_lower:
            empresa_match = busq_lower in lead["empresa"].lower()
            sector_match = False
            m = df_originales[df_originales["empresa"] == lead["empresa"]]
            if not m.empty:
                sector_match = busq_lower in str(m.iloc[0]["sector"]).lower()
            if not (empresa_match or sector_match):
                return False
        return True

    validos_filtrados = [r for r in validos if pasa_filtros(r)]

    st.markdown(
        f'<p class="yidoca-counter">Mostrando <strong>{len(validos_filtrados)}</strong> '
        f'de <strong>{total}</strong> leads · click en una fila para ver análisis</p>',
        unsafe_allow_html=True,
    )

    empresa_seleccionada = None
    if not validos_filtrados:
        st.info("No hay leads que coincidan con los filtros")
    else:
        filas = []
        for r in validos_filtrados:
            match_orig = df_originales[df_originales["empresa"] == r["empresa"]]
            if match_orig.empty:
                contacto = "—"
                sector = "—"
                primer_contacto = "—"
            else:
                lead_orig = match_orig.iloc[0]
                contacto = f"{lead_orig['contacto_nombre']} · {lead_orig['contacto_rol']}"
                sector = lead_orig["sector"]
                primer_contacto = lead_orig["fecha_primer_contacto"]

            bottleneck_dim = min(r["dimensiones"], key=r["dimensiones"].get)
            bottleneck_label = DIMENSIONES_INFO[bottleneck_dim]["label"]

            filas.append({
                "Score": round(r["puntuacion_total"] * 100 / 15),
                "Empresa": r["empresa"],
                "Contacto": contacto,
                "Sector": sector,
                "Categoría": r["categoria"],
                "Patrón": PATRON_LABELS.get(r["patron_detectado"], r["patron_detectado"]),
                "Cuello de botella": bottleneck_label,
                "Primer contacto": primer_contacto,
            })

        df_leads = pd.DataFrame(filas)

        event = st.dataframe(
            df_leads,
            hide_index=True,
            use_container_width=True,
            on_select="rerun",
            selection_mode="single-row",
            key=f"leads_table_{cat_sel}_{pat_sel}",
            column_config={
                "Score": st.column_config.NumberColumn("Score", format="%d/100", width="small"),
                "Empresa": st.column_config.TextColumn("Empresa", width="large"),
                "Contacto": st.column_config.TextColumn("Contacto", width="medium"),
                "Sector": st.column_config.TextColumn("Sector", width="medium"),
                "Categoría": st.column_config.TextColumn("Categoría", width="small"),
                "Patrón": st.column_config.TextColumn("Patrón", width="medium"),
                "Cuello de botella": st.column_config.TextColumn("Cuello de botella", width="medium"),
                "Primer contacto": st.column_config.TextColumn("Primer contacto", width="small"),
            },
        )

        if event.selection.rows:
            idx = event.selection.rows[0]
            if 0 <= idx < len(df_leads):
                empresa_seleccionada = df_leads.iloc[idx]["Empresa"]

    # BLOQUE B — Panel de detalle (ancho completo, debajo de la tabla)
    if empresa_seleccionada:
        lead_sel = next(r for r in validos_filtrados if r["empresa"] == empresa_seleccionada)
        match_original = df_originales[df_originales["empresa"] == empresa_seleccionada]
        lead_original = match_original.iloc[0] if not match_original.empty else None

        st.markdown(render_panel_detalle(lead_sel, lead_original), unsafe_allow_html=True)

        with st.expander("Trazabilidad — datos fuente", expanded=False):
            if lead_original is None:
                st.markdown(
                    '<p class="yidoca-trace-fact">Información original no disponible.</p>',
                    unsafe_allow_html=True,
                )
            else:
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
    else:
        st.markdown(
            '<div class="yidoca-placeholder">'
            '<p class="yidoca-placeholder-eyebrow">Detalle del lead</p>'
            '<p class="yidoca-placeholder-text">Selecciona un lead de la tabla para ver el análisis completo</p>'
            '</div>',
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
