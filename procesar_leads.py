"""
Procesa todos los leads de leads.csv con el scoring de Claude.
Guarda los resultados en resultados.json (estructura anidada) y resultados.csv (aplanado).
"""

import json
import os
import time

import pandas as pd
from anthropic import Anthropic
from dotenv import load_dotenv
from tqdm import tqdm

from scoring import evaluar_lead

# Precios Sonnet 4.5 (USD por millón de tokens)
PRECIO_INPUT_POR_MILLON = 3.0
PRECIO_OUTPUT_POR_MILLON = 15.0

RUTA_JSON = "resultados.json"
RUTA_CSV = "resultados.csv"

DIMENSIONES = [
    "encaje_icp",
    "madurez_problema",
    "capacidad_decision",
    "timing",
    "capacidad_presupuestaria",
]


def aplanar_para_csv(item: dict) -> dict:
    """Convierte un item de resultados (anidado o de error) en una fila plana para el CSV."""
    fila = {
        "empresa": item.get("empresa"),
        "puntuacion_total": item.get("puntuacion_total"),
        "categoria": item.get("categoria"),
    }
    dimensiones = item.get("dimensiones", {}) or {}
    for dim in DIMENSIONES:
        fila[dim] = dimensiones.get(dim)
    fila["patron_detectado"] = item.get("patron_detectado")
    fila["razonamiento_breve"] = item.get("razonamiento_breve")
    fila["error"] = item.get("error")
    return fila


def main():
    load_dotenv()
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    df = pd.read_csv("leads.csv")
    print(f"Procesando {len(df)} leads...")

    resultados = []
    input_tokens_total = 0
    output_tokens_total = 0
    tiempo_inicio = time.time()

    for _, row in tqdm(df.iterrows(), total=len(df), desc="Scoring"):
        lead = row.to_dict()
        empresa = lead["empresa"]

        resultado, in_t, out_t = evaluar_lead(client, lead)
        input_tokens_total += in_t
        output_tokens_total += out_t

        if resultado is not None:
            resultados.append({"empresa": empresa, **resultado})
        else:
            resultados.append({
                "empresa": empresa,
                "error": "JSON no parseable",
                "puntuacion_total": None,
            })

    tiempo_total = time.time() - tiempo_inicio

    # Resumen
    n_errores = sum(1 for r in resultados if "error" in r)
    coste_input = input_tokens_total / 1_000_000 * PRECIO_INPUT_POR_MILLON
    coste_output = output_tokens_total / 1_000_000 * PRECIO_OUTPUT_POR_MILLON
    coste_total = coste_input + coste_output

    print()
    print("=" * 70)
    print("RESUMEN")
    print("=" * 70)
    print(f"Leads procesados : {len(resultados)} / {len(df)}")
    print(f"Errores parseo   : {n_errores}")
    print(f"Tokens entrada   : {input_tokens_total:,}")
    print(f"Tokens salida    : {output_tokens_total:,}")
    print(f"Coste estimado   : ${coste_total:.4f} USD "
          f"(input ${coste_input:.4f} + output ${coste_output:.4f})")
    print(f"Tiempo total     : {tiempo_total:.1f}s "
          f"(media {tiempo_total / len(df):.2f}s/lead)")

    # Guardar JSON (estructura original anidada)
    with open(RUTA_JSON, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    print(f"\nGuardado: {RUTA_JSON}")

    # Guardar CSV (aplanado, una columna por dimensión)
    filas_planas = [aplanar_para_csv(r) for r in resultados]
    pd.DataFrame(filas_planas).to_csv(RUTA_CSV, index=False, encoding="utf-8")
    print(f"Guardado: {RUTA_CSV}")


if __name__ == "__main__":
    main()
