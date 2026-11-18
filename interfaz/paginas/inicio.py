
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QPlainTextEdit,
    QFrame
)
from PySide6.QtCore import Qt, Signal


class PaginaInicio(QWidget):

    analizar_solicitado = Signal(list)

    def __init__(self):
        super().__init__()

        self.crear_interfaz()

    def crear_interfaz(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 45, 50, 40)
        layout.setSpacing(18)

        # Encabezado
        titulo = QLabel("Bienvenido a AccessLens")
        titulo.setObjectName("titulo_pagina")

        descripcion = QLabel(
            "Analizá la accesibilidad de tus sitios web "
            "y descubrí oportunidades de mejora."
        )
        descripcion.setObjectName("descripcion")

        layout.addWidget(titulo)
        layout.addWidget(descripcion)
        layout.addSpacing(18)

        # Panel de nueva auditoría
        panel = QFrame()
        panel.setObjectName("panel_analisis")

        layout_panel = QVBoxLayout(panel)
        layout_panel.setContentsMargins(28, 28, 28, 28)
        layout_panel.setSpacing(16)

        titulo_panel = QLabel("Nueva auditoría")
        titulo_panel.setObjectName("titulo_panel")

        ayuda = QLabel(
            "Ingresá una o varias direcciones web. "
            "Escribí una URL por línea."
        )
        ayuda.setObjectName("descripcion_panel")

        self.entrada_urls = QPlainTextEdit()
        self.entrada_urls.setObjectName("entrada_urls")
        self.entrada_urls.setPlaceholderText(
            "https://example.com\n"
            "https://www.wikipedia.org"
        )
        self.entrada_urls.setMinimumHeight(160)

        self.boton_analizar = QPushButton("◎   Analizar sitios")
        self.boton_analizar.setObjectName("boton_analizar")
        self.boton_analizar.setCursor(
            Qt.CursorShape.PointingHandCursor
        )
        self.boton_analizar.setMinimumHeight(48)

        self.boton_analizar.clicked.connect(
            self.solicitar_analisis
        )

        layout_panel.addWidget(titulo_panel)
        layout_panel.addWidget(ayuda)
        layout_panel.addSpacing(5)
        layout_panel.addWidget(self.entrada_urls)
        layout_panel.addSpacing(5)
        layout_panel.addWidget(self.boton_analizar)

        layout.addWidget(panel)
        layout.addStretch()

        # Estilos: negro y celeste grisáceo
        self.setStyleSheet("""
            #titulo_pagina {
                color: #E2E8F0;
                font-size: 30px;
                font-weight: bold;
            }

            #descripcion {
                color: #94A3B8;
                font-size: 14px;
            }

            #panel_analisis {
                background-color: #141B24;
                border: 1px solid #263442;
                border-radius: 14px;
            }

            #titulo_panel {
                color: #E2E8F0;
                font-size: 20px;
                font-weight: bold;
            }

            #descripcion_panel {
                color: #94A3B8;
                font-size: 13px;
            }

            #entrada_urls {
                background-color: #0B0F14;
                color: #E2E8F0;
                border: 1px solid #334155;
                border-radius: 9px;
                padding: 13px;
                font-size: 14px;
                selection-background-color: #6D91A8;
            }

            #entrada_urls:focus {
                border: 1px solid #6D91A8;
            }

            #boton_analizar {
                background-color: #6D91A8;
                color: #0B0F14;
                border: none;
                border-radius: 9px;
                padding: 13px;
                font-size: 14px;
                font-weight: bold;
            }

            #boton_analizar:hover {
                background-color: #8EADC1;
            }

            #boton_analizar:pressed {
                background-color: #52758C;
            }
        """)

    def solicitar_analisis(self):

        urls = [
            url.strip()
            for url in self.entrada_urls.toPlainText().splitlines()
            if url.strip()
        ]

        if urls:
            self.analizar_solicitado.emit(urls)
