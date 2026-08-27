#!/usr/bin/env python3
"""
generar_videos.py
=================
Script automatizado para renderizar las 4 escenas de Manim en archivos de video MP4
listos para proyectar en el aula de clase de Grado 6°.

Uso:
    python3 generar_videos.py [--calidad l|m|h]
    
Opciones de calidad:
    - l : Baja calidad (480p, renderizado ultrarrápido)
    - m : Calidad media (720p, ideal para proyector de aula) [Por defecto]
    - h : Alta definición (1080p, calidad máxima de presentación)
"""

import sys
import subprocess
import os

ESCENAS = [
    "PlanoCartesianoYPosicion",
    "TransformacionesIsometricas",
    "LongitudVsArea",
    "De2Da3DDesdoblamiento"
]

def main():
    calidad_flag = "-qm"  # Calidad media por defecto
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["-ql", "--low", "l"]:
            calidad_flag = "-ql"
        elif arg in ["-qh", "--high", "h"]:
            calidad_flag = "-qh"

    print("=" * 70)
    print("🎬 Renderizador de Animaciones Manim - Geometría Grado 6° (Colombia)")
    print(f"Calidad seleccionada: {calidad_flag}")
    print("=" * 70)

    for i, escena in enumerate(ESCENAS, 1):
        print(f"\n[{i}/{len(ESCENAS)}] Renderizando escena: {escena}...")
        cmd = ["manim", calidad_flag, "--flush_cache", "animaciones_manim.py", escena]
        try:
            res = subprocess.run(cmd, check=True)
            print(f"✅ Escena {escena} generada exitosamente.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error al renderizar {escena}: {e}")
        except FileNotFoundError:
            print("⚠️ Manim no está instalado en el PATH. Instálalo con: pip install manim")
            sys.exit(1)

    print("\n" + "=" * 70)
    print("✨ ¡Todas las animaciones han sido procesadas!")
    print("Los videos se encuentran en la carpeta: media/videos/animaciones_manim/")
    print("=" * 70)

if __name__ == "__main__":
    main()
