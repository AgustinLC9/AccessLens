
from analisis.gestor_concurrente import GestorConcurrente
from analisis.procesador_resultados import ProcesadorResultados
from bdd.repositorios import RepositorioAnalisis
from ia.asistente import AsistenteIA


urls = [
    "https://example.com",
    "https://www.wikipedia.org",
    "https://dominio-que-no-existe-123456789.invalid"
]

# Inicializar componentes
repositorio = RepositorioAnalisis()
gestor = GestorConcurrente(max_trabajadores=3)
procesador = ProcesadorResultados()
asistente = AsistenteIA()


# 1. Crear análisis en SQLite
analisis_id = repositorio.crear_analisis(urls)
repositorio.iniciar_analisis(analisis_id)

paginas = repositorio.obtener_paginas(analisis_id)

paginas_por_url = {
    pagina[2]: pagina[0]
    for pagina in paginas
}

print("ANÁLISIS CREADO:", analisis_id)
print("Iniciando análisis concurrente...\n")


# 2. Analizar las páginas concurrentemente
resultados = gestor.analizar_urls(urls)


# 3. Procesar y guardar los resultados
for resultado in resultados:

    url = resultado["url"]
    pagina_id = paginas_por_url[url]

    print("\n" + "=" * 50)
    print("PROCESANDO:", url)

    if resultado["estado"] == "completado":

        datos = resultado["resultado"]
        resultados_axe = datos["resultados_axe"]

        # Procesar problemas y resumen
        problemas = procesador.procesar_problemas(resultados_axe)
        resumen = procesador.obtener_resumen(resultados_axe)

        # Calcular puntaje
        puntaje_resultado = procesador.obtener_puntaje_resultados(
            resultados_axe
        )

        puntaje = puntaje_resultado["puntaje"]
        clasificacion = puntaje_resultado["clasificacion"]

        # Diagnóstico del cálculo
        print("\nDIAGNÓSTICO DEL PUNTAJE:")
        print("Resultado completo:", puntaje_resultado)
        print("Puntaje que se va a guardar:", puntaje)

        # Guardar página
        repositorio.guardar_pagina(
            pagina_id=pagina_id,
            titulo=datos["titulo"],
            url_final=datos["url_final"],
            estado="completado",
            puntaje=puntaje,
            duracion_ms=resultado["duracion_ms"]
        )

        # Guardar problemas
        repositorio.guardar_problemas(pagina_id, problemas)

        print("\nRESULTADOS:")
        print("Estado: completado")
        print("Título:", datos["titulo"])
        print("Duración:", resultado["duracion_ms"], "ms")
        print("Problemas detectados:", resumen["total_problemas"])
        print("Puntaje:", puntaje, "/ 100")
        print("Clasificación:", clasificacion)

        # Recuperar problemas guardados
        problemas_guardados = repositorio.obtener_problemas(pagina_id)

        # Generar y guardar recomendaciones con IA
        for problema in problemas_guardados:

            problema_id = problema[0]
            regla_id = problema[2]
            impacto = problema[3]
            descripcion = problema[4]
            ayuda = problema[5]
            elementos = problema[6]
            
            # Recuperar información adicional del resultado original de axe-core
            problema_original = next(
                (
                    p for p in problemas
                    if p["regla_id"] == regla_id
                ),
                {}
            )

            elemento_html = None
            elemento_selector = None
            resumen_fallo = None

            if elementos:
                elemento_html = elementos[0].get("html", "")
                elemento_selector = elementos[0].get("selector", [])
                resumen_fallo = elementos[0].get("resumen", "")

            print("\nGenerando recomendación:", regla_id)

            try:
                recomendacion = asistente.analizar_problema(
                    regla_id=regla_id,
                    impacto=impacto,
                    descripcion=descripcion,
                    ayuda=ayuda,
                    elemento_html=elemento_html,
                    elemento_selector=elemento_selector,
                    resumen_fallo=resumen_fallo,
                    etiquetas_wcag=problema_original.get("etiquetas_wcag", []),
                    url_ayuda=problema_original.get("url_ayuda", "")
                )

                repositorio.guardar_recomendacion(
                    problema_id,
                    recomendacion
                )

                print("Explicación:", recomendacion["explicacion"])
                print("Recomendación:", recomendacion["recomendacion"])
                print("Recomendación guardada correctamente.")

            except Exception as error:
                print("Error al generar recomendación:", error)

    else:

        # Guardar página fallida
        repositorio.guardar_pagina(
            pagina_id=pagina_id,
            estado="fallido",
            error=resultado["error"],
            duracion_ms=resultado["duracion_ms"]
        )


# 4. Finalizar análisis y calcular puntaje general
resumen_final = repositorio.finalizar_analisis(analisis_id)


# 5. Mostrar resumen general
print("\n" + "=" * 50)
print("RESUMEN FINAL")

print("ID del análisis:", analisis_id)
print("Estado:", resumen_final["estado"])
print("Total de páginas:", resumen_final["total_paginas"])
print("Páginas completadas:", resumen_final["paginas_completadas"])
print("Páginas fallidas:", resumen_final["paginas_fallidas"])
print("Puntaje general:", resumen_final["puntaje_general"])


# 6. Verificar que los datos quedaron guardados en SQLite
analisis_guardado = repositorio.obtener_analisis_completo(analisis_id)

print("\nVERIFICACIÓN DE BASE DE DATOS")

print(
    "Puntaje general guardado:",
    analisis_guardado["analisis"][7]
)

paginas_guardadas = repositorio.obtener_paginas(analisis_id)

print("\nPUNTAJES INDIVIDUALES:")

for pagina in paginas_guardadas:
    print(
        "URL:", pagina[2],
        "| Estado:", pagina[5],
        "| Puntaje:", pagina[6]
    )

print("\nResultados guardados en SQLite.")
