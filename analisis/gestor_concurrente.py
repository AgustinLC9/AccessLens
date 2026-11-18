
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import traceback
from analisis.navegador import Navegador


class GestorConcurrente:

    def __init__(self, max_trabajadores=3, callback=None):
        self.max_trabajadores = max_trabajadores
        self.callback = callback

    def analizar_pagina(self, url):

        print(f"[INICIO] Comenzando análisis: {url}", flush=True)

        if self.callback:
            self.callback(url, "analizando")

        inicio = time.perf_counter()

        try:
            navegador = Navegador()
            resultado = navegador.obtener_datos(url)

            duracion_ms = int(
                (time.perf_counter() - inicio) * 1000
            )

            print(f"[FINALIZADO] {url}", flush=True)

            if self.callback:
                self.callback(url, "completado")

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

            if self.callback:
                self.callback(url, "fallido")

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
