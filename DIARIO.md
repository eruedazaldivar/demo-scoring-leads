# Diario de aprendizaje — Demo scoring de leads

Registro de sesiones de trabajo sobre el proyecto de demo de scoring de leads con la API de Claude. Apunto qué hago, qué aprendo, qué decido y por qué. Las sesiones van en orden cronológico inverso: la más reciente arriba.

---------------------------------------------------------------------------------------------------------------------

## Sesión 9 — 12 mayo 2026

**Duración prevista:** abierta, hasta donde aguantemos
**Duración real:** ~2h30 (cierre completo con cierre formal)

### Qué hicimos

Sesión dedicada al despliegue público de la demo Streamlit en cloud y a conectar el pipeline completo landing → demo.

Merge exp_UI → main:
- Verificación previa de exp_UI funcionando correctamente en local
- Cambio a main con git checkout main + git pull (working tree limpio)
- git merge exp_UI → resultó merge commit (no fast-forward)
- Vim se abrió para mensaje pre-rellenado, primera vez encontrando Vim en flujo Git real
- Aprendizaje básico Vim: Escape → :wq guardar, :q! cancelar, i editar
- Push a GitHub exitoso
- Limpieza de rama exp_UI: borrado local (git branch -d) + remoto (git push origin --delete)
- Verificación: solo main local y remoto

Setup Streamlit Community Cloud (con escollos significativos):
- Login con OAuth GitHub funcional
- Intento de Create app → 3 errores rojos "does not exist" para repo/branch/file
- Diagnóstico inicial erróneo: pensé que era problema de permisos GitHub App
- Investigación: github.com/apps/streamlit retorna 404 (URL deprecada)
- Revisión github.com/settings/installations: solo Vercel instalada, no Streamlit
- Authorized OAuth Apps: 2 apps Streamlit (antigua + nueva) ambas "Never used"
- Intento de reauth: pantalla solo pedía Email addresses (read-only), no acceso a repos
- Segunda pantalla más completa pero con permiso solo a Public repositories
- Decisión de pivot: hacer repo público temporalmente para desbloquear

Cambio repo demo-scoring-leads a público:
- github.com/eruedazaldivar/demo-scoring-leads/settings → Danger Zone → Make public
- Confirmación con nombre exacto del repo
- Riesgo evaluado: sin secretos (API key en .env ignorado), sin datos reales (leads ficticios), sin propiedad intelectual única (metodología explicable)

Deploy en Streamlit Cloud:
- Formulario "Deploy an app" auto-rellenó campos por defecto INCORRECTOS:
  - Repository con barra inicial: /eruedazaldivar/demo-scoring-leads (debe ser sin barra)
  - Main file path: streamlit_app.py (convención por defecto, no la del proyecto)
- Correcciones: quitar barra, cambiar a app.py, subdominio yidoca-scoring
- Click Deploy → build exitoso
- URL pública: yidoca-scoring.streamlit.app
- Validación: las 3 capas se ven correctamente con polish editorial Yidoca

Conexión landing → demo (Bloque F):
- Edit en yidoca-demo-landing (los 3 archivos):
  - header.tsx: CTA "Lanzar demo" con href="https://yidoca-scoring.streamlit.app" + target="_blank" + rel="noopener noreferrer"
  - hero.tsx: mismo cambio en CTA primario
  - cta-final.tsx: mismo cambio en CTA primario
- Decisión: NO tocar "Ver método" (hero.tsx) ni "Agendar discovery" (cta-final.tsx)
- Commit + push → Vercel auto-redepliega en 30 segundos
- Validación pipeline completo en incógnito: los 3 CTAs "Lanzar demo" abren pestaña nueva con la demo funcional

Decisión sobre repo público:
- Tras evaluación honesta de pros/contras
- Decisión: dejar público por transparencia técnica de marca consultora boutique
- Beneficios: sin fricción para redeploys futuros, contribuye a confianza técnica visible
- Riesgo evaluado: bajo (sin secretos, código es metodología explicable)

### Qué aprendí

- GitHub distingue claramente entre OAuth (login) y GitHub App (acceso a repos). Servicios como Streamlit Cloud, Vercel, Netlify requieren GitHub App instalada para repos privados, no solo OAuth.
- "Deploy a public app from GitHub" en Streamlit Cloud se refiere a que la APP desplegada será pública, NO a que el repo deba ser público. Lenguaje confuso de la plataforma.
- Streamlit Cloud free funciona con repos privados solo si la GitHub App tiene permisos correctos. Si no se logra esto, la solución más rápida es hacer el repo público temporalmente.
- Auto-rellenado de formularios web puede usar valores incorrectos por defecto. SIEMPRE verificar antes de submit. Streamlit Cloud puso barra inicial en repo y nombre de archivo convencional que no era el real.
- Vim básico es habilidad que aparece cuando Git abre editor para mensajes de commit/merge: Escape → :wq guardar+salir, :q! cancelar sin guardar, i para editar texto. Hostil al principio pero se domina rápido.
- Workflow Git de rama experimental completo: crear → trabajar → mergear a main + push → borrar local Y remota. Las ramas son temporales por diseño.
- target="_blank" + rel="noopener noreferrer" es patrón estándar para enlaces externos a otras plataformas. Abre pestaña nueva (UX correcto al cambiar de plataforma) + seguridad básica (anti-phishing, privacidad).
- Aceptar conscientemente trade-offs temporales (repo público para resolver bloqueo) con riesgo evaluado es disciplina madura. La trampa es no apuntarlas como deuda.

### Decisiones tomadas

- Mergeo exp_UI a main antes de desplegar (en lugar de desplegar rama experimental directamente). Disciplina profesional: main es siempre la rama desplegable.
- Borrar exp_UI tras merge (local y remota). Ramas son temporales por diseño.
- Streamlit Cloud como plataforma de deploy (en lugar de Render). Soporte nativo, setup simple, gestión de secrets built-in.
- Subdominio "yidoca-scoring" (en lugar de aleatorio, "yidoca-demo" o "demo-yidoca"). Coherente con familia Yidoca, descriptivo del producto, futuro-compatible.
- Repo demo-scoring-leads público temporal aceptado para desbloquear deploy. Riesgo evaluado y aceptable.
- Tras validar deploy funcional, decisión de DEJAR repo público. Razones: transparencia técnica de marca consultora boutique, sin fricción redeploys futuros, sin secretos ni datos reales.
- Los 3 CTAs "Lanzar demo" actualizados a URL real Streamlit con target="_blank" y rel seguridad. "Ver método" y "Agendar discovery" sin cambios (anchors internos válidos en su caso).
- Pipeline end-to-end validado: landing → demo funciona en producción.

### Próximos pasos

- Sub-sesión futura: prompt engineering para añadir "Recomendación" por patrón (modificar prompt scoring, reprocesar 50 leads costo ~$0.40)
- Sub-sesión futura: ajustes finos visuales de la demo si descubrimos problemas (donut, dimensiones, etc.)
- Sub-sesión futura: paralelización del procesado de leads (3 min → 30 seg)
- Sub-sesión futura: capacidad upload CSV en vivo (requiere API key como secret en Streamlit Cloud)
- Sub-sesión futura: backup del repo de la landing institucional a GitHub
- Sub-sesión futura: adaptación visual de la demo Streamlit al estilo dark/serif de la landing institucional (decisión arquitectónica primero, 4-6h)
- Sub-sesión futura: decisión estratégica nombre comercial (validación legal Yidoca vs alternativas)
- Sub-sesión futura: compra dominio yidoca.com + configurar email empresarial + conectar mailto: en "Agendar discovery"
- Sub-sesión futura: configurar herramienta de agenda (Cal.com/TidyCal cerca del salto comercial Oct-Nov 2026)
- Sub-sesión futura: aprender Next.js a fondo si hay tiempo de margen (15-30h)
- Sub-sesión futura: construir Demo 2 (propuestas o chatbot)
- Sub-sesión futura: Bloque 2.3 Make.com
- Sub-sesión futura: Bloque 2.5 HubSpot Workflows
- Sub-sesión futura: documentación profesional por demo (DOCUMENTACION/ carpeta con 4 archivos: arquitectura, código explicado, prompt engineering, historial decisiones)

