
from threading import Event

from PySide6.QtCore import QThread, Signal

from analisis.servicio_analisis import ServicioAnalisis


class TrabajadorAnalisis(QThread):

    analisis_finalizado = Signal(dict)
    error_ocurrido = Signal(str)
    progreso_actualizado = Signal(str, str)
    progreso_etapa = Signal(str, int)

    def __init__(self, urls):
        super().__init__()

        self.urls = urls
        self.evento_cancelacion = Event()

    def cancelar(self):
        self.evento_cancelacion.set()

    def run(self):
        try:
            servicio = ServicioAnalisis(
                callback_progreso=self.notificar_progreso,
                callback_etapa=self.notificar_etapa,
                evento_cancelacion=self.evento_cancelacion
            )

            resultados = servicio.ejecutar(self.urls)

            self.analisis_finalizado.emit(resultados)

        except Exception as error:
            self.error_ocurrido.emit(str(error))

    def notificar_progreso(self, url, estado):
        self.progreso_actualizado.emit(url, estado)

    def notificar_etapa(self, mensaje, porcentaje):
        self.progreso_etapa.emit(mensaje, porcentaje)

