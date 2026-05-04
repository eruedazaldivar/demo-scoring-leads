# Diario de aprendizaje — Demo scoring de leads

Registro de sesiones de trabajo sobre el proyecto de demo de scoring de leads con la API de Claude. Apunto qué hago, qué aprendo, qué decido y por qué. Las sesiones van en orden cronológico inverso: la más reciente arriba.

---

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

---

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

---
