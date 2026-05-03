# Diario de aprendizaje — Demo scoring de leads

Registro de sesiones de trabajo sobre el proyecto de demo de scoring de leads con la API de Claude. Apunto qué hago, qué aprendo, qué decido y por qué. Las sesiones van en orden cronológico inverso: la más reciente arriba.

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
