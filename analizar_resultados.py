import json
from collections import Counter

import pandas as pd


def main():
    # Cargar resultados
    with open("resultados.json", "r", encoding="utf-8") as f:
        resultados = json.load(f)

    print(f"\n{'='*70}")
    print(f"ANÁLISIS DE RESULTADOS — {len(resultados)} leads procesados")
    print(f"{'='*70}\n")

    # Filtrar solo los que se procesaron correctamente (sin errores)
    validos = [r for r in resultados if "puntuacion_total" in r and r["puntuacion_total"] is not None]

    # 1. Distribución por categoría
    print("DISTRIBUCIÓN POR CATEGORÍA")
    print("-" * 70)
    categorias = Counter(r["categoria"] for r in validos)
    for cat in ["Encaje claro", "Encaje parcial", "Encaje débil", "No encaje"]:
        n = categorias.get(cat, 0)
        pct = (n / len(validos)) * 100 if validos else 0
        print(f"  {cat:20s}: {n:3d} leads ({pct:.1f}%)")
    print()

    # 2. Distribución por patrón
    print("DISTRIBUCIÓN POR PATRÓN DETECTADO")
    print("-" * 70)
    patrones = Counter(r["patron_detectado"] for r in validos)
    for patron, n in patrones.most_common():
        pct = (n / len(validos)) * 100
        print(f"  {patron:35s}: {n:3d} leads ({pct:.1f}%)")
    print()

    # 3. Top 5 más alta puntuación
    print("TOP 5 LEADS — MAYOR PUNTUACIÓN")
    print("-" * 70)
    ordenados = sorted(validos, key=lambda r: r["puntuacion_total"], reverse=True)
    for r in ordenados[:5]:
        print(f"  [{r['puntuacion_total']:2d}/15] {r.get('empresa', 'N/A'):50s} ({r['patron_detectado']})")
    print()

    # 4. Top 5 más baja puntuación
    print("TOP 5 LEADS — MENOR PUNTUACIÓN")
    print("-" * 70)
    for r in ordenados[-5:]:
        print(f"  [{r['puntuacion_total']:2d}/15] {r.get('empresa', 'N/A'):50s} ({r['patron_detectado']})")
    print()

    # 5. Promedio por dimensión
    print("PROMEDIO POR DIMENSIÓN (sobre 3)")
    print("-" * 70)
    dims = ["encaje_icp", "madurez_problema", "capacidad_decision", "timing", "capacidad_presupuestaria"]
    for dim in dims:
        valores = [r["dimensiones"][dim] for r in validos]
        promedio = sum(valores) / len(valores)
        print(f"  {dim:30s}: {promedio:.2f}")
    print()

    # 6. Anomalías
    print("VERIFICACIÓN DE INTEGRIDAD")
    print("-" * 70)
    sin_patron = [r for r in validos if not r.get("patron_detectado")]
    print(f"  Leads sin patrón detectado: {len(sin_patron)}")

    fuera_rango = [r for r in validos if r["puntuacion_total"] < 0 or r["puntuacion_total"] > 15]
    print(f"  Puntuaciones fuera de rango [0-15]: {len(fuera_rango)}")

    # Verificar coherencia: la suma de dimensiones debe igualar puntuacion_total
    inconsistencias = []
    for r in validos:
        suma_dims = sum(r["dimensiones"].values())
        if suma_dims != r["puntuacion_total"]:
            inconsistencias.append({
                "empresa": r.get("empresa", "N/A"),
                "esperado": suma_dims,
                "reportado": r["puntuacion_total"]
            })
    print(f"  Inconsistencias suma dimensiones vs puntuación: {len(inconsistencias)}")
    if inconsistencias:
        for inc in inconsistencias[:3]:
            print(f"    - {inc['empresa']}: dimensiones suman {inc['esperado']} pero reporta {inc['reportado']}")

    print()


if __name__ == "__main__":
    main()
