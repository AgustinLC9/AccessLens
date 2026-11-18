
from threading import Lock

from analisis.gestor_concurrente import GestorConcurrente
from analisis.procesador_resultados import ProcesadorResultados

from bdd.repositorios import RepositorioAnalisis
from ia.asistente import AsistenteIA


class ServicioAnalisis:

    def __init__(
        self,
        callback_progreso=None,
        callback_etapa=None,
        evento_cancelacion=None
    ):

        self.repositorio = RepositorioAnalisis()
        self.procesador = ProcesadorResultados()
        self.asistente = AsistenteIA()

        self.callback_progreso = callback_progreso
        self.callback_etapa = callback_etapa
        self.evento_cancelacion = evento_cancelacion

        self.paginas_finalizadas = 0
        self.total_paginas = 0
        self.bloqueo_progreso = Lock()

    def esta_cancelado(self):

        return (
            self.evento_cancelacion is not None
            and self.evento_cancelacion.is_set()
        )

    def notificar(self, url, estado):

        if self.callback_progreso:
            self.callback_progreso(url, estado)

        if estado in ("completado", "fallido"):

            with self.bloqueo_progreso:

                self.paginas_finalizadas += 1

                porcentaje = int(
                    (self.paginas_finalizadas / self.total_paginas) * 60
                )

            if self.callback_etapa:
                self.callback_etapa(
                    "Analizando páginas",
                    porcentaje
                )

    def informar_etapa(self, mensaje, porcentaje):

        if self.callback_etapa:
            self.callback_etapa(mensaje, porcentaje)

    def ejecutar(self, urls):

        analisis_id = None

        try:

            self.total_paginas = len(urls)
            self.paginas_finalizadas = 0

            self.informar_etapa(
                "Analizando páginas",
                0
            )

            # 1. Crear análisis en SQLite

            analisis_id = self.repositorio.crear_analisis(urls)

            self.repositorio.iniciar_analisis(analisis_id)

            paginas = self.repositorio.obtener_paginas(analisis_id)

            paginas_por_url = {
                pagina[2]: pagina[0]
                for pagina in paginas
            }

            # 2. Ejecutar análisis concurrente

            gestor = GestorConcurrente(
                max_trabajadores=3,
                callback=self.notificar,
                evento_cancelacion=self.evento_cancelacion
            )

            resultados = gestor.analizar_urls(urls)

            registros_paginas = []
            total_recomendaciones = 0

            # 3. Procesar y guardar resultados

            self.informar_etapa(
                "Procesando resultados y guardando en SQLite",
                60
            )

            for indice, resultado in enumerate(resultados):

                url = resultado["url"]
                pagina_id = paginas_por_url[url]

                if resultado["estado"] == "completado":

                    datos = resultado["resultado"]

                    resultados_axe = datos["resultados_axe"]

                    problemas = self.procesador.procesar_problemas(
                        resultados_axe
                    )

                    resumen = self.procesador.obtener_resumen(
                        resultados_axe
                    )

                    puntaje_resultado = (
                        self.procesador.obtener_puntaje_resultados(
                            resultados_axe
                        )
                    )

                    puntaje = puntaje_resultado["puntaje"]
                    clasificacion = puntaje_resultado["clasificacion"]

                    self.repositorio.guardar_pagina(
                        pagina_id=pagina_id,
                        titulo=datos["titulo"],
                        url_final=datos["url_final"],
                        estado="completado",
                        puntaje=puntaje,
                        duracion_ms=resultado["duracion_ms"]
                    )

                    self.repositorio.guardar_problemas(
                        pagina_id,
                        problemas
                    )

                    problemas_guardados = (
                        self.repositorio.obtener_problemas(pagina_id)
                    )

                    total_recomendaciones += len(problemas_guardados)

                    registros_paginas.append({
                        "url": url,
                        "estado": "completado",
                        "datos": datos,
                        "duracion_ms": resultado["duracion_ms"],
                        "puntaje": puntaje,
                        "clasificacion": clasificacion,
                        "resumen": resumen,
                        "problemas": problemas,
                        "problemas_guardados": problemas_guardados,
                        "problemas_resultados": []
                    })

                elif resultado["estado"] == "fallido":

                    self.repositorio.guardar_pagina(
                        pagina_id=pagina_id,
                        estado="fallido",
                        error=resultado["error"],
                        duracion_ms=resultado["duracion_ms"]
                    )

                    registros_paginas.append({
                        "url": url,
                        "estado": "fallido",
                        "duracion_ms": resultado["duracion_ms"],
                        "error": resultado["error"]
                    })

                else:

                    self.repositorio.guardar_pagina(
                        pagina_id=pagina_id,
                        estado="cancelado",
                        error="Análisis cancelado por el usuario",
                        duracion_ms=resultado["duracion_ms"]
                    )

                    registros_paginas.append({
                        "url": url,
                        "estado": "cancelado",
                        "duracion_ms": resultado["duracion_ms"],
                        "error": "Análisis cancelado por el usuario"
                    })

                porcentaje = 60 + int(
                    ((indice + 1) / len(resultados)) * 15
                )

                self.informar_etapa(
                    "Procesando resultados y guardando en SQLite",
                    porcentaje
                )

            # 4. Generar recomendaciones con IA

            recomendaciones_generadas = 0
            ia_disponible = True

            if self.esta_cancelado():

                self.informar_etapa(
                    "Cancelando análisis",
                    95
                )

            else:

                self.informar_etapa(
                    "Generando recomendaciones con IA",
                    75
                )

                if total_recomendaciones == 0:

                    self.informar_etapa(
                        "No hay recomendaciones pendientes",
                        95
                    )

                for registro in registros_paginas:

                    if self.esta_cancelado():
                        break

                    if registro["estado"] != "completado":
                        continue

                    problemas_guardados = registro["problemas_guardados"]

                    for problema in problemas_guardados:

                        if self.esta_cancelado():
                            break

                        problema_id = problema[0]
                        regla_id = problema[2]
                        impacto = problema[3]
                        descripcion = problema[4]
                        ayuda = problema[5]
                        elementos = problema[6]

                        problema_original = next(
                            (
                                p for p in registro["problemas"]
                                if p["regla_id"] == regla_id
                            ),
                            {}
                        )

                        elemento_html = None
                        elemento_selector = None
                        resumen_fallo = None

                        if elementos:

                            elemento_html = elementos[0].get(
                                "html",
                                ""
                            )

                            elemento_selector = elementos[0].get(
                                "selector",
                                []
                            )

                            resumen_fallo = elementos[0].get(
                                "resumen",
                                ""
                            )

                        recomendacion = None

                        if ia_disponible:

                            try:

                                recomendacion = (
                                    self.asistente.analizar_problema(
                                        regla_id=regla_id,
                                        impacto=impacto,
                                        descripcion=descripcion,
                                        ayuda=ayuda,
                                        elemento_html=elemento_html,
                                        elemento_selector=elemento_selector,
                                        resumen_fallo=resumen_fallo,
                                        etiquetas_wcag=problema_original.get(
                                            "etiquetas_wcag",
                                            []
                                        ),
                                        url_ayuda=problema_original.get(
                                            "url_ayuda",
                                            ""
                                        )
                                    )
                                )

                                self.repositorio.guardar_recomendacion(
                                    problema_id,
                                    recomendacion
                                )

                            except Exception as error:

                                ia_disponible = False

                                print(
                                    f"[IA] Ollama no disponible o falló: {error}"
                                )

                                print(
                                    "[IA] Se omitirán las recomendaciones "
                                    "restantes de este análisis."
                                )

                        registro["problemas_resultados"].append({
                            "regla_id": regla_id,
                            "impacto": impacto,
                            "descripcion": descripcion,
                            "ayuda": ayuda,
                            "elementos": elementos,
                            "recomendacion": recomendacion
                        })

                        recomendaciones_generadas += 1

                        if total_recomendaciones > 0:

                            porcentaje = 75 + int(
                                (
                                    recomendaciones_generadas
                                    / total_recomendaciones
                                ) * 20
                            )

                            self.informar_etapa(
                                "Generando recomendaciones con IA",
                                porcentaje
                            )

            # 5. Preparar resultados finales

            resultados_completos = []

            for registro in registros_paginas:

                if registro["estado"] == "fallido":

                    resultados_completos.append({
                        "url": registro["url"],
                        "estado": "fallido",
                        "titulo": None,
                        "url_final": None,
                        "duracion_ms": registro["duracion_ms"],
                        "puntaje": None,
                        "clasificacion": None,
                        "resumen": None,
                        "problemas": [],
                        "error": registro["error"]
                    })

                elif registro["estado"] == "cancelado":

                    resultados_completos.append({
                        "url": registro["url"],
                        "estado": "cancelado",
                        "titulo": None,
                        "url_final": None,
                        "duracion_ms": registro["duracion_ms"],
                        "puntaje": None,
                        "clasificacion": None,
                        "resumen": None,
                        "problemas": [],
                        "error": registro["error"]
                    })

                else:

                    datos = registro["datos"]

                    resultados_completos.append({
                        "url": registro["url"],
                        "estado": "completado",
                        "titulo": datos["titulo"],
                        "url_final": datos["url_final"],
                        "duracion_ms": registro["duracion_ms"],
                        "puntaje": registro["puntaje"],
                        "clasificacion": registro["clasificacion"],
                        "resumen": registro["resumen"],
                        "problemas": registro["problemas_resultados"],
                        "error": None
                    })

            # 6. Finalizar análisis

            if self.esta_cancelado():

                self.repositorio.marcar_analisis_cancelado(
                    analisis_id
                )

                estado_final = "cancelado"

                self.informar_etapa(
                    "Análisis cancelado",
                    100
                )

            else:

                resumen_final = self.repositorio.finalizar_analisis(
                    analisis_id
                )

                estado_final = resumen_final["estado"]

                self.informar_etapa(
                    "Análisis finalizado",
                    100
                )

            return {
                "analisis_id": analisis_id,
                "estado": estado_final,
                "resumen_general": (
                    resumen_final
                    if not self.esta_cancelado()
                    else {
                        "estado": "cancelado",
                        "total_paginas": len(urls),
                        "paginas_completadas": sum(
                            1 for r in registros_paginas
                            if r["estado"] == "completado"
                        ),
                        "paginas_fallidas": sum(
                            1 for r in registros_paginas
                            if r["estado"] == "fallido"
                        )
                    }
                ),
                "paginas": resultados_completos
            }

        except Exception as error:

            if analisis_id is not None:

                try:

                    if self.esta_cancelado():

                        self.repositorio.marcar_analisis_cancelado(
                            analisis_id
                        )

                    else:

                        self.repositorio.marcar_analisis_fallido(
                            analisis_id,
                            str(error)
                        )

                except Exception as error_cierre:

                    print(
                        f"[ERROR] No se pudo cerrar el análisis: "
                        f"{error_cierre}"
                    )

            raise