### Estado al cierre

- Repo demo-scoring-leads: público, solo main, working tree limpio, 9 sesiones cronológicas (5, 6 y 9 retroactivas documentadas hoy)
- Demo desplegada: yidoca-scoring.streamlit.app pública, funcional, polish editorial Yidoca
- Pipeline landing → demo: conectado y validado en producción
- Sistema completo end-to-end de la primera demo de Yidoca: existente, funcional, compartible

### Dudas pendientes

- ¿Cuándo es momento de empezar a mostrar la demo a CEOs reales para validar interés? Decisión pendiente del fundador, no del mentor técnico. Probablemente Octubre-Noviembre 2026.
- ¿Mantengo solo demo de scoring o construyo Demo 2 (propuestas/chatbot) antes del salto comercial? Decisión meta de la propuesta de valor.
- ¿Compro dominio yidoca.com este mes o después de validación legal? Y0 con peso económico.
- ¿La demo necesita versión EN antes del salto comercial? ICP es España, probablemente no urgente.

### Acciones pendientes apuntadas (lista actualizada)

| Acción | Cuándo | Trabajo |
|---|---|---|
| Configurar email empresarial yidoca.com | Cuando compre dominio | 1-2h |
| Conectar "Agendar discovery" del CTA final landing demo con mailto: real | Cuando email funcione | 5 min |
| Conectar herramienta de agenda (Cal.com/TidyCal/Calendly) | Cerca salto comercial Oct-Nov 2026 | 30-60 min |
| Optimización responsive móvil landing demo si hay problemas | Sub-sesión específica | 1-2h |
| Compra dominio yidoca.com | Validación legal previa | Coste anual + 30 min setup |
| Backup repo institucional Yidoca a GitHub | Cuando tenga tiempo | 30-45 min |
| Adaptación visual demo Streamlit a dark/serif | Decisión arquitectónica primero | 4-6h |
| Aprender Next.js a fondo (Alternativa 2) | Cuando haya margen | 15-30h |
| Prompt engineering: añadir "Recomendación" por patrón | Sub-sesión específica | 1h + $0.40 reprocesado |
| Paralelización procesado leads | Sub-sesión específica | 1h |
| Capacidad upload CSV en vivo | Requiere API key como secret en Streamlit | 1.5-2h |
| Validación legal nombre comercial (EUIPO, OEPM, Mercantil) | Decisión estratégica | 30 min setup, ~10 días respuesta |
| Construir Demo 2 (propuestas o chatbot) | Decisión meta | 5-10h |
| Bloque 2.3 Make.com | Plan V3 | 6-8h |
| Bloque 2.5 HubSpot Workflows | Plan V3 | 4-6h |
| Documentación profesional por demo (DOCUMENTACION/ con 4 archivos) | Antes de mostrar a CEOs | 2-3h por demo |

---------------------------------------------------------------------------------------------------------------------

## Sesión 8 — 11 mayo 2026

**Duración real:** ~2h15
**Proyecto trabajado:** yidoca-demo-landing (no este repo)

Sesión dedicada al despliegue público de la landing demo en Vercel. Sin trabajo directo en este repo demo-scoring-leads.

**Resumen breve:**
- Conexión repo yidoca-demo-landing a Vercel
- Primera deployment exitosa en yidoca-demo-landing.vercel.app
- Fix de extensión imagen hero (jpg → png) — trampa Linux vs Windows
- Revisión exhaustiva de CTAs y corrección de hrefs
- Aceptación temporal del comportamiento "Agendar discovery" hasta tener email empresarial

**Documentación completa:** ver DIARIO.md del repo yidoca-demo-landing (sesión 2 en su numeración).

**Relación con este repo:** ninguna directa. La landing tenía CTAs "Lanzar demo" placeholder apuntando a sección interna; en sesión 9 se conectaron a este demo desplegado.

---------------------------------------------------------------------------------------------------------------------

## Sesión 7 — 10 mayo 2026

**Duración real:** ~2h30
**Proyecto trabajado:** yidoca-demo-landing (no este repo)

Sesión dedicada a la construcción inicial de la landing pública de la demo en v0/Next.js. Sin trabajo directo en este repo demo-scoring-leads.

**Resumen breve:**
- Construcción de la landing demo en v0 con prompt abierto
- Coherencia visual con landing institucional Yidoca (dark serif)
- Generación de imagen hero en Higgsfield (bodegón con caracteres japoneses 自働化)
- Descarga del ZIP de v0 + integración local de imagen
- Commit inicial a repo nuevo eruedazaldivar/yidoca-demo-landing (privado)

**Documentación completa:** ver DIARIO.md del repo yidoca-demo-landing (sesión 1 en su numeración).

**Relación con este repo:** ninguna directa. La landing apuntará eventualmente a este demo (conexión hecha en sesión 9).

---------------------------------------------------------------------------------------------------------------------

## Sesión 6 — 9 mayo 2026

**Duración prevista:** 2h
**Duración real:** ~2h (en rango)

### Qué hicimos

Sesión dedicada a iterar el rediseño visual de la demo de scoring usando v0 como referencia para una segunda versión más profesional. Trabajo realizado en rama exp_UI sin mergear a main.

Segundo intento con v0 (esta vez con prompt abierto):
- Prompt en inglés, narrativo, sin restricciones específicas
- v0 generó 4 capturas de mockups con estilo McKinsey internal tool
- Análisis de los mockups: KPIs nuevos (score medio, valor pipeline, con fricción), donut de distribución, cards apiladas con severidad codificada (Crítico/Atención/Info) con estructura DIAGNÓSTICO+RECOMENDACIÓN, panel lateral deslizante para detalle de lead

Decisiones de adaptación a Streamlit (qué tomamos del mockup v0 vs qué descartamos):
- 5 KPIs reales (sin "Valor pipeline" porque no tenemos datos de valor por lead)
- KPI 3 "Cuello de botella" calculado desde resultados (Timing 1.5/3, identificado en sesión 4)
- Cards apiladas en Capa 2 con 3 constantes nuevas en tono editorial Yidoca:
  - PATRON_DESCRIPCIONES: descripción narrativa de cada patrón
  - PATRON_SEVERIDAD: clasificación Crítico/Atención/Info por patrón
  - PATRON_DIMENSION_AFECTADA: dimensión principal asociada
- Refinamientos de copy:
  - Patrón presupuesto_insuficiente: "ciclo se alarga o no llega al cierre" (en lugar de "muere" — tono más profesional)
  - Patrón ideal_cliente: descripción "Todas las dimensiones" (en lugar de "Encaje perfecto" — más medible)
- Capa 3 reestructurada arquitectónicamente:
  - Inicial v0 propuso layout en st.columns([3,2]) con tabla a la izquierda y detalle a la derecha
  - Detectada zona muerta: cuando no hay lead seleccionado, la columna de detalle queda vacía generando vacío visual
  - Solución: tabla arriba ancho completo + panel detalle abajo ancho completo (vertical en lugar de horizontal)
  - Decisión: bloque héroe navy del detalle (que el mockup proponía) descartado en favor de panel sobre fondo crema (coherente con resto de la app)
