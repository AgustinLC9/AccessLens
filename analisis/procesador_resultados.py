
class ProcesadorResultados:

    def procesar_problemas(self, resultados_axe):

        problemas = []

        for violacion in resultados_axe.get("violations", []):

            elementos = []

            for nodo in violacion.get("nodes", []):

                elementos.append({
                    "selector": nodo.get("target", []),
                    "html": nodo.get("html", ""),
                    "resumen": nodo.get("failureSummary", "")
                })

            problema = {
                "regla_id": violacion.get("id"),
                "impacto": violacion.get("impact", "moderate"),
                "descripcion": violacion.get("description", ""),
                "ayuda": violacion.get("help", ""),
                "url_ayuda": violacion.get("helpUrl", ""),
                "etiquetas_wcag": violacion.get("tags", []),
                "elementos_afectados": elementos
            }

            problemas.append(problema)

        return problemas

    def obtener_resumen(self, resultados_axe):

        return {
            "total_problemas": len(
                resultados_axe.get("violations", [])
            ),
            "reglas_aprobadas": len(
                resultados_axe.get("passes", [])
            ),
            "reglas_incompletas": len(
                resultados_axe.get("incomplete", [])
            ),
            "reglas_no_aplicables": len(
                resultados_axe.get("inapplicable", [])
            )
        }

    def calcular_puntaje(self, problemas):

        penalizaciones = {
            "critical": 10,
            "serious": 5,
            "moderate": 2,
            "minor": 1
        }

        puntaje = 100

        for problema in problemas:

            impacto = problema.get("impacto", "").lower()
            descuento = penalizaciones.get(impacto, 0)

            puntaje -= descuento

        return max(0, min(100, puntaje))

    def clasificar_puntaje(self, puntaje):

        if puntaje >= 90:
            return "Excelente"

        elif puntaje >= 75:
            return "Buena"

        elif puntaje >= 50:
            return "Moderada"

        elif puntaje >= 25:
            return "Baja"

        else:
            return "Muy baja"

    def obtener_puntaje_resultados(self, resultados_axe):

        problemas = self.procesar_problemas(resultados_axe)

        puntaje = self.calcular_puntaje(problemas)
        clasificacion = self.clasificar_puntaje(puntaje)

        return {
            "puntaje": puntaje,
            "clasificacion": clasificacion,
            "total_problemas": len(problemas)
        }

    def calcular_puntaje_general(self, puntajes):

        if not puntajes:
            return None

        promedio = sum(puntajes) / len(puntajes)

        return round(promedio)
