"""
animaciones_manim.py
====================
Escenas de Manim (Community Edition) para la clase guiada de Geometría - Grado 6° (Colombia).
Alineado con los Estándares Básicos de Competencias y DBA del Ministerio de Educación Nacional (MEN).

Contenido de escenas:
1. PlanoCartesianoYPosicion: Sistemas de referencia, coordenadas (x,y) y polígonos 2D.
2. TransformacionesIsometricas: Traslación, Rotación y Reflexión en el plano.
3. LongitudVsArea: Diferenciación visual entre Perímetro (1D) y Área (2D).
4. De2Da3DDesdoblamiento: Red/Desarrollo plano 2D plegándose hacia un sólido 3D (Cubo).

Instrucciones de renderizado:
-----------------------------
Para renderizar en baja calidad (vista rápida):
    manim -pql animaciones_manim.py PlanoCartesianoYPosicion
    manim -pql animaciones_manim.py TransformacionesIsometricas
    manim -pql animaciones_manim.py LongitudVsArea
    manim -pql animaciones_manim.py De2Da3DDesdoblamiento

Para renderizar todas en alta calidad (1080p):
    manim -pqh animaciones_manim.py
"""

from manim import *
import numpy as np

# Configuración global de estilo
config.background_color = "#121824"  # Fondo azul oscuro moderno y de alto contraste
PRIMARY_COLOR = "#00D2FF"           # Cyan brillante
SECONDARY_COLOR = "#FF6B6B"         # Coral / Rojo suave
ACCENT_COLOR = "#FFD166"            # Amarillo dorado
SUCCESS_COLOR = "#06D6A0"           # Verde menta
TEXT_COLOR = "#FFFFFF"


# ==============================================================================
# ESCENA 1: SISTEMAS DE REFERENCIA Y COORDENADAS (Competencia 2, Evidencia 2)
# ==============================================================================
class PlanoCartesianoYPosicion(Scene):
    """
    Demuestra la estructura del plano cartesiano:
    - Ejes X (abscisas) e Y (ordenadas)
    - Origen (0,0)
    - Ubicación de pares ordenados (x, y)
    - Construcción de un polígono 2D a partir de sus vértices
    """
    def construct(self):
        # 1. Título de la escena
        titulo = Text("1. Sistema de Referencia: El Plano Cartesiano", font_size=32, color=PRIMARY_COLOR)
        subtitulo = Text("Ubicación de puntos y figuras 2D mediante coordenadas (x, y)", font_size=20, color=ACCENT_COLOR)
        cabecera = VGroup(titulo, subtitulo).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UL, buff=0.4)
        
        self.play(Write(titulo), run_time=1.0)
        self.play(FadeIn(subtitulo, shift=UP * 0.2), run_time=0.8)
        self.wait(0.5)

        # 2. Construcción de la cuadrícula y ejes
        plano = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            x_length=8.5,
            y_length=5.1,
            background_line_style={"stroke_color": "#2A364F", "stroke_width": 1.5, "stroke_opacity": 0.8},
            axis_config={"stroke_color": "#8D99AE", "stroke_width": 2.5, "include_numbers": True, "font_size": 18}
        ).shift(DOWN * 0.4 + RIGHT * 0.5)

        etiqueta_x = MathTex("X", color=PRIMARY_COLOR, font_size=24).next_to(plano.x_axis.get_end(), RIGHT, buff=0.15)
        etiqueta_y = MathTex("Y", color=PRIMARY_COLOR, font_size=24).next_to(plano.y_axis.get_end(), UP, buff=0.15)

        self.play(Create(plano), Write(etiqueta_x), Write(etiqueta_y), run_time=1.5)

        # 3. Punto origen
        origen_punto = Dot(plano.c2p(0, 0), color=ACCENT_COLOR, radius=0.08)
        origen_texto = Text("Origen (0, 0)", font_size=18, color=ACCENT_COLOR).next_to(origen_punto, DL, buff=0.15)
        self.play(FadeIn(origen_punto, scale=0.5), Write(origen_texto), run_time=0.8)
        self.wait(0.5)

        # 4. Puntos a ubicar: Vértices de un cuadrilátero
        coords = [
            ("A", 2, 2, SECONDARY_COLOR),
            ("B", -3, 1, SUCCESS_COLOR),
            ("C", -2, -2, ACCENT_COLOR),
            ("D", 3, -1, PRIMARY_COLOR)
        ]

        puntos_dots = []
        puntos_labels = []
        lineas_guias = []

        for nombre, x, y, col in coords:
            pos = plano.c2p(x, y)
            dot = Dot(pos, color=col, radius=0.09)
            label = MathTex(f"{nombre}({x}, {y})", font_size=20, color=col).next_to(dot, UR if x>=0 else UL, buff=0.12)
            
            # Líneas de proyección punteadas desde los ejes
            linea_x = DashedLine(plano.c2p(x, 0), pos, color=col, stroke_width=1.5, stroke_opacity=0.7)
            linea_y = DashedLine(plano.c2p(0, y), pos, color=col, stroke_width=1.5, stroke_opacity=0.7)
            guia = VGroup(linea_x, linea_y)

            puntos_dots.append(dot)
            puntos_labels.append(label)
            lineas_guias.append(guia)

        # Animación secuencial de ubicación de puntos con líneas guía
        for dot, label, guia in zip(puntos_dots, puntos_labels, lineas_guias):
            self.play(Create(guia), run_time=0.5)
            self.play(FadeIn(dot, scale=1.5), Write(label), run_time=0.6)
            self.wait(0.3)

        # 5. Unir los vértices para formar el polígono 2D
        vertices_coords = [plano.c2p(x, y) for _, x, y, _ in coords]
        poligono = Polygon(*vertices_coords, color=ACCENT_COLOR, stroke_width=3.5, fill_color=ACCENT_COLOR, fill_opacity=0.25)
        
        texto_figura = Text("Figura 2D formada por 4 vértices", font_size=20, color=ACCENT_COLOR).to_corner(DL, buff=0.5)
        
        self.play(Create(poligono), Write(texto_figura), run_time=1.5)
        self.play(Indicate(poligono, color=PRIMARY_COLOR, scale_factor=1.05))
        self.wait(1.5)