- Selección reactiva implementada con on_select="rerun" + selection_mode="single-row"
- Key del selectbox con categoría+patrón para que resetee al cambiar filtros (decisión YAGNI sobre session_state)

Smoke tests funcionales:
- Filtros funcionan independientemente
- Cards Capa 2 expanden correctamente
- Tabla Capa 3 actualiza con filtros aplicados
- Panel detalle muestra trazabilidad completa (output → input)

Commit + push en rama exp_UI:
- Trabajo completo en rama experimental sin mergear a main
- Decisión consciente: mantener exp_UI viva hasta validar definitivamente (mergeada finalmente en sesión 9)

### Qué aprendí

- Prompts a v0 con referencias visuales (capturas) producen interpretación, no copia literal. Para obtener mockups inspiradores, mejor pasar el problema (no la solución) + tono + audiencia.
- Para SORPRENDER en herramientas LLM-driven (v0, Claude Code), no pedir tu solución actual con palabras nuevas. Pedir el problema y dar libertad real.
- Cuando el LLM (Claude Code o v0) ofrece opciones técnicas con trade-offs, no aceptar la primera. Pedir explícitamente la evaluación meta de la decisión.
- Construir en rama experimental, mergear cuando convencido. Disciplina profesional de Git que evita romper main.
- Cuando descubres una "zona muerta" en un layout (espacio que queda vacío sin contenido), reestructurar la arquitectura del layout es mejor que rellenar con contenido forzado.
- YAGNI (You Aren't Gonna Need It) aplica también a session_state de Streamlit: si el reset al cambiar filtros se resuelve con la key del selectbox, no necesitas variables de estado adicionales.
- Modificar el padding global de Streamlit (st.markdown con CSS custom) es patrón común en producción para apps con diseño cuidado.
- Constantes en tono editorial elevan la percepción del producto. PATRON_DESCRIPCIONES con tono profesional es radicalmente distinto a etiquetas técnicas.

### Decisiones tomadas

- Adaptación selectiva del mockup v0 (no copia 1:1). Mantener lo que aporta valor real, descartar lo que no encaja con datos o estilo Yidoca.
- 5 KPIs (no los del mockup) calculados desde los datos reales del CSV.
- Cards apiladas con severidad codificada (Crítico/Atención/Info) — nuevo paradigma visual en Capa 2.
- 3 constantes nuevas en scoring.py o módulo aparte: PATRON_DESCRIPCIONES, PATRON_SEVERIDAD, PATRON_DIMENSION_AFECTADA.
- Refinamiento de copy con tono más profesional ("ciclo se alarga", "todas las dimensiones") en lugar de tono coloquial.
- Capa 3 con layout vertical (tabla ancho completo arriba + detalle ancho completo abajo) en lugar de columnas horizontales con zona muerta.
- Panel detalle sobre fondo crema (no navy hero) para coherencia visual con el resto de la app.
- Selección reactiva con on_select + key compuesta + sin session_state adicional.
- Mantener exp_UI viva sin mergear hasta validar (mergeada finalmente en sesión 9).

### Próximos pasos

- Validar polish exp_UI vs main con uso prolongado
- Decidir cuándo mergear exp_UI a main (decisión tomada en sesión 9: ANTES del deploy)
- Pendiente: prompt engineering para añadir "Recomendación" por patrón

### Estado al cierre

- Rama exp_UI con rediseño completo Capas 1-2-3 funcionando localmente
- Smoke tests pasados (4 escenarios funcionales)
- main intacta (decisión de no mergear todavía)
- 3 constantes nuevas integradas en código

### Dudas pendientes

- ¿Mergeo exp_UI a main ahora o tras más uso? (Respondida en sesión 9: antes del deploy)
- ¿La demo necesita más capas o quedamos en 3? Decisión meta de la propuesta de valor.

---------------------------------------------------------------------------------------------------------------------

## Sesión 5 — 8 mayo 2026

**Duración prevista:** 2h
**Duración real:** ~2h (en rango)

### Qué hicimos

Sesión dedicada al polish editorial visual de la demo de scoring y al primer contacto con v0 como herramienta de diseño.

Cambio de marca de trabajo:
- TJC ("Takumi Jidoka Consultoría") → "Yidoca"
- Razón: TJC era nombre placeholder pesado; Yidoca es más fácil de recordar y pronunciar
- Validación legal queda pendiente (sub-sesión futura: EUIPO, OEPM, Mercantil)
- Actualización en CLAUDE.md del proyecto

Polish editorial de la demo Streamlit (rama exp_UI):
- Inspirado en la paleta y tipografía de la calculadora hermana (sesión 2)
- Paleta aplicada: crema #F5F1E8 fondo + navy #0A1628 texto principal + oro tierra acentos
- CSS global inyectado vía st.markdown con unsafe_allow_html=True
- Header editorial: "DEMO · SCORING DE LEADS" con eyebrows tracked + "YIDOCA" derecha
- Subhero: "Análisis diagnóstico de tu pipeline comercial."
- Tipografía Inter sans-serif coherente con calculadora

Detección y corrección de problemas de contraste:
- Bloque héroe original tenía fondo navy con texto navy oscuro → fallido de contraste
- Color verde oliva como acento perdía contraste sobre crema
- "_arrow_right" literal aparecía en algún lado del código
- Iteración correctiva: paleta refinada hacia oro tierra como acento (mejor contraste)

Iteración manual del fundador (no del mentor):
- Eduardo decidió colapsar Capa 1 (Visión agregada) + Capas 2 y 3 (Análisis por lead) en 2 dropdowns
- Razón: reducir densidad cognitiva de la app, permitir al usuario navegar progresivamente
- Resultado: portada de la app más limpia, 2 secciones expandibles claras
- Esta decisión la tomó el fundador autónomamente entre sesiones, no como propuesta del mentor

Primer contacto con v0 (bloqueado):
- Intento de pedir un rediseño a v0 con prompt restrictivo
- Incidente con upload de imágenes (no se pudo)
- Resultado: v0 produjo reproducción de la solución Streamlit existente (no aportó valor)
- Diagnóstico: prompt restrictivo + falta de referencia → resultado mediocre
- Lección capturada: para sorprender con LLMs, pedir el problema y libertad creativa, no la solución actual

Trabajo entre sesiones (Eduardo en paralelo):
- Briefing visual de la marca Yidoca redactado
- Copy de landing institucional redactado en otro chat

### Qué aprendí

- Cambios de marca de trabajo pueden ser frecuentes en fase de preparación. Conservar la disciplina de actualizar todos los lugares donde aparezca el nombre (CLAUDE.md, README, comments, etc.) ahorra confusión futura.
- Polish editorial radical (paleta nueva + tipografía + microcopy) puede aplicarse a una app Streamlit funcional sin reescribirla. CSS injection vía st.markdown es patrón estándar.
- Contraste de color es disciplina visual a verificar siempre. Texto sobre fondos similares (navy sobre navy, oliva sobre crema) falla en ciertos contextos y produce ilegibilidad.
- Prompts restrictivos generan reproducción de la solución actual. Para sorprender con LLMs, pedir el problema (no la solución) + audiencia emocional + libertad creativa explícita.
- v0 está optimizado para inglés. Aunque el producto final esté en español, los prompts a v0 en inglés producen mejores resultados.
- El instinto del fundador para tomar decisiones de UX (colapsar en dropdowns para reducir densidad cognitiva) sin esperar al mentor es valor real. El mentor técnico ejecuta; el fundador decide qué se ejecuta.
- Iterar visual de una app funcional es disciplina diferente a construirla desde cero. Hay capas (paleta → tipografía → microcopy → spacing → componentes específicos) que se pueden trabajar independientemente.

### Decisiones tomadas

- Cambio de marca de trabajo: TJC → Yidoca (validación legal pendiente)
- Polish editorial aplicado a la rama exp_UI: paleta crema/navy/oro tierra + Inter + microcopy editorial
- Header editorial "DEMO · SCORING DE LEADS" + wordmark YIDOCA
- 2 dropdowns para Capa 1 y Capas 2+3 (decisión del fundador, no del mentor)
- v0 abandonado en este intento por bloqueo de upload + prompt restrictivo. Retomar en sesión 6 con prompt abierto.
- Briefing visual de marca Yidoca redactado para futuras iteraciones

### Próximos pasos

- Probar de nuevo v0 con prompt abierto en inglés (sesión 6)
- Iterar Capas 2 y 3 con rediseño inspirado en v0 (sesión 6)
- Validación legal de "Yidoca" como nombre comercial (sub-sesión futura)

### Estado al cierre

- Rama exp_UI con polish editorial aplicado y funcional
- main intacta (sin polish, sin cambio de marca)
- 2 dropdowns implementados
- Briefing visual de marca Yidoca capturado externamente al repo

### Dudas pendientes

- ¿Yidoca es nombre comercial legalmente disponible? (Pendiente validación EUIPO/OEPM/Mercantil)
- ¿La portada con 2 dropdowns es la mejor UX? (Validado posteriormente en uso)
- ¿v0 puede aportar valor si lo usamos con otro prompt? (Respondida en sesión 6: sí, con prompt abierto)

---------------------------------------------------------------------------------------------------------------------

## Sesión 4 — 7 mayo 2026

**Duración prevista:** 1-2 horas
**Duración real:** ~2 horas (justo en el límite)

### Qué hicimos

Sesión dedicada a v0 a fondo + adaptación de los hallazgos a Streamlit en la rama `exp_UI`.

**Primer contacto profundo con v0**

- Login en `v0.dev` con GitHub.
- Aprendizaje de la sesión 5 aplicado: prompt corto y abierto en inglés ("Surprise me", referencia a McKinsey internal tool, libertad creativa total).
- Resultado: 4 capturas de v0 con dirección visual fuerte y diferenciada.
- v0 propuso decisiones que yo no habría tomado solo: KPIs adicionales (score medio, valor pipeline, con fricción), donut chart en lugar de bar chart, cards apiladas con severidad codificada en lugar de tabla de patrones, panel lateral deslizante para detalle de lead.

**Adaptación a Streamlit en rama `exp_UI` — 3 cambios estructurales con validación visual entre cada uno**

- **Cambio 1 — Capa 1 (5 KPIs + donut)**: sustituida la fila de 4 KPIs + bar chart por 5 elementos en `st.columns(5)`: Leads activos / Score medio /100 / Cuello de botella (Timing 1.5/3) / Con fricción / Donut Plotly. Donut con paleta editorial 4 colores tonales (verde oliva `#3D5A3F`, dorado tierra `#A88858`, terracota `#8B6F5C`, gris piedra `#7A716A`). Decisión KPI 3 "Cuello de botella" en lugar de "Patrón dominante" o "Eficiencia diagnóstica" — más narrativo, refuerza posicionamiento boutique.
- **Cambio 2 — Capa 2 (cards apiladas)**: sustituida la tabla de patrones + bar chart horizontal por cards apiladas. Cada card con `border-left` 4px del color de severidad, header con icono + nombre + meta-info + badge, cuerpo en 2 columnas DIAGNÓSTICO + RECOMENDACIÓN. 3 constantes nuevas creadas: `PATRON_DESCRIPCIONES` (textos editoriales tono Yidoca, notas de consultor sénior), `PATRON_SEVERIDAD` (Crítico/Atención/Info), `PATRON_DIMENSION_AFECTADA`. Severidades asignadas: Crítico (decisor_equivocado, fuera_icp_tamano, fuera_icp_sector, presupuesto_insuficiente) / Atención (dolor_generico_sin_diagnostico, decision_por_moda, conflicto_interes, buen_encaje_timing_largo) / Info (ideal_cliente, sistema_comercial_roto). "Recomendación" con placeholder por ahora — pendiente sub-sesión separada de prompt engineering.
- **Cambio 3 — Capa 3 (layout vertical ancho completo)**: el plan inicial era `st.columns([3, 2])` con tabla 60% / panel 40%. Tras render, detección de zona muerta a la derecha y compresión del panel. Decisión de cambio sobre la marcha: tabla arriba ancho completo + detalle abajo ancho completo. Tabla con selección reactiva (`st.dataframe` con `on_select="rerun"`, `selection_mode="single-row"`). Panel detalle con encabezado grid 2fr/1fr (nombre + score grande coloreado), 5 dimensiones en grid horizontal con barras coloreadas por valor, cuello de botella destacado, análisis estratégico + perfil empresa en grid 3fr/2fr, expander trazabilidad. Bloque héroe navy del detalle descartado en favor de panel sobre crema (coherencia visual con el resto de la app). Gestión de estado de fila seleccionada: opción simple (key con `cat_sel + pat_sel` — selección se resetea al cambiar filtros mayores) en lugar de `session_state` complejo (decisión YAGNI).

**Cierre**

- 4 smoke tests funcionales pasados (3 capas, selección, filtros, expander).
- Commit y push de `exp_UI` con todos los cambios. Mantener `exp_UI` abierta — no mergear a `main` todavía. Mergeará cuando ejecute al menos una demo real con prospecto y la versión aguante.

### Qué aprendí

- **Los prompts a v0 deben ser cortos y abiertos para que la herramienta sorprenda.** Mismo principio que descubrí con Claude Code en `calculadora-capacidad`. Es disciplina universal de generación con LLMs, no específica de una herramienta concreta.
- **v0 está optimizado para inglés.** Redactar prompts en inglés aunque el producto sea en español. La calidad del output cambia sensiblemente.
- **Cuando una herramienta de generación me ofrece opciones técnicas con trade-offs, no decido yo directamente: escalo al mentor para evaluación meta.** La tecnología es medio, la decisión es sobre el producto.
- **Las operaciones irreversibles** (merge a `main`, force push, delete branch) **merecen pausa adicional incluso aunque el trabajo se vea bien.** La duda razonable cuesta menos que el rollback.
- **Mi propio instinto de UX gana ocasionalmente al criterio del mentor.** Específicamente: cuando el mentor propone un layout porque "es lo que hace v0" o "es el patrón estándar", mi pregunta "¿pero esto realmente funciona en mi pantalla con mi uso?" produce mejores resultados.
- **Modificar el padding global de Streamlit es patrón común** en producción para apps "tipo informe", no dashboards genéricos. La diferencia entre "se ve a Streamlit" y "se ve a producto curado" pasa por ahí.
- **Capturar v0 visualmente y describir con criterio "qué decisiones tomó que yo NO habría tomado" abre vocabulario visual nuevo.** v0 no es para copiar — es para ver qué es posible. La pregunta correcta no es "¿lo aplico?" sino "¿qué intuición visual tenía v0 que a mí se me había escapado?"
- **La feature de selección reactiva en `st.dataframe`** (`on_select="rerun"`) es estable desde Streamlit 1.35. Permite UX moderna sin necesidad de `session_state` complejo en muchos casos. Cambia lo que se puede pedirle a Streamlit como herramienta de prototipado.
- **Iterar visualmente entre cada cambio estructural** (Cambio 1 → validar → Cambio 2 → validar → Cambio 3 → validar) **es disciplina cara pero ahorra rollbacks dolorosos.** Si hubiera aplicado los 3 de un tirón, el cambio de plan en Capa 3 (de columnas a vertical) habría requerido deshacer mucho.
- **Las descripciones de patrones en Yidoca tienen voz: notas de consultor sénior, no marketing genérico.** Frases tipo "El dolor está articulado y el problema apunta a nuestro lenguaje" son la diferencia entre boutique premium y dashboard SaaS.

### Decisiones tomadas

- **5 KPIs en Capa 1 con métricas reales calculables** — sin inventar campos como "valor pipeline" sin datos.
- **KPI 3 "Cuello de botella"** como métrica diagnóstica destacada, no "Patrón dominante" ni "Eficiencia diagnóstica".
- **Donut compacto en columna 5** (en lugar de fila propia) — funcionó visualmente, no hizo falta plan B.
- **"Recomendación" por patrón = pendiente** para sub-sesión separada de prompt engineering. Modificar prompt de scoring + reprocesar 50 leads + validar calidad.
- **Cards apiladas con severidad por color** en Capa 2 (no tabla).
- **Severidades asignadas con justificación**: Crítico = bloqueo estructural (no se neutraliza con tiempo), Atención = fricción cualitativa neutralizable, Info = señales positivas que destacar.
- **Layout vertical en Capa 3** (no 2 columnas) — mejor uso del ancho de pantalla y composición tipo informe.
- **Bloque héroe navy del detalle descartado** — coherencia visual sobre presencia gráfica.
- **Selección con key dinámica** que resetea al cambiar filtros, en lugar de `session_state` (YAGNI).
- **Mantener `exp_UI` abierta**, no mergear a `main` todavía.

### Próximos pasos

- **Sub-sesión de prompt engineering**: añadir "Recomendación" por patrón. Modificar prompt de scoring, reprocesar 50 leads, validar la calidad de las recomendaciones generadas.
- **Sub-sesión 4D opcional de ajustes finos**: validar si el donut necesita diferenciación visual adicional, si las 5 dimensiones se ven apretadas en pantallas grandes, si el header del lead necesita ajuste de proporciones.
- **Decisión de merge `exp_UI` → `main`**: tras ejecutar al menos una demo real con prospecto.
- **Despliegue público de la demo** (Streamlit Cloud o Render) — cierre del bloque 2.2 del plan V3.
- **Paralelización del procesado de leads** (3 min secuencial → 30 seg paralelo).
- **Capacidad de upload de CSV en vivo** en la demo.
- **Decisión final del nombre comercial** (Yidoca vs alternativas) — sub-sesión estratégica futura.
- **Construir Demo 2** (propuestas o chatbot).
- **Bloque 2.3 Make.com**.
- **Bloque 2.5 HubSpot Workflows**.
- **`DOCUMENTACION/` por demo** cuando estén estables.

### Estado al cierre

`main` intacta y funcional con la versión de la sesión 5 (UI con polish editorial Yidoca + iteraciones manuales del fundador). Rama `exp_UI` con rediseño profundo de Capas 1-2-3 inspirado en v0, respaldada en GitHub (`origin/exp_UI`). Demo más robusta narrativamente: 5 KPIs reales + cards apiladas con diagnóstico/recomendación + layout informe ancho completo. Pendiente decidir el merge cuando haya prueba real en demo con prospecto.

### Dudas pendientes

- ¿Las recomendaciones por patrón (cuando se implementen) deben ser genéricas para todos los leads del patrón, o personalizadas por lead? Decisión de prompt engineering pendiente.
- ¿El merge a `main` lo hago tras 1 demo real, o tras 3-5 demos para validar resistencia al uso real?
- ¿Los ajustes finos visuales pendientes (donut, dimensiones, score) los hacemos antes del merge o después?

---------------------------------------------------------------------------------------------------------------------

## Sesión 3 — 6 mayo 2026

**Duración prevista:** 2-3 horas
**Duración real:** ~2 horas

### Qué hicimos

**Sub-sesión 4C — Polish creativo de la UI Streamlit (rama experimental)**

- Smoke test del entorno (venv + `test_api.py` respondió OK + `git status` limpio).
- Creación de la rama `exp_UI` para iterar el polish sin tocar `main`.
- Lectura del proyecto hermano `calculadora-capacidad` como referencia visual: Claude Code accedió a `index.html`, `css/styles.css` y `CLAUDE.md` para identificar el lenguaje visual (paleta crema/navy/oro tierra, tipografía Inter editorial, kickers eyebrow uppercase con líneas finas, marcas de agua sobre fondo oscuro, layout magazine).
- Decisión de marca de trabajo: **TJC / TAKUMI JIDOKA → "Yidoca"**. Más accesible foneticamente para el ICP español. Decisión final del nombre comercial sigue abierta para sesión estratégica futura.
- Plan estructurado de polish por secciones aprobado antes de ejecutar — disciplina aprendida de sesiones anteriores.
- Aplicación: CSS global inyectado vía `st.markdown(unsafe_allow_html=True)` en una función `aplicar_estilos_yidoca()`, `.streamlit/config.toml` con tema base coherente, KPI cards crema custom HTML (sustituyen `st.metric`), bar charts Plotly tematizados con paleta navy, bloque héroe navy profundo con marca de agua "Yidoca" en `opacity 0.18`, footer editorial.
- Detección de problemas en el primer render: contraste fallido en el bloque héroe (textos oscuros sobre navy oscuro, ilegibles), expander mostrando `_arrow_right` literal (la fuente Material Symbols pisada por mi propio override global), color verde oliva profundo con poco contraste sobre navy.
- Iteración correctiva: textos del bloque héroe pasados a cream/cream-soft con `!important` por defensa en profundidad, `span`/`div` retirados del override de `font-family !important` para devolver el control de Material Symbols a Streamlit, escala de color de la puntuación recalibrada a tonos brillados (`#8FA77B / #C4A77B / #B89281 / #A8A39B`) que leen sobre navy.
- Iteración propia por mi cuenta sobre la estructura: colapso de las tres capas en dos dropdowns (`Visión agregada` que agrupa Capa 1+2, `Análisis por Lead` que contiene la 3 con un expander anidado de información original). Reduce densidad cognitiva y controla la narrativa al abrir solo lo que el cliente necesita en cada momento del discovery.

**Primer contacto con v0 (parte del bloque 2.2 del plan V3)**

- Setup en `v0.dev` con login GitHub.
- Primer prompt construido: largo, detallado, con hex codes obligatorios y especificaciones cerradas.
- Primer mockup de v0 prácticamente idéntico a lo que ya teníamos en Streamlit. Sin sorpresa.
- Identificación clara del problema: prompts restrictivos generan reproducción de la solución actual, no exploración real. Mismo error que cometí en la sesión 1 con la calculadora.
- Segundo prompt corto y abierto preparado ("Surprise me", McKinsey internal tool, libertad creativa total).
- Bloqueo por incidente del chat: imposibilidad de subir capturas de pantalla durante el contacto con v0. Sub-sesión interrumpida.

**Cierre**

- Decisión: la rama `exp_UI` se mantiene viva, no se mergea a `main` todavía. Pendiente iterar más con v0 cuando se restablezca la subida de imágenes.
- Push de `exp_UI` a `origin` con upstream configurado, respaldada en GitHub aunque no esté integrada en `main`.

### Qué aprendí

- **El principio "prompts restrictivos vs prompts creativos" se aplica a TODAS las herramientas de generación con LLM.** Claude Code, v0, Lovable, cualquier futuro generador. Es disciplina universal, no específica de una herramienta. Si le das al modelo las restricciones de tu solución actual, te devuelve tu solución actual. Sin sorpresa.
- **Para que un LLM te sorprenda visualmente, hay que darle el problema y no la solución.** Audiencia emocional + libertad creativa explícita + jaula clara solo donde es innegociable. La fórmula que aprendí en la calculadora aplica idéntica aquí.
- **v0 y Streamlit son mundos técnicos distintos** (React/Next.js vs Python). v0 sirve como herramienta de **inspiración visual**, no como generador de código directamente integrable en Streamlit. Mezclar ambas cosas confunde la decisión.
- **Tres approaches con v0 según ambición**: (1) inspiración visual capturando screenshots, (2) reconstruir todo en Next.js (15-30h adicionales), (3) híbrido con landing en v0 + demo en Streamlit. Para la fase actual de preparación silenciosa, el approach 1 es lo correcto. Los otros dos son trabajo que puede esperar.
- **Capturar v0 visualmente es mi propio cuello de botella operativo.** El upload de imágenes en chat es la palanca crítica para iterar con v0. Cuando vuelva, hay que reservar tiempo de calidad para esa sesión.
- **Iniciativa propia: detectar el ruido cognitivo de "todo a la vista" y resolverlo con desplegables.** Mucha información mostrada de golpe sobrecarga al cliente en discovery. La narrativa se controla decidiendo qué se ve y cuándo. Lección de UX que aplica a cualquier dashboard futuro.

### Decisiones tomadas

- **"Yidoca" como marca de trabajo** durante el desarrollo. Decisión final del nombre comercial sigue abierta para sub-sesión estratégica futura.
- **Polish editorial con paleta crema/navy/oro tierra** coherente con la calculadora hermana.
- **4 colores tonales para puntuaciones** (verde oliva / dorado tierra / terracota apagado / gris piedra) en lugar de rojo/amarillo/verde de semáforo. Editorial, no SaaS.
- **Rama experimental `exp_UI` se mantiene abierta**, `main` no se toca hasta tener convicción real del polish con la inspiración v0 incorporada.
- **v0 se explora como inspiración (Approach 1)**, no como herramienta de migración técnica. Sin Next.js todavía.
- **Sub-sesiones futuras pendientes**: v0 a fondo (cuando vuelva el upload) + despliegue público (resto del bloque 2.2 del plan).
- **Colapso de secciones en 2 dropdowns** como mejora UX, integrada en la rama experimental.

### Próximos pasos

- **Sesión 6: v0 a fondo cuando vuelva la subida de imágenes.** Sub-sesión completa de exploración visual con prompt creativo abierto + adaptación selectiva a Streamlit.
- **Sesión 7 (o cuando proceda): despliegue público de la demo** (Streamlit Cloud o Render). Cierre del bloque 2.2 del plan V3.
- **Sesión estratégica futura: decisión final del nombre comercial** (Yidoca, Takumi Consulting, otro). Verificación legal EUIPO/OEPM. Test de pronunciación con 3-5 ICP.
- **Sesión técnica futura: paralelización del procesado de leads** (de 3 min secuencial a 30 seg paralelo).
- **Sesión técnica futura: capacidad de upload de CSV en vivo** en la demo.

### Estado al cierre

`main` intacta y funcional con la versión de la sesión 4 (UI funcional sin polish editorial). Rama `exp_UI` con polish editorial Yidoca aplicado, respaldada en GitHub (`origin/exp_UI`). Demo funcional, presentable y narrativamente coherente desde `main`. Versión "premium" en rama experimental para iteraciones futuras. Pendiente desbloquear v0 con upload de imágenes para iteración profunda.

### Dudas pendientes

- ¿Qué porcentaje de v0 acabaremos incorporando a Streamlit cuando volvamos a ello? Decisión a tomar tras ver mockups con prompt creativo abierto.
- Decisión final sobre nombre comercial. No urgente. Decisión Y0 con peso.
- ¿Mantener la rama experimental viva o mergearla cuando haya iteración suficiente con v0? Decisión a tomar en sesión 6 según resultado.

---------------------------------------------------------------------------------------------------------------------

## Sesión 2 — 4 mayo 2026

**Duración prevista:** 3+ horas
**Duración real:** ~5 horas (sub-sesión 4A mañana ~2h, sub-sesión 4B tarde ~2h45)

### Qué hicimos

**Sub-sesión 4A (mañana, ~2h) — Lógica de scoring de leads**

- **Decisión estratégica de versión:** scoring estratégico/diagnóstico (Versión B), no scoring táctico (Versión A). Coherente con el posicionamiento de boutique de "diagnóstico antes que propuesta".
- Diseño del flujo de la demo en 3 capas: visión agregada, patrones detectados, leads individuales.
- Modelo de evaluación: 5 dimensiones (`encaje_icp`, `madurez_problema`, `capacidad_decision`, `timing`, `capacidad_presupuestaria`) con escala 0-3 cada una. Categorización derivada (Encaje claro 13-15, parcial 9-12, débil 5-8, no encaje 0-4).
- Generación de 50 leads ficticios con distribución realista (10 buenos, 20 parciales, 15 débiles, 5 fuera) y patrones repetidos: `decisor_equivocado`, `fuera_icp_tamano`, `sistema_comercial_roto`, etc.
- Prompt engineering del scoring: system prompt detallado con ICP, productos, dimensiones, lista cerrada de patrones y formato JSON obligatorio.
- Test con 3 leads → detección de bug: el modelo envuelve el JSON en bloques de markdown a pesar de la instrucción negativa "NO añadas markdown".
- Solución defensiva en dos capas: función `limpiar_respuesta_json()` en código + refuerzo del prompt con instrucción positiva ("DEBE empezar con `{`"). Tras los cambios, parseo limpio en los 3 leads de prueba.
- Refactor a `scoring.py` para reutilización entre `test_scoring.py` y `procesar_leads.py`.
- Procesamiento secuencial de los 50 leads con barra de progreso (3 min 34 seg, $0.40 USD).
- Análisis agregado con `analizar_resultados.py`: distribución sana (38% Encaje claro, 24% parcial, 26% débil, 12% no encaje), integridad 100% (cero inconsistencias suma de dimensiones vs puntuación total), cuello de botella sistemático identificado en dimensión `timing` (1.50/3 promedio).

**Sub-sesión 4B (tarde, ~2h45) — UI Streamlit en 3 capas**

- Diseño de la UI siguiendo las 3 capas planteadas en 4A. Construcción incremental capa por capa, con ajustes intermedios antes de pasar a la siguiente.
- **Capa 1** (visión agregada): KPIs neutralizados sin flechas + bar chart vertical. Migración desde `st.bar_chart` a Plotly por necesidad de control sobre orden de categorías y etiquetas horizontales.
- **Capa 2** (patrones detectados): tabla de patrones con labels humanos (no identificadores técnicos) + bar chart horizontal con barra más larga arriba + 5 KPIs de promedio por dimensión + frase interpretativa dinámica que muta según la dimensión más débil detectada en cada ejecución.
- **Capa 3** (leads individuales): filtros en horizontal (categoría/patrón/búsqueda) + tabla con `column_config` (anchos ajustados, formato `X/15`) + panel de detalle con puntuación grande coloreada (verde/ámbar/rojo según rango) + expander con la información original del CSV. Eliminación de toda mención al modelo o IA en strings visibles al usuario.
- Falsa alarma de "discrepancia de datos" entre análisis y app: error de comparación al revisar números, los datos eran consistentes. Verificación adicional con `git status` confirmando que `resultados.json` no se había modificado desde el commit anterior.
- Cierre técnico: `requirements.txt` generado vía `pip freeze` para reproducibilidad del entorno (58 paquetes congelados, 6 directos: `streamlit`, `anthropic`, `pandas`, `plotly`, `python-dotenv`, `tqdm`).

### Qué aprendí

- **Los modelos no obedecen siempre las instrucciones del prompt al 100%.** Las instrucciones negativas ("NO hagas X") son menos fiables que las positivas ("DEBE hacer Y"). La defensa robusta es prompt reforzado en ambos sentidos + función defensiva en código que limpie el output. Asumir que el modelo va a desviarse y prepararse para ello.
- **Refactor temprano a módulo compartido evita deuda técnica.** El momento de extraer `scoring.py` fue cuando me iba a duplicar las constantes y funciones entre dos scripts. Si esperas, cada cambio futuro hay que aplicarlo en N sitios.
- **Streamlit es declarativo y rápido para prototipos, pero tiene techo.** `st.bar_chart()` está bien para casos casuales; para control fino (orden, etiquetas horizontales, colores específicos), saltar a Plotly directamente. Lo identifiqué tarde y en Capa 1 hubo que reescribir el gráfico.
- **Construir UI capa por capa permite detectar problemas pronto.** Si hubiera intentado escribir las 3 capas de un tirón antes de testear, habría acumulado fricción visual y tareas de reajuste. El bucle "construye → mira → ajusta → siguiente capa" funciona muy bien con Streamlit.
- **La trazabilidad del output al input es central en sistemas de IA aplicada a consultoría.** Sin la información original visible, el sistema parece "magia". Con ella visible, es "consultoría auditable". Esta es la diferenciación entre boutique y SaaS commodity: el cliente no compra un score, compra el razonamiento sobre datos que reconoce.
- **Los datos sin interpretación son ruido.** La frase "el cuello de botella sistemático está en timing" vale más que la tabla de números que la sustenta. La frase interpretativa dinámica de Capa 2 nació por esto.
- **Mi instinto estético sobre la UI es válido y conviene aplicarlo.** Mi tendencia natural es pedir lo mínimo (`st.metric`); cuando empujé hacia más (puntuación grande con color), el resultado fue mejor. La fórmula que aprendí de la calculadora aplica también aquí: jaula clara + permisos amplios + objetivo emocional.

### Decisiones tomadas

- **Versión B (scoring diagnóstico/estratégico)** en lugar de Versión A (priorización táctica). Coherente con la propuesta de la boutique: diagnóstico antes que propuesta.
- **5 dimensiones, 4 categorías, 10 patrones cerrados.** El espacio de salida es enumerable y eso permite agregados estables y analítica posterior.
- **50 leads ficticios, no 10.** Realismo del tamaño de un pipeline PYME + masa estadística suficiente para que los patrones agregados sean significativos.
- **Procesamiento secuencial primero**, con barra de progreso (~4 seg/lead). Optimización a paralelo queda para una sesión futura cuando haya razón para hacerlo.
- **CSV con comas estándar**, no punto y coma de Excel español. Compatibilidad amplia.
- **Refactor a `scoring.py` reutilizable** entre los scripts de test, procesamiento y app.
- **UI: Streamlit por defecto + Plotly para gráficos** donde Streamlit nativo se queda corto.
- **Trazabilidad obligatoria con expander cerrado**, no abierto: la narrativa controla el orden de revelación durante un discovery.
- **Cero menciones al modelo o IA en strings visibles al usuario.** El producto es "análisis estratégico", no "razonamiento de Claude". Para una demo a CEOs.
- **Polish estético creativo** (escala de colores, tipografía, etc.) se aborda en sub-sesión 4C en rama experimental cuando se decida.
- **`requirements.txt` creado al cierre** vía `pip freeze` para reproducibilidad del venv en otras máquinas o colaboradores futuros.

### Próximos pasos

- **Posible Sub-sesión 4C:** rama experimental para polish visual creativo de la app, en línea con TJC y boutique premium. Aplicar fórmula de prompt creativo (jaula clara + permisos amplios + objetivo emocional + referencia a `CLAUDE.md`).
- **Pendiente UX:** añadir capacidad de subir CSV nuevo y reprocesar en vivo (actualmente la app solo carga `resultados.json` precomputado).
- **Pendiente optimización:** paralelización del procesamiento de leads (de secuencial 3 min a paralelo ~30 seg).
- **Decisión a tomar:** si hace falta una Sub-sesión 4D antes de pasar a la siguiente demo (propuestas o chatbot).

### Estado al cierre

Demo de scoring funcional y narrativa coherente, lista para pruebas internas. 3 capas implementadas con datos reales validados. Trazabilidad de output a input implementada. Coste por ejecución completa: $0.40 USD; con $50 USD iniciales hay margen para ~125 ejecuciones. 5 archivos Python en el repo (`scoring.py` como módulo compartido, `test_scoring.py`, `procesar_leads.py`, `analizar_resultados.py`, `app.py` con UI Streamlit) + 50 leads ficticios + `resultados.json` + `resultados.csv` + `requirements.txt`. Repo sincronizado con GitHub, varios commits descriptivos en `main`.

### Dudas pendientes

- ¿Cuándo añadir capacidad de upload de CSV en vivo? Decisión a tomar tras pruebas internas con la versión actual: si el discovery se siente forzado por la rigidez de los datos pre-cargados, se prioriza; si fluye, espera.
- ¿Mantener `resultados.json` y `resultados.csv` en Git o moverlos a `.gitignore`? Para la versión actual los mantengo como "prueba" reproducible de que la demo funcionó. Para producción real irán a `.gitignore`.

---------------------------------------------------------------------------------------------------------------------

## Sesión 1 — 3 mayo 2026

**Duración prevista:** 2-3h
**Duración real:** ~2h45 con pausa de comida en medio

### Qué hicimos

**Fase 0 (~60 min) — Instalación de Python desde cero**

- Detectamos que Windows tenía un alias trampa de Microsoft Store que redirigía `python` a la Store en vez de a un intérprete real. Lo desactivamos en Configuración → Aplicaciones → Alias de ejecución de aplicaciones.
- Decidimos instalar Python 3.12.10 en lugar de la última (3.14) por compatibilidad con el ecosistema de librerías. La regla de "última versión disponible" no se aplica al runtime de Python: muchas librerías llevan semanas o meses en alcanzar la versión más reciente.
- Instalación con las dos casillas críticas marcadas: *Add Python to PATH* y *Use admin privileges*.
- Verificación con `python --version`, `pip --version` y `where.exe python` para confirmar que la PATH apunta al intérprete correcto y no al alias.

**Fase 1 (~45 min) — Entorno virtual + Streamlit operativo**

- Concepto de entornos virtuales (`venv`): por qué son obligatorios en Python profesional, qué problema resuelven (aislamiento de dependencias por proyecto, evitar conflictos de versiones entre proyectos).
- Creación del primer venv en el proyecto `demo-scoring-leads` con `python -m venv .venv`.
- Resolución del error de execution policy en PowerShell al activar el venv: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`. Suficiente para developers, no abre la puerta a scripts arbitrarios de internet.
- Activación del venv con `.\.venv\Scripts\Activate.ps1` y verificación visual del prefijo `(.venv)` en el prompt.
- Instalación de `streamlit` y `anthropic` con `pip install`. Arrastraron 60+ dependencias transitivas (numpy, pandas, pillow, httpx, pydantic, etc.).
- Creación del primer `app.py` con un "Hello Streamlit" mínimo. `streamlit run app.py` abrió el navegador en `localhost:8501` y validó que el stack funciona end-to-end.

**Fase 2 (~45 min) — Cuenta Anthropic + secretos + primera llamada a la API**

- Cuenta nueva en `console.anthropic.com`, separada de la cuenta de `claude.ai` (consumer vs developer son productos distintos con facturación distinta).
- Carga inicial de $50 USD en créditos. Cálculo a vuelo de pájaro: suficiente para sesiones 3-5 con margen amplio.
- Generación de la primera API key con nombre descriptivo: *"Eduardo - Demo Scoring Leads - Sesion 3"*. Disciplina: que el nombre indique para qué se usa, no genérico tipo "key1".
- Configuración profesional de gestión de secretos:
  - `.env` con la API key real (en `.gitignore`, nunca se commitea).
  - `.env.example` como template público (sin valores reales, sí commiteable). Permite que cualquiera que clone el repo entienda qué variables hace falta definir.
  - `.gitignore` reforzado con `.env*` para cubrir variantes (`.env.local`, `.env.production`, etc.).
- `test_api.py` para validar conectividad: `load_dotenv` → `os.getenv` → `Anthropic(api_key)` → `client.messages.create`. Llamada real al modelo `claude-sonnet-4-5`, respuesta correcta, 63 tokens consumidos, coste aproximado de $0.0007 USD.

**Fase 3 (~15 min) — Git + GitHub**

- `git init`, branch a `main`, primer commit con los 4 archivos del setup (`.env.example`, `.gitignore`, `app.py`, `test_api.py`). Verificación previa de que `.env` real no apareciera en staging.
- Repositorio privado creado en GitHub (`github.com/eruedazaldivar/demo-scoring-leads`), remoto conectado, `git push -u origin main`. Credenciales tomadas automáticamente del Credential Manager de Windows desde sesiones anteriores.

### Qué aprendí

- **Python global vs entornos virtuales aislados.** Un Python global compartido entre proyectos es una bomba de tiempo: una librería actualizada por un proyecto puede romper a otros. El venv resuelve esto con aislamiento por carpeta. Es la primera disciplina obligatoria del Python profesional.
- **"Última versión disponible" ≠ "versión correcta para tu caso".** En Python, el ecosistema de librerías va por detrás del runtime. Hoy 3.12 es más segura que 3.14 simplemente por compatibilidad: las librerías han tenido meses para adaptarse. La regla de "lo último siempre" funciona en consumer software, no en runtimes con ecosistema de paquetes.
- **El alias trampa de Python en Windows.** Windows incluye un stub que redirige `python` a la Microsoft Store si no encuentra un intérprete real. Es invisible hasta que rompe algo. Se desactiva en *Configuración → Aplicaciones → Alias de ejecución de aplicaciones*. Lección genérica: cuando un comando hace algo raro en Windows, sospechar de aliases del sistema antes que del propio comando.
- **PowerShell y políticas de ejecución de scripts.** Por defecto PowerShell bloquea ejecución de scripts `.ps1` por seguridad. `RemoteSigned -Scope CurrentUser` es el equilibrio adecuado para developers: permite scripts locales propios, exige firma a los descargados de internet, y solo afecta a mi usuario (no al sistema).
- **Patrón profesional de gestión de secretos.** `.env` real (privado, en `.gitignore`) + `.env.example` (template público, sí commiteable) + `.gitignore` protegiendo es el patrón estándar. Sirve para cualquier API: Anthropic, OpenAI, HubSpot, Stripe, lo que venga. Asumirlo ya como convención evita reinventar el patrón en cada proyecto.
- **Anatomía de una llamada a la API de Anthropic desde Python.** `load_dotenv()` carga el `.env` al entorno → `os.getenv("ANTHROPIC_API_KEY")` recupera la key → `Anthropic(api_key=...)` instancia el cliente → `client.messages.create(model, max_tokens, messages)` ejecuta la llamada. Patrón aplicable a cualquier integración LLM.
- **Estructura del response.** `response.content[0].text` para el texto generado, `response.usage.input_tokens` y `response.usage.output_tokens` para tracking de coste. Saber esto desde el día 1 evita tener que vigilar el coste en el dashboard de Anthropic — se puede instrumentar localmente.
- **Lección operativa: Ctrl+S antes de probar cualquier cambio.** Hoy se me olvidó guardar y perdimos 15 minutos buscando un archivo que no existía en disco (existía en el buffer del editor pero no estaba persistido). Es disciplina muscular básica que se interioriza con repetición.
- **Lección operativa: verificar el foco en el panel izquierdo de VS Code antes de "New File".** Si tengo seleccionada una subcarpeta como `.venv` y creo un archivo nuevo, se crea ahí dentro en lugar de en la raíz del proyecto. Trivial pero confunde si no se detecta a tiempo.
- **Lección sobre venvs: cada nueva terminal requiere reactivación.** El venv no persiste entre sesiones de terminal. Cada vez que abro una nueva: `.\.venv\Scripts\Activate.ps1`. Es disciplina que se interioriza tras varias semanas de uso.

### Decisiones tomadas

- **Python 3.12.10** (no 3.14) por compatibilidad con el ecosistema de librerías.
- **`console.anthropic.com` como cuenta de developer separada de `claude.ai`.** Productos distintos, facturación distinta, mejor mantenerlos limpios desde el principio.
- **$50 USD iniciales en créditos** en la cuenta Anthropic. Cálculo conservador para cubrir sesiones 3-5 con margen.
- **API key con nombre descriptivo** (*"Eduardo - Demo Scoring Leads - Sesion 3"*) en lugar de genérico. Si en el futuro hay varias keys activas, sé de un vistazo cuál es cuál.
- **`python-dotenv`** como librería estándar para gestión de secretos en todos los proyectos Python con API keys.
- **`claude-sonnet-4-5`** como modelo default para las demos: balance correcto precio/calidad para el tipo de tarea que se va a hacer (scoring estructurado de leads, no generación creativa larga).
- **Patrón `.env` + `.env.example` + `.gitignore`** como convención que se aplicará por defecto a todos los proyectos futuros con secretos.
- **`test_api.py` se mantiene en el repo** como referencia y herramienta de verificación rápida de conectividad. No se borra una vez validado el setup.

### Próximos pasos

- **Sesión 4: empezar la demo de scoring de leads de verdad.** Definir inputs (un CSV de leads ficticios con campos plausibles), prompt (qué le pedimos al modelo y con qué estructura), output (puntuación numérica + razonamiento estructurado por dimensiones). Construir versión funcional end-to-end.
- **Antes de la sesión 4: preparar 5-10 leads ficticios** con datos plausibles: empresa, sector, tamaño, dolor declarado, antigüedad de contacto, canal de entrada, etc. La calidad de los leads de prueba determina la calidad de la demo.
- **Decidir el modelo de interacción:** scoring por CSV en batch (sube fichero, devuelve resultados) o uno a uno interactivo (introduce datos, ves la respuesta). Cada uno tiene un tipo de discovery distinto al que sirve mejor.

### Estado al cierre

Stack Python 3.12 + Streamlit + Anthropic SDK operativo. Setup de secretos correctamente implementado (`.env` real protegido, `.env.example` commiteable como template). Conectividad con la API de Claude validada con llamada real (Sonnet 4.5, 63 tokens, ~$0.0007 USD). Repositorio privado `github.com/eruedazaldivar/demo-scoring-leads` sincronizado con un commit en `main`. Todo respaldado.

### Dudas pendientes

- ¿La demo de scoring debería incluir feedback en streaming (tokens apareciendo en tiempo real, efecto "el modelo está pensando") o respuesta completa al final? El streaming impresiona más en discovery pero añade complejidad de implementación. Decisión a tomar al inicio de la sesión 4.

---------------------------------------------------------------------------------------------------------------------
