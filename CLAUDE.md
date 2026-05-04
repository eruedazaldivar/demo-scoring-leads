# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Proyecto

Demo educativa de **scoring de leads** con la API de Claude. Streamlit como front, Anthropic SDK como backend de IA. El proyecto se construye en sesiones documentadas en `DIARIO.md` y, a fecha del último commit, está en el cierre de la Sesión 1: setup terminado, sin funcionalidad de scoring todavía.

El idioma del proyecto (código, UI, comentarios, docs, commits) es **español**. Mantenlo así salvo que el usuario pida lo contrario.

## Comandos habituales

Todos los comandos asumen el venv activado. **El venv NO persiste entre terminales nuevas — hay que reactivarlo cada vez:**

```powershell
.\.venv\Scripts\Activate.ps1     # PowerShell (Windows, el shell del usuario)
```

Operaciones frecuentes:

```powershell
streamlit run app.py             # Levanta la app en http://localhost:8501
python test_api.py               # Smoke test de conectividad con la API de Claude
pip install <paquete>            # Instalar dependencia nueva (siempre con venv activado)
pip freeze                       # Ver qué hay instalado
```

No hay `requirements.txt` ni `pyproject.toml` todavía: las dependencias se instalan a mano (`streamlit`, `anthropic`, `python-dotenv` y sus transitivas). Si añades dependencias importantes, propón al usuario congelar a `requirements.txt` antes de hacerlo unilateralmente.

No hay tests ni linter configurados. No hay pipeline de CI.

## Arquitectura

Repositorio plano de momento. Dos puntos de entrada:

- [app.py](app.py) — La app Streamlit. Hoy es un "Hello World". Aquí irá la UI de scoring.
- [test_api.py](test_api.py) — Verificación de conectividad con la API. **No borrar** aunque el docstring sugiera que se puede: el usuario decidió mantenerlo como herramienta diagnóstica permanente (ver Sesión 1 en `DIARIO.md`).

Patrón canónico para llamadas a la API (replica este flujo en cualquier código nuevo que necesite Claude):

```python
from dotenv import load_dotenv
from anthropic import Anthropic
import os

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=...,
    messages=[{"role": "user", "content": "..."}],
)
text = response.content[0].text
input_tokens = response.usage.input_tokens
output_tokens = response.usage.output_tokens
```

## Convenciones

- **Modelo por defecto:** `claude-sonnet-4-5`. Decisión explícita por balance precio/calidad para tareas de scoring estructurado. No cambies el modelo sin confirmar.
- **Python 3.12** (no 3.13/3.14). Decisión explícita por compatibilidad del ecosistema de librerías. Si el usuario plantea actualizar, recuérdale el motivo antes de proceder.
- **Secretos:** patrón `.env` (real, en `.gitignore`) + `.env.example` (template público sin valores). Toda variable nueva con secreto debe aparecer en ambos sitios. Nunca incluyas el valor real en commits, mensajes ni outputs.
- **`load_dotenv()` + `os.getenv("...")`** es el modo estándar de leer secretos en este repo. No introduzcas `Anthropic()` sin parámetro confiando en `ANTHROPIC_API_KEY` del entorno: el patrón actual lee la key explícitamente.

## DIARIO.md

`DIARIO.md` es un cuaderno de aprendizaje del usuario, no documentación técnica del proyecto. Convenciones a respetar si el usuario pide actualizarlo:

- **Orden cronológico inverso:** la sesión más reciente va arriba (debajo del título y separador inicial), encima de las sesiones más antiguas.
- **Estructura por sesión:** Qué hicimos / Qué aprendí / Decisiones tomadas / Próximos pasos / Estado al cierre / Dudas pendientes.
- **Tono:** primera persona, reflexivo, registra el *porqué* de las decisiones, no solo el *qué*. Cuando dudes del estilo, lee la Sesión 1 como referencia.
- No edites entradas pasadas para "mejorarlas"; son registro histórico. Si algo cambió, escríbelo en la sesión actual.
