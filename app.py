import json
from collections import Counter

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Demo Scoring de Leads", layout="wide")


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

# Header
st.title("Demo Scoring de Leads")
st.caption("Análisis diagnóstico de tu pipeline comercial")

# Capa 1
st.header("Análisis agregado de tu pipeline")

st.write(
    f"De tus **{total}** leads, **{pct_claros:.0f}%** encajan claramente con tu propuesta. "
    "El resto consume tiempo de tu equipo sin probabilidad real de cierre."
)

def fmt_metric(n: int) -> str:
    pct = (n / total * 100) if total else 0
    return f"{n} ({pct:.1f}%)"


col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Encaje claro", value=fmt_metric(n_claro))
col2.metric(label="Encaje parcial", value=fmt_metric(n_parcial))
col3.metric(label="Encaje débil", value=fmt_metric(n_debil))
col4.metric(label="No encaje", value=fmt_metric(n_no))

st.subheader("Distribución por categoría")
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
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# Capa 2 — Patrones detectados
st.header("Patrones detectados en tu pipeline")

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

# Frase interpretativa
st.write(
    f"El patrón más frecuente es **'{label_top}'** con **{n_top}** leads ({pct_top:.0f}%). "
    f"El cuello de botella sistemático está en la dimensión **{label_baja}** "
    f"(promedio {prom_mas_baja:.2f}/3): {implicacion_baja}"
)

# Tabla y gráfico en dos columnas
col_tabla, col_grafico = st.columns(2)

with col_tabla:
    st.subheader("Distribución por patrón")
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
    st.subheader("Visualización")
    # Sort ascendente para que la barra más larga quede arriba en orientación 'h'
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
    st.plotly_chart(fig_patrones, use_container_width=True)

# Promedios por dimensión
st.subheader("Calidad por dimensión (promedio sobre 3)")
cols_dim = st.columns(5)
for col, dim in zip(cols_dim, DIM_KEYS):
    col.metric(
        label=DIMENSIONES_INFO[dim]["label"],
        value=f"{promedios[dim]:.2f}",
    )

st.divider()

# Capa 3 — Leads individuales
st.header("Leads individuales")
st.write(
    "Listado completo con análisis estratégico por lead. "
    "Filtra por categoría o patrón para profundizar."
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

st.caption(f"Mostrando **{len(validos_filtrados)}** de **{total}** leads")

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
    st.subheader("Detalle de un lead")
    empresas_filtradas = [r["empresa"] for r in validos_filtrados]
    empresa_sel = st.selectbox(
        "Ver razonamiento detallado de un lead:",
        empresas_filtradas,
    )
    lead_sel = next(r for r in validos_filtrados if r["empresa"] == empresa_sel)

    puntuacion = lead_sel["puntuacion_total"]
    if puntuacion >= 13:
        color_punt = "#10b981"   # verde — Encaje claro
    elif puntuacion >= 9:
        color_punt = "#f59e0b"   # ámbar — Encaje parcial
    else:
        color_punt = "#ef4444"   # rojo — Encaje débil / No encaje

    with st.container(border=True):
        st.markdown(f"### {lead_sel['empresa']}")
        st.caption(
            f"{lead_sel['categoria']}  ·  "
            f"{PATRON_LABELS.get(lead_sel['patron_detectado'], lead_sel['patron_detectado'])}"
        )

        st.markdown(
            f"""
            <div style="text-align: center; margin: 1.5rem 0 1rem 0;">
              <div style="font-size: 4.5rem; font-weight: 700; color: {color_punt}; line-height: 1;">
                {puntuacion}<span style="font-size: 2rem; color: #9ca3af; font-weight: 500;">/15</span>
              </div>
              <div style="font-size: 0.85rem; color: #9ca3af; margin-top: 0.4rem; text-transform: uppercase; letter-spacing: 0.08em;">
                Puntuación total
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("**Dimensiones**")
        cols_dim_lead = st.columns(5)
        for col, dim in zip(cols_dim_lead, DIM_KEYS):
            col.metric(
                label=DIMENSIONES_INFO[dim]["label"],
                value=f"{lead_sel['dimensiones'][dim]}/3",
            )

        with st.expander(
            "Ver información original sobre la que se basa el análisis",
            expanded=False,
        ):
            match_original = df_originales[df_originales["empresa"] == empresa_sel]
            if match_original.empty:
                st.write("Información original no disponible.")
            else:
                lead_original = match_original.iloc[0]
                col_o1, col_o2 = st.columns(2)
                with col_o1:
                    st.markdown(f"**Sector:** {lead_original['sector']}")
                    st.markdown(f"**Tamaño:** {lead_original['tamano_empleados']} empleados")
                    st.markdown(f"**Facturación:** {lead_original['facturacion_estimada']}")
                    st.markdown(f"**Canal de origen:** {lead_original['canal_origen']}")
                with col_o2:
                    st.markdown(f"**Contacto:** {lead_original['contacto_nombre']}")
                    st.markdown(f"**Rol:** {lead_original['contacto_rol']}")
                    st.markdown(f"**Primer contacto:** {lead_original['fecha_primer_contacto']}")

                st.markdown("---")

                st.markdown("**Dolor declarado:**")
                st.markdown(f"> {lead_original['dolor_declarado']}")

                st.markdown("**Notas del SDR:**")
                st.markdown(f"> {lead_original['notas_sdr']}")

        st.markdown("**Análisis estratégico**")
        st.markdown(f"> {lead_sel['razonamiento_breve']}")
