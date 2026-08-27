# Geometría Grado 6° - Secuencia Didáctica con Quarto y Manim

Material interactivo de geometría y medición para grado 6° de educación básica secundaria en Colombia. Está estructurado según los Estándares Básicos de Competencias (EBC) y los Derechos Básicos de Aprendizaje (DBA 5 y 6) del Ministerio de Educación Nacional (MEN).

---

## Estructura del Contenido

| Competencia (MEN) | Evidencia de Aprendizaje | Módulo |
|---|---|---|
| **1. Reconocimiento de características medibles, posición y movimientos rígidos** | Señala atributos medibles de una figura junto con sus posibles unidades y magnitudes. | Módulo 3: Longitud (1D) vs Área (2D) |
| **2. Reconocimiento de objetos geométricos y métricos** | Identifica relaciones entre figuras 2D y 3D. | Módulo 4: Redes planas y sólidos 3D |
| | Utiliza sistemas de referencia para representar la ubicación de objetos. | Módulo 1: Plano cartesiano y coordenadas $(x, y)$ |
| | Reconoce el conjunto de unidades usadas para longitud y área. | Módulo 2 y 3: Transformaciones y unidades métricas |

---

## Cómo Ejecutar el Proyecto

### Método Principal: Quarto (Recomendado)

Este proyecto está diseñado para ejecutarse y visualizarse como un documento interactivo con [Quarto](https://quarto.org).

#### 1. Requisitos
- **Quarto CLI**: Descargar e instalar desde [quarto.org/docs/get-started](https://quarto.org/docs/get-started/).
- **Python 3.9+** con Manim:
  ```bash
  pip install manim
  ```

#### 2. Visualización Interactiva
Para abrir la lección interactiva en el navegador con recarga automática:
```bash
quarto preview clase_geometria_grado6.qmd
```

#### 3. Renderizar a HTML estático
Para generar un archivo HTML autocontenido para compartir:
```bash
quarto render clase_geometria_grado6.qmd --to html
```

---

## Métodos Alternativos

### Google Colab
Si prefieres no instalar herramientas locales:
1. Abre [Google Colab](https://colab.research.google.com).
2. Sube el archivo `clase_geometria_grado6.ipynb`.
3. Ejecuta las celdas en orden. La primera celda instala Manim en el entorno de Colab.

### Videos para Aulas sin Conexión (Offline)
Para generar los 4 videos MP4 de las animaciones y usarlos desde una memoria USB:
```bash
python3 generar_videos.py
```
Los archivos `.mp4` se guardarán en `media/videos/animaciones_manim/`.

---

## Descripción de Archivos

- `clase_geometria_grado6.qmd`: Documento maestro en Quarto con teoría, animaciones embebidas, retos interactivos y rúbrica de evaluación.
- `clase_geometria_grado6.ipynb`: Cuaderno Jupyter equivalente para Colab o JupyterLab.
- `animaciones_manim.py`: Código fuente de las 4 escenas animadas en Manim.
- `GUIA_DOCENTE.md`: Plan de aula detallado para 4 sesiones de 50 minutos, soluciones a los retos y criterios de evaluación según el Decreto 1290.
- `generar_videos.py`: Script para renderizar las animaciones a video MP4 por lotes.
