
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
        layout.setContentsMargins(45, 40, 45, 40)
        layout.setSpacing(18)

        titulo = QLabel("Bienvenido a AccessLens")
        titulo.setObjectName("titulo_pagina")

        descripcion = QLabel(
            "Analizá la accesibilidad de tus sitios web "
            "y descubrí oportunidades de mejora."
        )
        descripcion.setObjectName("descripcion")

        layout.addWidget(titulo)
        layout.addWidget(descripcion)
        layout.addSpacing(15)

        # Panel de nuevo análisis
        panel = QFrame()
        panel.setObjectName("panel_analisis")

        layout_panel = QVBoxLayout(panel)
        layout_panel.setContentsMargins(25, 25, 25, 25)
        layout_panel.setSpacing(15)

        titulo_panel = QLabel("Nueva auditoría")
        titulo_panel.setObjectName("titulo_panel")

        ayuda = QLabel(
            "Ingresá una o varias direcciones web. "
            "Escribí una URL por línea."
        )
        ayuda.setObjectName("descripcion")

        self.entrada_urls = QPlainTextEdit()
        self.entrada_urls.setObjectName("entrada_urls")
        self.entrada_urls.setPlaceholderText(
            "https://example.com\n"
            "https://www.wikipedia.org"
        )
        self.entrada_urls.setMinimumHeight(140)

        self.boton_analizar = QPushButton("Analizar sitios")
        self.boton_analizar.setObjectName("boton_analizar")
        self.boton_analizar.setCursor(
            Qt.CursorShape.PointingHandCursor
        )
        self.boton_analizar.clicked.connect(
            self.solicitar_analisis
        )

        layout_panel.addWidget(titulo_panel)
        layout_panel.addWidget(ayuda)
        layout_panel.addWidget(self.entrada_urls)
        layout_panel.addWidget(self.boton_analizar)

        layout.addWidget(panel)
        layout.addStretch()

        self.setStyleSheet("""
            #panel_analisis {
                background-color: #211E30;
                border: 1px solid #353044;
                border-radius: 12px;
            }

            #titulo_panel {
                color: #D9CCFF;
                font-size: 19px;
                font-weight: bold;
            }

            #entrada_urls {
                background-color: #171521;
                color: #E5E1EF;
                border: 1px solid #454052;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
            }

            #entrada_urls:focus {
                border: 1px solid #A78BFA;
            }

            #boton_analizar {
                background-color: #A78BFA;
                color: #171521;
                border: none;
                border-radius: 8px;
                padding: 13px;
                font-size: 14px;
                font-weight: bold;
            }

            #boton_analizar:hover {
                background-color: #BCA5FF;
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
