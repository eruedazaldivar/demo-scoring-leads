"""
Test del prompt de scoring sobre 3 leads representativos.
Sirve para iterar el prompt antes de procesar el CSV completo.
"""

import json
import os

import pandas as pd
from anthropic import Anthropic
from dotenv import load_dotenv

from scoring import evaluar_lead

INDICES_PRUEBA = [0, 2, 17]


def main():
    load_dotenv()
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    df = pd.read_csv("leads.csv")

    for idx in INDICES_PRUEBA:
        lead = df.iloc[idx].to_dict()
        print("=" * 70)
        print(f"Lead #{idx} — {lead['empresa']} ({lead['contacto_rol']})")
        print("=" * 70)

        resultado, input_tokens, output_tokens = evaluar_lead(client, lead)
        print(f"  Tokens: {input_tokens} entrada / {output_tokens} salida")
        if resultado is not None:
            print(json.dumps(resultado, indent=2, ensure_ascii=False))
        print()


if __name__ == "__main__":
    main()
