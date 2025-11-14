#!/usr/bin/env python
"""Script de prueba para verificar que el scraper funciona con el buscador público"""

import sys
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv(dotenv_path="../.env")

# Fix para Windows si es necesario
if sys.platform == 'win32':
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from scraper import get_contrataciones

def main():
    print("=" * 80)
    print("PRUEBA DEL SCRAPER DE SEACE")
    print("=" * 80)
    print()

    # Las credenciales no son necesarias para el buscador público
    # pero las pasamos por si acaso
    username = os.getenv("user", "")
    password = os.getenv("pass", "")

    print(f"Usuario configurado: {username}")
    print(f"Iniciando scraping del buscador público...")
    print()

    try:
        contrataciones = get_contrataciones(username, password)

        print("=" * 80)
        print(f"RESULTADOS: {len(contrataciones)} contrataciones encontradas")
        print("=" * 80)
        print()

        for i, c in enumerate(contrataciones, 1):
            print(f"{i}. Código: {c.codigo}")
            print(f"   Descripción: {c.descripcion[:100]}...")
            print(f"   Entidad: {c.entidad}")
            print(f"   Tiempo restante: {c.tiempo_restante_horas:.1f} horas")
            print(f"   Estado: {c.estado_tiempo.upper()}")
            print(f"   URL: {c.url_detalle}")
            print()

        if len(contrataciones) == 0:
            print("⚠️  No se encontraron contrataciones. Esto puede ser normal si:")
            print("   - No hay contrataciones activas en este momento")
            print("   - El buscador público tiene una estructura diferente")
            print("   - Se requiere actualizar los selectores CSS en scraper.py")
        else:
            print("✅ El scraper funciona correctamente!")

    except Exception as e:
        print("❌ ERROR al ejecutar el scraper:")
        print(f"   {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