# ==============================================================================
# ESCENA 2: MOVIMIENTOS EN EL PLANO (Competencia 1)
# ==============================================================================
class TransformacionesIsometricas(Scene):
    """
    Muestra los tres movimientos rígidos fundamentales (isometrías):
    1. Traslación (vector desplazamiento)
    2. Rotación (ángulo y centro de giro)
    3. Reflexión (eje de simetría / espejo)
    """
    def construct(self):
        # 1. Título principal
        titulo = Text("2. Movimientos Rígidos en el Plano (Isometrías)", font_size=30, color=PRIMARY_COLOR)
        subtitulo = Text("Conservan la forma y el tamaño exacto de la figura original", font_size=18, color="#A0AABF")
        cabecera = VGroup(titulo, subtitulo).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.35)
        self.play(Write(titulo), FadeIn(subtitulo, shift=UP*0.1), run_time=1.0)

        # Plano base
        plano = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-3.5, 3.5, 1],
            x_length=11.5,
            y_length=5.5,
            background_line_style={"stroke_color": "#1F293D", "stroke_width": 1.2},
            axis_config={"stroke_color": "#5C677D", "stroke_width": 1.8}
        ).shift(DOWN * 0.4)
        self.play(Create(plano), run_time=1.0)

        # Figura inicial: Triángulo asimétrico para apreciar giros y reflejos
        p1 = plano.c2p(-4, -1)
        p2 = plano.c2p(-2, -1)
        p3 = plano.c2p(-2.5, 1)
        triangulo_orig = Polygon(p1, p2, p3, color=PRIMARY_COLOR, fill_color=PRIMARY_COLOR, fill_opacity=0.4, stroke_width=3)
        lbl_orig = Text("Original", font_size=16, color=PRIMARY_COLOR).next_to(triangulo_orig, DOWN, buff=0.15)
        
        self.play(Create(triangulo_orig), Write(lbl_orig), run_time=1.0)
        self.wait(0.5)

        # -------------------------------------------------------------
        # PARTE A: TRASLACIÓN
        # -------------------------------------------------------------
        banner_trans = Text("A) TRASLACIÓN: Desplazamiento por vector v = (3, 1)", font_size=20, color=SUCCESS_COLOR).to_corner(UR, buff=0.4)
        self.play(Write(banner_trans), run_time=0.8)

        # Vector de desplazamiento
        flecha_v = Arrow(plano.c2p(-4, -1), plano.c2p(-1, 0), color=SUCCESS_COLOR, buff=0, stroke_width=3.5, max_tip_length_to_length_ratio=0.2)
        lbl_v = MathTex(r"\vec{v} = (+3, +1)", font_size=18, color=SUCCESS_COLOR).next_to(flecha_v, UP, buff=0.1)

        # Triángulo fantasma para dejar rastro
        triangulo_fantasma_1 = triangulo_orig.copy().set_opacity(0.2).set_stroke(PRIMARY_COLOR, width=1.5)
        
        triangulo_trasladado = triangulo_orig.copy().set_color(SUCCESS_COLOR).set_fill(SUCCESS_COLOR, opacity=0.4)
        
        self.play(Create(flecha_v), Write(lbl_v), FadeIn(triangulo_fantasma_1))
        self.play(
            triangulo_trasladado.animate.shift(plano.c2p(3, 1) - plano.c2p(0, 0)),
            run_time=1.5
        )
        lbl_tras = Text("Trasladada", font_size=16, color=SUCCESS_COLOR).next_to(triangulo_trasladado, DOWN, buff=0.15)
        self.play(Write(lbl_tras), run_time=0.5)
        self.wait(1.0)

        # Limpiar elementos de traslación
        self.play(
            FadeOut(flecha_v), FadeOut(lbl_v), FadeOut(triangulo_trasladado), 
            FadeOut(lbl_tras), FadeOut(triangulo_fantasma_1), FadeOut(banner_trans),
            run_time=0.8
        )

        # -------------------------------------------------------------
        # PARTE B: ROTACIÓN
        # -------------------------------------------------------------
        banner_rot = Text("B) ROTACIÓN: Giro de 90° antihorario con centro en O(0,0)", font_size=20, color=ACCENT_COLOR).to_corner(UR, buff=0.4)
        self.play(Write(banner_rot), run_time=0.8)

        # Centro de rotación
        centro_rot = Dot(plano.c2p(0, 0), color=ACCENT_COLOR, radius=0.09)
        lbl_centro = MathTex(r"O(0,0)", font_size=18, color=ACCENT_COLOR).next_to(centro_rot, DR, buff=0.1)
        self.play(FadeIn(centro_rot), Write(lbl_centro), run_time=0.6)

        # Triángulo fantasma
        triangulo_fantasma_2 = triangulo_orig.copy().set_opacity(0.2).set_stroke(PRIMARY_COLOR, width=1.5)
        self.add(triangulo_fantasma_2)

        # Animación de rotación alrededor del origen
        triangulo_rotado = triangulo_orig.copy().set_color(ACCENT_COLOR).set_fill(ACCENT_COLOR, opacity=0.4)
        
        # Arco de rotación indicativo
        arco = Arc(radius=1.8, start_angle=np.arctan2(-1, -3), angle=PI/2, arc_center=plano.c2p(0,0), color=ACCENT_COLOR)
        lbl_arco = MathTex(r"+90^\circ", font_size=18, color=ACCENT_COLOR).next_to(arco, UR, buff=0.1)

        self.play(
            Rotate(triangulo_rotado, angle=PI/2, about_point=plano.c2p(0, 0)),
            Create(arco),
            Write(lbl_arco),
            run_time=2.0
        )
        lbl_rot = Text("Rotada (90°)", font_size=16, color=ACCENT_COLOR).next_to(triangulo_rotado, UP, buff=0.15)
        self.play(Write(lbl_rot), run_time=0.5)
        self.wait(1.0)

        # Limpiar elementos de rotación
        self.play(
            FadeOut(centro_rot), FadeOut(lbl_centro), FadeOut(triangulo_rotado),
            FadeOut(lbl_rot), FadeOut(arco), FadeOut(lbl_arco),
            FadeOut(triangulo_fantasma_2), FadeOut(banner_rot),
            run_time=0.8
        )

        # -------------------------------------------------------------
        # PARTE C: REFLEXIÓN
        # -------------------------------------------------------------
        banner_ref = Text("C) REFLEXIÓN: Simetría axial respecto al Eje Y (espejo)", font_size=20, color=SECONDARY_COLOR).to_corner(UR, buff=0.4)
        self.play(Write(banner_ref), run_time=0.8)

        # Resaltar eje Y como espejo
        eje_espejo = Line(plano.c2p(0, -3), plano.c2p(0, 3), color=SECONDARY_COLOR, stroke_width=4)
        lbl_espejo = Text("Eje de Simetría (Espejo)", font_size=16, color=SECONDARY_COLOR).next_to(eje_espejo, UP, buff=0.1)
        self.play(Create(eje_espejo), Write(lbl_espejo), run_time=0.8)

        triangulo_fantasma_3 = triangulo_orig.copy().set_opacity(0.2).set_stroke(PRIMARY_COLOR, width=1.5)
        self.add(triangulo_fantasma_3)

        # Crear figura reflejada (x -> -x)
        p1_ref = plano.c2p(4, -1)
        p2_ref = plano.c2p(2, -1)
        p3_ref = plano.c2p(2.5, 1)
        triangulo_reflejado = Polygon(p1_ref, p2_ref, p3_ref, color=SECONDARY_COLOR, fill_color=SECONDARY_COLOR, fill_opacity=0.4, stroke_width=3)
        
        # Líneas de simetría perpendiculares
        linea_sim1 = DashedLine(p1, p1_ref, color=SECONDARY_COLOR, stroke_width=1.5, stroke_opacity=0.7)
        linea_sim2 = DashedLine(p2, p2_ref, color=SECONDARY_COLOR, stroke_width=1.5, stroke_opacity=0.7)
        linea_sim3 = DashedLine(p3, p3_ref, color=SECONDARY_COLOR, stroke_width=1.5, stroke_opacity=0.7)

        self.play(
            Create(linea_sim1), Create(linea_sim2), Create(linea_sim3),
            TransformFromCopy(triangulo_orig, triangulo_reflejado),
            run_time=1.8
        )
        lbl_ref = Text("Reflejada (Invertida)", font_size=16, color=SECONDARY_COLOR).next_to(triangulo_reflejado, DOWN, buff=0.15)
        self.play(Write(lbl_ref), run_time=0.5)
        self.wait(1.5)


