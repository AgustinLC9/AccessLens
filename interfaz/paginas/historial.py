
from PySide6.QtCore import Signal

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QHBoxLayout,
    QMessageBox,
    QHeaderView
)

from bdd.repositorios import RepositorioAnalisis


class PaginaHistorial(QWidget):

    abrir_informe_solicitado = Signal(int)

    def __init__(self):
        super().__init__()

        self.repositorio = RepositorioAnalisis()

        self.crear_interfaz()
        self.cargar_historial()

    def crear_interfaz(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(45, 40, 45, 40)
        layout.setSpacing(18)

        titulo = QLabel("Historial de análisis")
        titulo.setObjectName("titulo_pagina")

        descripcion = QLabel(
            "Consultá los análisis realizados anteriormente."
        )
        descripcion.setObjectName("descripcion")

        layout.addWidget(titulo)
        layout.addWidget(descripcion)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)

        self.tabla.setHorizontalHeaderLabels([
            "ID",
            "Fecha",
            "Estado",
            "Páginas",
            "Puntaje",
            "Resultado"
        ])

        self.tabla.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.tabla.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.tabla.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )

        self.tabla.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.tabla.doubleClicked.connect(
            self.abrir_informe
        )

        layout.addWidget(self.tabla)

        botones = QHBoxLayout()

        self.boton_actualizar = QPushButton(
            "Actualizar historial"
        )

        self.boton_actualizar.clicked.connect(
            self.cargar_historial
        )

        botones.addWidget(self.boton_actualizar)

        botones.addStretch()

        self.boton_ver_informe = QPushButton(
            "Ver informe"
        )

        self.boton_ver_informe.clicked.connect(
            self.abrir_informe
        )

        botones.addWidget(self.boton_ver_informe)

        layout.addLayout(botones)

    def cargar_historial(self):

        try:

            analisis = self.repositorio.listar_analisis()

            self.tabla.setRowCount(0)

            for registro in analisis:

                fila = self.tabla.rowCount()
                self.tabla.insertRow(fila)

                analisis_id = registro[0]
                fecha = registro[1]
                estado = registro[3]
                total_paginas = registro[4]
                completadas = registro[5]
                fallidas = registro[6]
                puntaje = registro[7]

                estados = {
                    "completado": "Completado",
                    "completado_parcial": "Completado parcialmente",
                    "fallido": "Fallido",
                    "en_ejecucion": "En ejecución",
                    "pendiente": "Pendiente"
                }

                nombre_estado = estados.get(
                    estado,
                    estado
                )

                texto_puntaje = (
                    f"{puntaje}/100"
                    if puntaje is not None
                    else "No disponible"
                )

                valores = [
                    analisis_id,
                    fecha,
                    nombre_estado,
                    f"{completadas}/{total_paginas}",
                    texto_puntaje,
                    f"Fallidas: {fallidas}"
                ]

                for columna, valor in enumerate(valores):

                    elemento = QTableWidgetItem(str(valor))

                    self.tabla.setItem(
                        fila,
                        columna,
                        elemento
                    )

            if not analisis:

                self.tabla.setRowCount(1)

                elemento = QTableWidgetItem(
                    "Todavía no hay análisis registrados."
                )

                self.tabla.setItem(0, 0, elemento)
                self.tabla.setSpan(0, 0, 1, 6)

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo cargar el historial:\n{error}"
            )

    def abrir_informe(self):

        fila = self.tabla.currentRow()

        if fila < 0:
            QMessageBox.information(
                self,
                "Seleccionar análisis",
                "Seleccioná un análisis del historial."
            )
            return

        elemento = self.tabla.item(fila, 0)

        if elemento is None:
            return

        try:
            analisis_id = int(elemento.text())
            self.abrir_informe_solicitado.emit(analisis_id)

        except ValueError:
            return
