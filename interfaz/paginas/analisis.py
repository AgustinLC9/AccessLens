
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QProgressBar,
    QListWidget,
    QFrame,
    QScrollArea,
    QPlainTextEdit,
    QPushButton
)

from PySide6.QtCore import Signal, Qt

from ia.conocimiento import obtener_nombre_regla


class PaginaAnalisis(QWidget):

    cancelar_solicitado = Signal()

    def __init__(self, urls):
        super().__init__()

        self.urls = urls
        self.estados_urls = {}

        self.crear_interfaz()

    def crear_interfaz(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(45, 40, 45, 40)
        layout.setSpacing(18)

        titulo = QLabel("Análisis de accesibilidad")
        titulo.setObjectName("titulo_pagina")

        descripcion = QLabel(
            "Estamos evaluando la accesibilidad de los sitios ingresados."
        )
        descripcion.setObjectName("descripcion")

        layout.addWidget(titulo)
        layout.addWidget(descripcion)

        # Panel principal
        panel = QFrame()
        panel.setObjectName("panel")

        layout_panel = QVBoxLayout(panel)
        layout_panel.setContentsMargins(24, 24, 24, 24)
        layout_panel.setSpacing(14)

        subtitulo = QLabel("Sitios analizados")
        subtitulo.setObjectName("subtitulo")

        self.lista_urls = QListWidget()
        self.lista_urls.setObjectName("lista_urls")

        for url in self.urls:
            self.estados_urls[url] = "En espera"
            self.lista_urls.addItem(f"En espera - {url}")

        self.progreso = QProgressBar()
        self.progreso.setObjectName("progreso")
        self.progreso.setRange(0, 100)
        self.progreso.setValue(0)

        self.estado = QLabel("Preparando análisis...")
        self.estado.setObjectName("descripcion")
        self.estado.setWordWrap(True)

        # Resumen general
        self.resumen_general = QPlainTextEdit()
        self.resumen_general.setObjectName("resumen_general")
        self.resumen_general.setPlainText(
            "El resumen general aparecerá al finalizar el análisis."
        )
        self.resumen_general.setReadOnly(True)
        self.resumen_general.setLineWrapMode(
            QPlainTextEdit.LineWrapMode.WidgetWidth
        )
        self.resumen_general.setMinimumHeight(240)
        self.resumen_general.setMaximumHeight(260)
        self.resumen_general.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.resumen_general.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.boton_cancelar = QPushButton("Cancelar análisis")
        self.boton_cancelar.setObjectName("boton_cancelar")
        self.boton_cancelar.setCursor(
            Qt.CursorShape.PointingHandCursor
        )
        self.boton_cancelar.clicked.connect(
            self.solicitar_cancelacion
        )

        layout_panel.addWidget(subtitulo)
        layout_panel.addWidget(self.lista_urls)
        layout_panel.addWidget(self.progreso)
        layout_panel.addWidget(self.estado)
        layout_panel.addWidget(self.resumen_general)
        layout_panel.addWidget(self.boton_cancelar)

        layout.addWidget(panel)

        # Área desplazable para los informes individuales
        self.informes_scroll = QScrollArea()
        self.informes_scroll.setWidgetResizable(True)
        self.informes_scroll.setObjectName("informes_scroll")
        self.informes_scroll.setMinimumHeight(300)

        self.contenedor_informes = QWidget()
        self.contenedor_informes.setObjectName("contenedor_informes")

        self.layout_informes = QVBoxLayout(
            self.contenedor_informes
        )

        self.layout_informes.setSpacing(15)

        self.informes_scroll.setWidget(
            self.contenedor_informes
        )

        self.informes_scroll.hide()

        layout.addWidget(self.informes_scroll, 1)

        self.aplicar_estilos()

    def aplicar_estilos(self):

        self.setStyleSheet("""
            #titulo_pagina {
                color: #E2E8F0;
                font-size: 28px;
                font-weight: bold;
            }

            #descripcion {
                color: #94A3B8;
                font-size: 13px;
                font-weight: normal;
            }

            #panel {
                background-color: #141B24;
                border: 1px solid #263442;
                border-radius: 12px;
            }

            QLabel#subtitulo {
                color: #D5E2EC;
                font-size: 14px;
                font-weight: bold;
            }

            #lista_urls {
                background-color: #0B0F14;
                color: #CBD5E1;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 8px;
                font-size: 12px;
            }

            #lista_urls::item {
                padding: 7px;
                border-radius: 5px;
            }

            #lista_urls::item:selected {
                background-color: #263B4B;
                color: #E2E8F0;
            }

            #progreso {
                background-color: #0B0F14;
                border: none;
                border-radius: 5px;
                height: 10px;
                text-align: center;
            }

            #progreso::chunk {
                background-color: #6D91A8;
                border-radius: 5px;
            }

            QPlainTextEdit#resumen_general {
                background-color: #1C2936;
                color: #D7E2EA;
                border: none;
                border-radius: 8px;
                padding: 14px;
                font-size: 13px;
                font-weight: normal;
            }

            #boton_cancelar {
                background-color: #263B4B;
                color: #C7D7E2;
                border: 1px solid #3D596D;
                border-radius: 8px;
                padding: 11px;
                font-size: 13px;
                font-weight: bold;
            }

            #boton_cancelar:hover {
                background-color: #344F62;
            }

            #boton_cancelar:disabled {
                background-color: #1C2936;
                color: #64748B;
            }

            #informes_scroll {
                background-color: transparent;
                border: none;
            }

            #contenedor_informes {
                background-color: transparent;
            }

            #tarjeta_informe {
                background-color: #141B24;
                border: 1px solid #263442;
                border-radius: 12px;
            }

            #titulo_tarjeta {
                color: #E2E8F0;
                font-size: 19px;
                font-weight: bold;
            }

            #puntaje {
                color: #8EADC1;
                font-size: 14px;
                font-weight: bold;
            }

            QLabel#texto_problema {
                color: #E2E8F0;
                font-size: 13px;
                font-weight: normal;
            }

            QLabel#texto_recomendacion {
                color: #CBD5E1;
                font-size: 13px;
                font-weight: normal;
            }

            #separador {
                background-color: #263442;
                border: none;
                max-height: 1px;
            }

            QPlainTextEdit {
                background-color: #0B0F14;
                color: #D7E2EA;
                border: 1px solid #334155;
                border-radius: 7px;
                padding: 10px;
                font-family: Consolas;
                font-size: 12px;
            }

            QScrollBar:vertical {
                background-color: #0B0F14;
                width: 9px;
                margin: 0;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical {
                background-color: #40596B;
                border-radius: 4px;
                min-height: 25px;
            }

            QScrollBar::handle:vertical:hover {
                background-color: #6D91A8;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0;
            }
        """)

    def solicitar_cancelacion(self):

        self.boton_cancelar.setEnabled(False)
        self.boton_cancelar.setText("Cancelando...")
        self.estado.setText(
            "Solicitando cancelación. Esperando que terminen "
            "las tareas que ya están en ejecución..."
        )

        self.cancelar_solicitado.emit()

    def actualizar_estado(self, url, nuevo_estado):

        nombres_estados = {
            "analizando": "Analizando",
            "completado": "Completado",
            "fallido": "Fallido",
            "cancelado": "Cancelado"
        }

        nombre = nombres_estados.get(
            nuevo_estado,
            nuevo_estado
        )

        self.estados_urls[url] = nombre

        self.lista_urls.clear()

        for direccion in self.urls:

            estado = self.estados_urls[direccion]

            self.lista_urls.addItem(
                f"{estado} - {direccion}"
            )

        finalizadas = sum(
            1 for estado in self.estados_urls.values()
            if estado in (
                "Completado",
                "Fallido",
                "Cancelado"
            )
        )

        porcentaje = int(
            (finalizadas / len(self.urls)) * 60
        )

        self.progreso.setValue(porcentaje)

        analizando = sum(
            1 for estado in self.estados_urls.values()
            if estado == "Analizando"
        )

        pendientes = sum(
            1 for estado in self.estados_urls.values()
            if estado == "En espera"
        )

        self.estado.setText(
            f"Finalizadas: {finalizadas}/{len(self.urls)} | "
            f"Analizando: {analizando} | "
            f"En espera: {pendientes}"
        )

    def mostrar_resultados(self, resultados):

        self.lista_urls.clear()

        paginas = resultados["paginas"]
        resumen = resultados["resumen_general"]

        completadas = 0
        fallidas = 0
        canceladas = 0
        total_problemas = 0

        severidades = {
            "critical": 0,
            "serious": 0,
            "moderate": 0,
            "minor": 0
        }

        # Limpiar informes anteriores
        while self.layout_informes.count():

            elemento = self.layout_informes.takeAt(0)
            widget = elemento.widget()

            if widget:
                widget.deleteLater()

        # Procesar resultados de cada página
        for pagina in paginas:

            url = pagina["url"]

            if pagina["estado"] == "completado":

                puntaje = pagina["puntaje"]
                clasificacion = pagina["clasificacion"]

                texto = (
                    f"Completado - {url} | "
                    f"{puntaje}/100 ({clasificacion})"
                )

                completadas += 1

                problemas = pagina.get("problemas", [])

                total_problemas += len(problemas)

                for problema in problemas:

                    impacto = problema.get(
                        "impacto",
                        "unknown"
                    )

                    if impacto in severidades:
                        severidades[impacto] += 1

                self.crear_informe_pagina(pagina)

            elif pagina["estado"] == "cancelado":

                texto = f"Cancelado - {url}"
                canceladas += 1

            else:

                texto = f"Fallido - {url}"
                fallidas += 1

            self.lista_urls.addItem(texto)

        self.progreso.setValue(100)

        estado_general = resultados.get(
            "estado",
            resumen.get("estado", "desconocido")
        )

        if estado_general == "cancelado":

            self.estado.setText(
                "Análisis cancelado. "
                f"Completadas: {completadas} | "
                f"Fallidas: {fallidas} | "
                f"Canceladas: {canceladas}"
            )

        else:

            self.estado.setText(
                "Análisis finalizado. "
                f"Completadas: {completadas} | "
                f"Fallidas: {fallidas}"
            )

        puntaje_general = resumen.get("puntaje_general")

        if puntaje_general is not None:
            texto_puntaje = f"{puntaje_general}/100"
        else:
            texto_puntaje = "No disponible"

        texto_resumen = (
            f"ID del análisis: {resultados['analisis_id']}\n"
            f"Estado: {estado_general}\n\n"
            f"RESUMEN GENERAL\n"
            f"Total de páginas: {len(paginas)}\n"
            f"Páginas completadas: {completadas}\n"
            f"Páginas fallidas: {fallidas}\n"
            f"Páginas canceladas: {canceladas}\n"
            f"Puntaje general orientativo: {texto_puntaje}\n\n"
            f"PROBLEMAS DETECTADOS\n"
            f"Total: {total_problemas}\n"
            f"Críticos: {severidades['critical']}\n"
            f"Serios: {severidades['serious']}\n"
            f"Moderados: {severidades['moderate']}\n"
            f"Menores: {severidades['minor']}"
        )

        self.resumen_general.setPlainText(texto_resumen)

        self.boton_cancelar.hide()
        self.informes_scroll.show()

    def actualizar_progreso_general(self, mensaje, porcentaje):

        self.progreso.setValue(porcentaje)
        self.estado.setText(mensaje)

    def crear_informe_pagina(self, pagina):

        tarjeta = QFrame()
        tarjeta.setObjectName("tarjeta_informe")

        layout_tarjeta = QVBoxLayout(tarjeta)
        layout_tarjeta.setContentsMargins(20, 20, 20, 20)
        layout_tarjeta.setSpacing(12)

        # Título de la página
        titulo = QLabel(
            pagina["titulo"] or pagina["url"]
        )

        titulo.setObjectName("titulo_tarjeta")
        titulo.setWordWrap(True)

        layout_tarjeta.addWidget(titulo)

        # URL
        url = QLabel(pagina["url"])
        url.setObjectName("descripcion")
        url.setWordWrap(True)

        layout_tarjeta.addWidget(url)

        # Puntaje
        valor_puntaje = pagina.get("puntaje")

        if valor_puntaje is not None:

            texto_puntaje = (
                f"Puntaje: {valor_puntaje}/100 "
                f"({pagina['clasificacion']})"
            )

        else:

            texto_puntaje = "Puntaje: No disponible"

        puntaje = QLabel(texto_puntaje)
        puntaje.setObjectName("puntaje")

        layout_tarjeta.addWidget(puntaje)

        # Resumen de accesibilidad
        resumen = pagina["resumen"]

        texto_resumen = QLabel(
            f"Problemas detectados: "
            f"{resumen.get('total_problemas', 0)}"
        )

        texto_resumen.setObjectName("descripcion")

        layout_tarjeta.addWidget(texto_resumen)

        # Problemas detectados
        problemas = pagina.get("problemas", [])

        orden_severidad = {
            "critical": 0,
            "serious": 1,
            "moderate": 2,
            "minor": 3
        }

        problemas = sorted(
            problemas,
            key=lambda problema: orden_severidad.get(
                problema.get("impacto", "unknown"),
                4
            )
        )

        if not problemas:

            sin_problemas = QLabel(
                "No se detectaron problemas de accesibilidad."
            )

            sin_problemas.setObjectName("descripcion")

            layout_tarjeta.addWidget(sin_problemas)

        else:

            for problema in problemas:

                separador = QFrame()
                separador.setObjectName("separador")
                separador.setFrameShape(QFrame.Shape.HLine)

                layout_tarjeta.addWidget(separador)

                regla = QLabel(
                    obtener_nombre_regla(problema["regla_id"])
                )

                regla.setObjectName("subtitulo")

                layout_tarjeta.addWidget(regla)

                # Indicador de severidad
                impacto = problema.get(
                    "impacto",
                    "unknown"
                )

                severidades = {
                    "critical": ("CRÍTICO", "#EF4444"),
                    "serious": ("SERIO", "#F97316"),
                    "moderate": ("MODERADO", "#EAB308"),
                    "minor": ("MENOR", "#22C55E")
                }

                nombre, color = severidades.get(
                    impacto,
                    ("NO ESPECIFICADO", "#94A3B8")
                )

                etiqueta_severidad = QLabel(nombre)

                etiqueta_severidad.setStyleSheet(
                    f"""
                    QLabel {{
                        background-color: {color};
                        color: #0B0F14;
                        font-size: 12px;
                        font-weight: bold;
                        padding: 5px 10px;
                        border-radius: 6px;
                    }}
                    """
                )

                etiqueta_severidad.setMaximumWidth(160)

                layout_tarjeta.addWidget(etiqueta_severidad)

                descripcion = QLabel(
                    problema["descripcion"]
                )

                descripcion.setTextFormat(
                    Qt.TextFormat.PlainText
                )
                descripcion.setObjectName("texto_problema")
                descripcion.setWordWrap(True)

                layout_tarjeta.addWidget(descripcion)

                recomendacion = problema.get("recomendacion")

                if recomendacion:

                    explicacion = QLabel(
                        "Explicación: "
                        + recomendacion.get("explicacion", "")
                    )

                    explicacion.setTextFormat(
                        Qt.TextFormat.PlainText
                    )
                    explicacion.setObjectName("texto_recomendacion")
                    explicacion.setWordWrap(True)

                    layout_tarjeta.addWidget(explicacion)

                    impacto_usuarios = QLabel(
                        "Impacto para los usuarios: "
                        + recomendacion.get("impacto_usuarios", "")
                    )

                    impacto_usuarios.setTextFormat(
                        Qt.TextFormat.PlainText
                    )
                    impacto_usuarios.setObjectName("texto_recomendacion")
                    impacto_usuarios.setWordWrap(True)

                    layout_tarjeta.addWidget(impacto_usuarios)

                    consejo = QLabel(
                        "Recomendación: "
                        + recomendacion.get("recomendacion", "")
                    )

                    consejo.setTextFormat(
                        Qt.TextFormat.PlainText
                    )
                    consejo.setObjectName("texto_recomendacion")
                    consejo.setWordWrap(True)

                    layout_tarjeta.addWidget(consejo)

                    codigo = recomendacion.get("codigo_sugerido")

                    if codigo:

                        etiqueta_codigo = QLabel(
                            "Código sugerido:"
                        )
                        etiqueta_codigo.setObjectName("subtitulo")

                        layout_tarjeta.addWidget(etiqueta_codigo)

                        visor_codigo = QPlainTextEdit()

                        visor_codigo.setPlainText(str(codigo))
                        visor_codigo.setReadOnly(True)
                        visor_codigo.setMaximumHeight(150)

                        layout_tarjeta.addWidget(visor_codigo)

                else:

                    sin_ia = QLabel(
                        "Recomendación no disponible\n\n"
                        "No se pudo generar la explicación mediante "
                        "inteligencia artificial. Esto puede ocurrir "
                        "si Ollama no está disponible o si ocurrió "
                        "un error durante la generación.\n\n"
                        "Los resultados del análisis de accesibilidad "
                        "siguen disponibles."
                    )

                    sin_ia.setObjectName("descripcion")
                    sin_ia.setWordWrap(True)

                    layout_tarjeta.addWidget(sin_ia)

        self.layout_informes.addWidget(tarjeta)


