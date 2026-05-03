"""
Test rápido de conectividad con la API de Anthropic.
Este archivo es solo para verificar que el setup funciona.
Después de validarlo, puede borrarse.
"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Cargar variables del archivo .env
load_dotenv()

# Leer la API key desde la variable de entorno
api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    print("ERROR: No se encontró ANTHROPIC_API_KEY en .env")
    print("Verifica que el archivo .env existe y contiene la key.")
    exit(1)

# Inicializar el cliente
client = Anthropic(api_key=api_key)

# Hacer una llamada simple
print("Llamando a Claude...")
print()

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=100,
    messages=[
        {
            "role": "user",
            "content": "En una sola frase, ¿qué eres?"
        }
    ]
)

# Mostrar la respuesta
print("Respuesta de Claude:")
print(response.content[0].text)
print()
print(f"Modelo usado: {response.model}")
print(f"Tokens entrada: {response.usage.input_tokens}")
print(f"Tokens salida: {response.usage.output_tokens}")