# ==============================================================================
# ESCENA 3: ATRIBUTOS MEDIBLES: LONGITUD VS ÁREA (Competencia 1.1 y 2.3)
# ==============================================================================
class LongitudVsArea(Scene):
    """
    Diferencia visual e intuitiva entre:
    - Longitud / Perímetro (1D): Contorno que se desenrolla en una línea continua [metros / cm].
    - Área / Superficie (2D): Espacio interior medido en unidades cuadradas [m² / cm²].
    """
    def construct(self):
        # 1. Título
        titulo = Text("3. Atributos Medibles: Longitud (1D) vs Área (2D)", font_size=30, color=PRIMARY_COLOR)
        subtitulo = Text("Cada magnitud física tiene una dimensión y unidad de medida distinta", font_size=18, color=ACCENT_COLOR)
        cabecera = VGroup(titulo, subtitulo).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UL, buff=0.35)
        self.play(Write(titulo), FadeIn(subtitulo, shift=UP*0.1), run_time=1.0)

        # 2. Rectángulo de ejemplo: 4 cm de ancho x 3 cm de alto
        ancho, alto = 4.0, 3.0
        escala = 0.8  # factor de escala para centrar
        w = ancho * escala
        h = alto * escala

        rect_pos = UP * 0.2 + LEFT * 3.0
        rect = Rectangle(width=w, height=h, color=PRIMARY_COLOR, stroke_width=4).move_to(rect_pos)
        
        lbl_ancho_top = MathTex("4\\text{ m}", font_size=20, color=PRIMARY_COLOR).next_to(rect, UP, buff=0.15)
        lbl_ancho_bot = MathTex("4\\text{ m}", font_size=20, color=PRIMARY_COLOR).next_to(rect, DOWN, buff=0.15)
        lbl_alto_izq = MathTex("3\\text{ m}", font_size=20, color=PRIMARY_COLOR).next_to(rect, LEFT, buff=0.15)
        lbl_alto_der = MathTex("3\\text{ m}", font_size=20, color=PRIMARY_COLOR).next_to(rect, RIGHT, buff=0.15)
        
        etiquetas_lados = VGroup(lbl_ancho_top, lbl_ancho_bot, lbl_alto_izq, lbl_alto_der)

        self.play(Create(rect), Write(etiquetas_lados), run_time=1.2)
        self.wait(0.5)

        # -------------------------------------------------------------
        # FASE 1: PERÍMETRO (LONGITUD - 1 DIMENSIÓN)
        # -------------------------------------------------------------
        titulo_perim = Text("A) PERÍMETRO (Magnitud: Longitud)", font_size=20, color=SUCCESS_COLOR).to_corner(UR, buff=0.4)
        desc_perim = Text("Es la medida del CONTORNO (línea 1D).\nUnidades: mm, cm, m, km", font_size=16, color="#C5D3E8").next_to(titulo_perim, DOWN, aligned_edge=LEFT, buff=0.15)
        
        formula_perim = MathTex(
            r"P = 4\text{ m} + 3\text{ m} + 4\text{ m} + 3\text{ m} = 14\text{ m}",
            font_size=22, color=SUCCESS_COLOR
        ).next_to(desc_perim, DOWN, aligned_edge=LEFT, buff=0.2)

        self.play(Write(titulo_perim), FadeIn(desc_perim), Write(formula_perim), run_time=1.2)

        # Animación de "desenrollar" el contorno en una línea recta
        # 4 segmentos del rectángulo
        top_left = rect.get_corner(UL)
        top_right = rect.get_corner(UR)
        bot_right = rect.get_corner(DR)
        bot_left = rect.get_corner(DL)

        seg1 = Line(top_left, top_right, color=SUCCESS_COLOR, stroke_width=5)
        seg2 = Line(top_right, bot_right, color=SUCCESS_COLOR, stroke_width=5)
        seg3 = Line(bot_right, bot_left, color=SUCCESS_COLOR, stroke_width=5)
        seg4 = Line(bot_left, top_left, color=SUCCESS_COLOR, stroke_width=5)

        self.play(Create(seg1), Create(seg2), Create(seg3), Create(seg4), run_time=0.8)

        # Desplegar en una sola línea horizontal en la parte inferior
        linea_desplegada = Line(LEFT * 5.0, RIGHT * 2.0, color=SUCCESS_COLOR, stroke_width=5).to_edge(DOWN, buff=0.8)
        lbl_linea = MathTex(r"\text{Línea continua de } 14\text{ metros}", font_size=20, color=SUCCESS_COLOR).next_to(linea_desplegada, UP, buff=0.12)

        self.play(
            ReplacementTransform(VGroup(seg1, seg2, seg3, seg4), linea_desplegada),
            Write(lbl_linea),
            run_time=1.5
        )
        self.wait(1.0)

        # -------------------------------------------------------------
        # FASE 2: ÁREA (SUPERFICIE - 2 DIMENSIONES)
        # -------------------------------------------------------------
        titulo_area = Text("B) ÁREA (Magnitud: Superficie)", font_size=20, color=ACCENT_COLOR).next_to(formula_perim, DOWN, aligned_edge=LEFT, buff=0.4)
        desc_area = Text("Es la medida del RELLENO interior (2D).\nUnidades: mm², cm², m², km²", font_size=16, color="#C5D3E8").next_to(titulo_area, DOWN, aligned_edge=LEFT, buff=0.15)
        
        formula_area = MathTex(
            r"A = \text{base} \times \text{altura} = 4\text{ m} \times 3\text{ m} = 12\text{ m}^2",
            font_size=22, color=ACCENT_COLOR
        ).next_to(desc_area, DOWN, aligned_edge=LEFT, buff=0.2)

        self.play(Write(titulo_area), FadeIn(desc_area), Write(formula_area), run_time=1.2)

        # Crear cuadrícula de 12 cuadritos unitarios (1m x 1m = 1m²)
        cuadritos = VGroup()
        dx = w / 4.0
        dy = h / 3.0
        
        for i in range(4):
            for j in range(3):
                x_c = top_left[0] + (i + 0.5) * dx
                y_c = bot_left[1] + (j + 0.5) * dy
                c = Square(side_length=min(dx, dy) * 0.95, fill_color=ACCENT_COLOR, fill_opacity=0.5, stroke_color=ACCENT_COLOR, stroke_width=1.5)
                c.move_to([x_c, y_c, 0])
                cuadritos.add(c)

        # Animación del llenado con cuadritos unitarios
        self.play(
            LaggedStart(*[FadeIn(c, scale=0.3) for c in cuadritos], lag_ratio=0.08),
            run_time=2.0
        )

        # Resaltar 1 cuadrito unitario
        cuadrito_muestra = cuadritos[0].copy().set_color(SECONDARY_COLOR).set_fill(SECONDARY_COLOR, opacity=0.8)
        lbl_cuadrito = MathTex(r"1\text{ m}^2", font_size=16, color=SECONDARY_COLOR).move_to(cuadrito_muestra.get_center())
        
        self.play(Transform(cuadritos[0], cuadrito_muestra), Write(lbl_cuadrito), run_time=0.8)
        self.wait(1.5)


