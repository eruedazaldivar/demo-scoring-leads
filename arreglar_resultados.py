"""
Script auxiliar: recalcula puntuacion_total y categoria desde las dimensiones.

Razón: los LLMs son probabilísticos también en matemática simple (~4% error en sumas).
Patrón profesional: lo determinista se calcula determinista, no se delega a IA.

Lee resultados.json, recalcula campos derivados, sobrescribe.
También actualiza resultados.csv para consistencia entre formatos.

Uso:
    python arreglar_resultados.py
"""

import json
import pandas as pd


def categoria_desde_puntuacion(puntuacion: int) -> str:
    """Devuelve la categoría según los umbrales definidos en el prompt."""
    if puntuacion >= 13:
        return "Encaje claro"
    elif puntuacion >= 9:
        return "Encaje parcial"
    elif puntuacion >= 5:
        return "Encaje débil"
    else:
        return "No encaje"


def main():
    # Cargar resultados actuales
    with open("resultados.json", "r", encoding="utf-8") as f:
        leads = json.load(f)

    inconsistencias_corregidas = 0
    cambios_categoria = 0

    for lead in leads:
        if not lead.get("dimensiones"):
            continue

        suma_real = sum(lead["dimensiones"].values())
        puntuacion_reportada = lead.get("puntuacion_total")
        categoria_reportada = lead.get("categoria")
        categoria_real = categoria_desde_puntuacion(suma_real)

        if suma_real != puntuacion_reportada:
            inconsistencias_corregidas += 1
            print(f"  [FIX] {lead.get('empresa', '?'):50s}: "
                  f"puntuacion {puntuacion_reportada} → {suma_real}", end="")

            if categoria_reportada != categoria_real:
                cambios_categoria += 1
                print(f"  | categoria '{categoria_reportada}' → '{categoria_real}'")
            else:
                print()

            lead["puntuacion_total"] = suma_real
            lead["categoria"] = categoria_real

    # Sobrescribir resultados.json
    with open("resultados.json", "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)

    # Sobrescribir resultados.csv
    df = pd.DataFrame(leads)
    df.to_csv("resultados.csv", index=False, encoding="utf-8")

    print()
    print("=" * 70)
    print("RESUMEN")
    print("=" * 70)
    print(f"Leads totales            : {len(leads)}")
    print(f"Inconsistencias corregidas: {inconsistencias_corregidas}")
    print(f"Cambios de categoría     : {cambios_categoria}")
    print(f"Guardado: resultados.json")
    print(f"Guardado: resultados.csv")


if __name__ == "__main__":
    main()