
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
        self.trabajador = None
        self.cierre_pendiente = False

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

        # Botones del menú
        self.boton_inicio = QPushButton("⌂   Inicio")
        self.boton_analisis = QPushButton("◎   Análisis")
        self.boton_historial = QPushButton("◷   Historial")

        self.boton_inicio.clicked.connect(self.mostrar_inicio)

        self.boton_analisis.clicked.connect(
            lambda: self.mostrar_pagina_temporal("Análisis")
        )

        self.boton_historial.clicked.connect(
            lambda: self.mostrar_pagina_temporal("Historial")
        )

        self.botones = [
            self.boton_inicio,
            self.boton_analisis,
            self.boton_historial
        ]

        for boton in self.botones:
            boton.setObjectName("boton_menu")
            boton.setCheckable(True)
            boton.setCursor(Qt.CursorShape.PointingHandCursor)
            boton.setMinimumHeight(44)
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

    def actualizar_menu_activo(self, boton_activo):

        for boton in self.botones:
            boton.setChecked(boton == boton_activo)

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

        self.actualizar_menu_activo(self.boton_inicio)

    def mostrar_pagina_temporal(self, nombre):

        # Mostrar análisis actual si existe
        if nombre == "Análisis":

            self.actualizar_menu_activo(self.boton_analisis)

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

            self.actualizar_menu_activo(self.boton_historial)

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

    def iniciar_analisis(self, urls):

        self.actualizar_menu_activo(self.boton_analisis)

        pagina = PaginaAnalisis(urls)

        self.paginas["analisis_actual"] = pagina
        self.contenido.addWidget(pagina)
        self.contenido.setCurrentWidget(pagina)

        self.trabajador = TrabajadorAnalisis(urls)

        # Conectar solicitud de cancelación
        pagina.cancelar_solicitado.connect(
            self.trabajador.cancelar
        )

        # Conectar señales del trabajador
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

        self.actualizar_menu_activo(self.boton_historial)

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

    def closeEvent(self, event):

        trabajador = self.trabajador

        # Si hay un análisis ejecutándose
        if trabajador is not None and trabajador.isRunning():

            # Evitar procesar varias solicitudes de cierre
            if self.cierre_pendiente:
                event.ignore()
                return

            respuesta = QMessageBox.question(
                self,
                "Análisis en curso",
                "Hay un análisis en curso.\n\n"
                "¿Querés cancelarlo y cerrar la aplicación?\n\n"
                "AccessLens esperará a que terminen "
                "las tareas que ya están ejecutándose.",
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if respuesta == QMessageBox.StandardButton.Yes:

                self.cierre_pendiente = True

                # Deshabilitar la ventana mientras termina
                self.setEnabled(False)

                # Cerrar automáticamente cuando termine el hilo
                trabajador.finished.connect(self.close)

                # Solicitar cancelación
                trabajador.cancelar()

            event.ignore()
            return

        # Si no hay ningún análisis activo, cerrar normalmente
        event.accept()

    def aplicar_estilos(self):

        self.setStyleSheet("""
            QMainWindow {
                background-color: #0B0F14;
            }

            QWidget {
                color: #E2E8F0;
            }

            #barra_lateral {
                background-color: #080C12;
                border-right: 1px solid #1C2936;
            }

            #titulo_app {
                color: #E2E8F0;
                font-size: 23px;
                font-weight: bold;
            }

            #subtitulo {
                color: #94A3B8;
                font-size: 10px;
                letter-spacing: 2px;
            }

            #boton_menu {
                background-color: transparent;
                color: #94A3B8;
                border: none;
                border-radius: 9px;
                text-align: left;
                padding: 13px;
                font-size: 14px;
            }

            #boton_menu:hover {
                background-color: #1C2936;
                color: #E2E8F0;
            }

            #boton_menu:checked {
                background-color: #1C2936;
                color: #E2E8F0;
                border-left: 3px solid #6D91A8;
                font-weight: bold;
            }

            #contenido {
                background-color: #0B0F14;
            }

            #titulo_pagina {
                color: #E2E8F0;
                font-size: 30px;
                font-weight: bold;
            }

            #descripcion {
                color: #94A3B8;
                font-size: 14px;
            }

            #version {
                color: #64748B;
                font-size: 11px;
            }

            QMessageBox {
                background-color: #141B24;
                color: #E2E8F0;
            }

            QMessageBox QLabel {
                color: #E2E8F0;
            }

            QMessageBox QPushButton {
                background-color: #263B4B;
                color: #E2E8F0;
                border: 1px solid #40596B;
                border-radius: 6px;
                padding: 7px 16px;
                min-width: 70px;
            }

            QMessageBox QPushButton:hover {
                background-color: #344F62;
            }
        """)
