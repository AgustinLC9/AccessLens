
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from interfaz.paginas.inicio import PaginaInicio
from interfaz.paginas.analisis import PaginaAnalisis
from interfaz.trabajador_analisis import TrabajadorAnalisis
from interfaz.paginas.historial import PaginaHistorial
from bdd.repositorios import RepositorioAnalisis

class VentanaPrincipal(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("AccessLens")
        self.setMinimumSize(1100, 700)
        self.resize(1200, 750)
        self.paginas = {}
        self.crear_interfaz()
        self.aplicar_estilos()

    def crear_interfaz(self):

        contenedor = QWidget()
        self.setCentralWidget(contenedor)

        layout_principal = QHBoxLayout(contenedor)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # Barra lateral
        self.barra_lateral = QWidget()
        self.barra_lateral.setObjectName("barra_lateral")
        self.barra_lateral.setFixedWidth(230)

        layout_lateral = QVBoxLayout(self.barra_lateral)
        layout_lateral.setContentsMargins(20, 25, 20, 20)
        layout_lateral.setSpacing(12)

        titulo = QLabel("◈ AccessLens")
        titulo.setObjectName("titulo_app")
        layout_lateral.addWidget(titulo)

        subtitulo = QLabel("ACCESIBILIDAD WEB")
        subtitulo.setObjectName("subtitulo")
        layout_lateral.addWidget(subtitulo)

        layout_lateral.addSpacing(25)

        self.boton_inicio = QPushButton("⌂   Inicio")
        self.boton_analisis = QPushButton("◎   Análisis")
        self.boton_informes = QPushButton("▤   Informes")
        self.boton_historial = QPushButton("◷   Historial")
        self.boton_configuracion = QPushButton("⚙   Configuración")
        
        self.boton_inicio.clicked.connect(self.mostrar_inicio)

        self.boton_analisis.clicked.connect(
            lambda: self.mostrar_pagina_temporal("Análisis")
        )

        self.boton_informes.clicked.connect(
            lambda: self.mostrar_pagina_temporal("Informes")
        )

        self.boton_historial.clicked.connect(
            lambda: self.mostrar_pagina_temporal("Historial")
        )

        self.boton_configuracion.clicked.connect(
            lambda: self.mostrar_pagina_temporal("Configuración")
        )

        self.botones = [
            self.boton_inicio,
            self.boton_analisis,
            self.boton_informes,
            self.boton_historial,
            self.boton_configuracion
        ]

        for boton in self.botones:
            boton.setObjectName("boton_menu")
            boton.setCursor(Qt.CursorShape.PointingHandCursor)
            layout_lateral.addWidget(boton)

        layout_lateral.addStretch()

        version = QLabel("AccessLens v1.0")
        version.setObjectName("version")
        layout_lateral.addWidget(version)

        # Área de contenido
        self.contenido = QStackedWidget()
        self.contenido.setObjectName("contenido")

        layout_principal.addWidget(self.barra_lateral)
        layout_principal.addWidget(self.contenido)

        self.mostrar_inicio()

    def mostrar_inicio(self):

        if "inicio" not in self.paginas:
            pagina = PaginaInicio()
            pagina.analizar_solicitado.connect(
                self.iniciar_analisis
            )

            self.paginas["inicio"] = pagina
            self.contenido.addWidget(pagina)

        self.contenido.setCurrentWidget(
            self.paginas["inicio"]
        )
        
    
    
    def mostrar_pagina_temporal(self, nombre):

        # Mostrar análisis actual si existe
        if nombre == "Análisis":

            if "analisis_actual" in self.paginas:
                self.contenido.setCurrentWidget(
                    self.paginas["analisis_actual"]
                )
                return

            # Mostrar pantalla inicial de análisis
            if "analisis_vacio" not in self.paginas:

                pagina = QWidget()
                layout = QVBoxLayout(pagina)

                layout.setContentsMargins(45, 40, 45, 40)

                titulo = QLabel("Análisis")
                titulo.setObjectName("titulo_pagina")

                descripcion = QLabel(
                    "Todavía no realizaste ningún análisis. "
                    "Ingresá a Inicio para comenzar uno."
                )
                descripcion.setObjectName("descripcion")

                layout.addWidget(titulo)
                layout.addWidget(descripcion)
                layout.addStretch()

                self.paginas["analisis_vacio"] = pagina
                self.contenido.addWidget(pagina)

            self.contenido.setCurrentWidget(
                self.paginas["analisis_vacio"]
            )
            return

        # Mostrar historial real
        if nombre == "Historial":

            if "historial" not in self.paginas:
                pagina = PaginaHistorial()

                pagina.abrir_informe_solicitado.connect(
                    self.abrir_informe_historico
                )

                self.paginas["historial"] = pagina
                self.contenido.addWidget(pagina)

            else:
                self.paginas["historial"].cargar_historial()

            self.contenido.setCurrentWidget(
                self.paginas["historial"]
            )
            return

        # Otras secciones todavía en desarrollo
        if nombre not in self.paginas:

            pagina = QWidget()
            layout = QVBoxLayout(pagina)

            layout.setContentsMargins(45, 40, 45, 40)

            titulo = QLabel(nombre)
            titulo.setObjectName("titulo_pagina")

            descripcion = QLabel(
                "Esta sección se encuentra en desarrollo."
            )
            descripcion.setObjectName("descripcion")

            layout.addWidget(titulo)
            layout.addWidget(descripcion)
            layout.addStretch()

            self.paginas[nombre] = pagina
            self.contenido.addWidget(pagina)

        self.contenido.setCurrentWidget(
            self.paginas[nombre]
        )


        
    
    def iniciar_analisis(self, urls):

        pagina = PaginaAnalisis(urls)

        self.paginas["analisis_actual"] = pagina
        self.contenido.addWidget(pagina)
        self.contenido.setCurrentWidget(pagina)

        self.trabajador = TrabajadorAnalisis(urls)

        self.trabajador.progreso_actualizado.connect(
            pagina.actualizar_estado
        )

        self.trabajador.analisis_finalizado.connect(
            self.finalizar_analisis
        )

        self.trabajador.error_ocurrido.connect(
            self.error_analisis
        )
        
        self.trabajador.progreso_etapa.connect(
            pagina.actualizar_progreso_general
        )

        self.trabajador.start()

        
    def finalizar_analisis(self, resultados):

        pagina = self.paginas["analisis_actual"]

        pagina.mostrar_resultados(resultados)


    def error_analisis(self, mensaje):

        pagina = self.paginas["analisis_actual"]

        pagina.estado.setText(
            f"Error durante el análisis: {mensaje}"
        )
        
    
    def abrir_informe_historico(self, analisis_id):

        try:
            repositorio = RepositorioAnalisis()

            datos = repositorio.obtener_analisis_completo(
                analisis_id
            )

            if datos is None:
                QMessageBox.warning(
                    self,
                    "Informe no encontrado",
                    "No se encontró el análisis seleccionado."
                )
                return

            # Datos generales del análisis
            analisis = datos["analisis"]

            resumen_general = {
                "estado": analisis[3],
                "total_paginas": analisis[4],
                "paginas_completadas": analisis[5],
                "paginas_fallidas": analisis[6],
                "puntaje_general": analisis[7]
            }

            paginas_resultado = []
            urls = []

            for pagina_guardada in datos["paginas"]:

                pagina = pagina_guardada["datos"]

                url = pagina[2]
                urls.append(url)

                problemas_resultado = []

                for problema_guardado in pagina_guardada["problemas"]:

                    problema = problema_guardado["datos"]
                    recomendacion = problema_guardado["recomendacion"]

                    datos_recomendacion = None

                    if recomendacion is not None:
                        datos_recomendacion = {
                            "explicacion": recomendacion[2],
                            "impacto_usuarios": recomendacion[3],
                            "recomendacion": recomendacion[4],
                            "codigo_sugerido": recomendacion[5]
                        }

                    problemas_resultado.append({
                        "regla_id": problema[2],
                        "impacto": problema[3],
                        "descripcion": problema[4],
                        "ayuda": problema[5],
                        "elementos_afectados": problema[6],
                        "recomendacion": datos_recomendacion
                    })

                puntaje = pagina[6]

                if puntaje is not None:
                    if puntaje >= 90:
                        clasificacion = "Excelente"
                    elif puntaje >= 75:
                        clasificacion = "Buena"
                    elif puntaje >= 50:
                        clasificacion = "Moderada"
                    elif puntaje >= 25:
                        clasificacion = "Baja"
                    else:
                        clasificacion = "Muy baja"
                else:
                    clasificacion = "No disponible"

                paginas_resultado.append({
                    "url": url,
                    "titulo": pagina[3],
                    "url_final": pagina[4],
                    "estado": pagina[5],
                    "puntaje": puntaje,
                    "clasificacion": clasificacion,
                    "error": pagina[7],
                    "resumen": {
                        "total_problemas": len(problemas_resultado)
                    },
                    "problemas": problemas_resultado
                })

            resultados = {
                "analisis_id": analisis_id,
                "resumen_general": resumen_general,
                "paginas": paginas_resultado
            }

            # Crear la pantalla del informe histórico
            clave = f"informe_historico_{analisis_id}"

            if clave not in self.paginas:

                pagina_informe = PaginaAnalisis(urls)

                pagina_informe.mostrar_resultados(resultados)

                self.paginas[clave] = pagina_informe
                self.contenido.addWidget(pagina_informe)

            self.contenido.setCurrentWidget(
                self.paginas[clave]
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo abrir el informe histórico:\n{error}"
            )


    def aplicar_estilos(self):

        self.setStyleSheet("""
            QMainWindow {
                background-color: #171521;
            }

            #barra_lateral {
                background-color: #11101A;
            }

            #titulo_app {
                color: #D9CCFF;
                font-size: 23px;
                font-weight: bold;
            }

            #subtitulo {
                color: #85818F;
                font-size: 10px;
                letter-spacing: 2px;
            }

            #boton_menu {
                background-color: transparent;
                color: #B8B4C5;
                border: none;
                border-radius: 8px;
                text-align: left;
                padding: 13px;
                font-size: 14px;
            }

            #boton_menu:hover {
                background-color: #211E30;
                color: #D9CCFF;
            }

            #contenido {
                background-color: #171521;
            }

            #titulo_pagina {
                color: #D9CCFF;
                font-size: 30px;
                font-weight: bold;
            }

            #descripcion {
                color: #A5A1B2;
                font-size: 14px;
            }

            #version {
                color: #666273;
                font-size: 11px;
            }
        """)