# ==============================================================================
# ESCENA 4: RELACIÓN 2D Y 3D: DESARROLLO PLANO A SÓLIDO (Competencia 2.1)
# ==============================================================================
class De2Da3DDesdoblamiento(ThreeDScene):
    """
    Muestra la relación directa entre figuras 2D y sólidos 3D:
    - Desarrollo plano en cruz (6 cuadrados bidimensionales).
    - Plegado hacia un Cubo tridimensional.
    - Rotación en perspectiva 3D para apreciar caras, aristas y vértices.
    """
    def construct(self):
        # 1. Título inicial (en 2D)
        titulo = Text("4. Relación 2D y 3D: Desarrollo Plano a Sólido", font_size=30, color=PRIMARY_COLOR)
        subtitulo = Text("Una red 2D de 6 caras cuadradas se pliega para formar un Cubo (3D)", font_size=18, color=ACCENT_COLOR)
        cabecera = VGroup(titulo, subtitulo).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.35)
        
        self.add_fixed_in_frame_mobjects(cabecera)
        self.play(Write(titulo), FadeIn(subtitulo, shift=UP*0.1), run_time=1.0)

        # 2. Construcción de la Red 2D del Cubo (Forma de Cruz Latina)
        # Tamaño de arista
        L = 1.6
        
        # 6 caras en 2D con colores temáticos
        colores_caras = [
            PRIMARY_COLOR,   # Base
            SECONDARY_COLOR, # Frontal
            SUCCESS_COLOR,   # Posterior
            ACCENT_COLOR,    # Lateral Izquierda
            "#9B5DE5",       # Lateral Derecha
            "#F15BB5"        # Tapa superior
        ]
        
        nombres_caras = ["Base", "Frente", "Atrás", "Izq", "Der", "Tapa"]

        # Posiciones en cruz 2D relativas al centro
        posiciones_2d = [
            [0, 0, 0],       # 0: Base
            [0, -L, 0],      # 1: Frente (abajo)
            [0, L, 0],       # 2: Atrás (arriba)
            [-L, 0, 0],      # 3: Izquierda
            [L, 0, 0],       # 4: Derecha
            [0, 2*L, 0]      # 5: Tapa (arriba del todo)
        ]

        caras_2d = VGroup()
        for pos, col, nom in zip(posiciones_2d, colores_caras, nombres_caras):
            sq = Square(side_length=L, fill_color=col, fill_opacity=0.6, stroke_color=WHITE, stroke_width=2.5)
            sq.move_to(pos)
            lbl = Text(nom, font_size=14, color=WHITE).move_to(sq.get_center())
            caras_2d.add(VGroup(sq, lbl))

        caras_2d.shift(DOWN * 0.5 + LEFT * 1.5)
        
        banner_2d = Text("Red 2D (Plantilla plana de 6 caras)", font_size=20, color=WHITE).to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(banner_2d)

        self.play(
            LaggedStart(*[FadeIn(c, scale=0.8) for c in caras_2d], lag_ratio=0.15),
            Write(banner_2d),
            run_time=2.0
        )
        self.wait(1.0)

        # 3. Transición a Cámara 3D
        self.play(FadeOut(banner_2d), run_time=0.5)
        
        # Mover la cámara a una vista isométrica 3D
        self.move_camera(phi=65 * DEGREES, theta=-45 * DEGREES, zoom=0.85, run_time=2.0)

        # 4. Construcción del Cubo 3D
        # Definición de las 6 caras orientadas en 3D
        cubo_3d = VGroup()
        
        # Cara 0: Base (z = -L/2)
        c_base = Square(side_length=L, fill_color=colores_caras[0], fill_opacity=0.7, stroke_color=WHITE, stroke_width=2)
        c_base.move_to([0, 0, -L/2])
        
        # Cara 1: Frente (y = -L/2, rotada en X)
        c_frente = Square(side_length=L, fill_color=colores_caras[1], fill_opacity=0.7, stroke_color=WHITE, stroke_width=2)
        c_frente.rotate(PI/2, axis=RIGHT).move_to([0, -L/2, 0])
        
        # Cara 2: Atrás (y = L/2, rotada en X)
        c_atras = Square(side_length=L, fill_color=colores_caras[2], fill_opacity=0.7, stroke_color=WHITE, stroke_width=2)
        c_atras.rotate(PI/2, axis=RIGHT).move_to([0, L/2, 0])
        
        # Cara 3: Izquierda (x = -L/2, rotada en Y)
        c_izq = Square(side_length=L, fill_color=colores_caras[3], fill_opacity=0.7, stroke_color=WHITE, stroke_width=2)
        c_izq.rotate(PI/2, axis=UP).move_to([-L/2, 0, 0])
        
        # Cara 4: Derecha (x = L/2, rotada en Y)
        c_der = Square(side_length=L, fill_color=colores_caras[4], fill_opacity=0.7, stroke_color=WHITE, stroke_width=2)
        c_der.rotate(PI/2, axis=UP).move_to([L/2, 0, 0])
        
        # Cara 5: Tapa (z = L/2)
        c_tapa = Square(side_length=L, fill_color=colores_caras[5], fill_opacity=0.7, stroke_color=WHITE, stroke_width=2)
        c_tapa.move_to([0, 0, L/2])

        cubo_3d.add(c_base, c_frente, c_atras, c_izq, c_der, c_tapa)
        cubo_3d.shift(RIGHT * 1.0)

        banner_3d = Text("Sólido 3D Plegado (Cubo: 6 Caras, 12 Aristas, 8 Vértices)", font_size=20, color=SUCCESS_COLOR).to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(banner_3d)

        # Animación de plegado y transformación
        self.play(
            ReplacementTransform(caras_2d, cubo_3d),
            Write(banner_3d),
            run_time=2.5
        )
        self.wait(0.5)

        # 5. Rotación del Cubo en 3D para apreciar todas sus perspectivas
        self.begin_ambient_camera_rotation(rate=0.4)
        self.wait(3.0)
        self.stop_ambient_camera_rotation()
        self.wait(1.0)
