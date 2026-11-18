
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Event
import time
import traceback

from analisis.navegador import Navegador


class GestorConcurrente:

    def __init__(
        self,
        max_trabajadores=3,
        callback=None,
        evento_cancelacion=None
    ):
        self.max_trabajadores = max_trabajadores
        self.callback = callback
        self.evento_cancelacion = (
            evento_cancelacion or Event()
        )

    def cancelar(self):
        self.evento_cancelacion.set()

    def esta_cancelado(self):
        return self.evento_cancelacion.is_set()

    def notificar_estado(self, url, estado):

        if self.callback:
            try:
                self.callback(url, estado)

            except Exception as error:
                print(
                    f"[ADVERTENCIA] Error al notificar "
                    f"el estado de {url}: {error}",
                    flush=True
                )

    def analizar_pagina(self, url):

        if self.esta_cancelado():
            self.notificar_estado(url, "cancelado")

            return {
                "url": url,
                "estado": "cancelado",
                "resultado": None,
                "duracion_ms": 0,
                "error": None
            }

        print(f"[INICIO] Comenzando análisis: {url}", flush=True)

        self.notificar_estado(url, "analizando")

        inicio = time.perf_counter()

        try:
            navegador = Navegador()
            resultado = navegador.obtener_datos(url)

            duracion_ms = int(
                (time.perf_counter() - inicio) * 1000
            )

            print(f"[FINALIZADO] {url}", flush=True)

            self.notificar_estado(url, "completado")

            return {
                "url": url,
                "estado": "completado",
                "resultado": resultado,
                "duracion_ms": duracion_ms,
                "error": None
            }

        except Exception as error:

            print(f"[ERROR] {url}: {error}", flush=True)

            traceback.print_exc()

            duracion_ms = int(
                (time.perf_counter() - inicio) * 1000
            )

            self.notificar_estado(url, "fallido")

            return {
                "url": url,
                "estado": "fallido",
                "resultado": None,
                "duracion_ms": duracion_ms,
                "error": str(error)
            }

    def analizar_urls(self, urls):

        resultados = []

        with ThreadPoolExecutor(
            max_workers=self.max_trabajadores
        ) as ejecutor:

            tareas = {
                ejecutor.submit(self.analizar_pagina, url): url
                for url in urls
            }

            for tarea in as_completed(tareas):

                resultado = tarea.result()
                resultados.append(resultado)

        return resultados
