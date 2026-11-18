from bdd.repositorios import RepositorioAnalisis
from ia.asistente import AsistenteIA


repositorio = RepositorioAnalisis()
asistente = AsistenteIA()

# 1. Obtener el análisis más reciente
analisis = repositorio.listar_analisis()

if not analisis:
    print("No hay análisis registrados.")
    raise SystemExit

analisis_id = analisis[0][0]

# 2. Obtener sus páginas
paginas = repositorio.obtener_paginas(analisis_id)

if not paginas:
    print("El análisis no tiene páginas.")
    raise SystemExit

pagina_id = paginas[0][0]

# 3. Obtener los problemas detectados
problemas = repositorio.obtener_problemas(pagina_id)

if not problemas:
    print("No se encontraron problemas para analizar con IA.")
    raise SystemExit


# 4. Procesar todos los problemas con IA

for problema in problemas:

    problema_id = problema[0]
    regla_id = problema[2]
    impacto = problema[3]
    descripcion = problema[4]
    ayuda = problema[5]
    elementos = problema[6]

    elemento_html = None

    if elementos:
        elemento_html = elementos[0].get("html", "")

    print("\nAnalizando:", regla_id)

    try:
        resultado_ia = asistente.analizar_problema(
            regla_id,
            impacto,
            descripcion,
            ayuda,
            elemento_html
        )

        repositorio.guardar_recomendacion(
            problema_id,
            resultado_ia
        )

        print("Explicación:", resultado_ia["explicacion"])
        print("Recomendación:", resultado_ia["recomendacion"])
        print("Recomendación guardada correctamente.")

    except Exception as error:
        print("Error al analizar", regla_id, ":", error)

print("\nPROCESAMIENTO DE IA FINALIZADO.")


# Obtener el HTML del primer elemento afectado
elemento_html = None

if elementos:
    elemento_html = elementos[0].get("html", "")

# 4. Enviar el problema a Ollama
resultado_ia = asistente.analizar_problema(
    regla_id,
    impacto,
    descripcion,
    ayuda,
    elemento_html
)

# 5. Guardar la recomendación en SQLite
repositorio.guardar_recomendacion(
    problema_id,
    resultado_ia
)

# 6. Mostrar el resultado
print("\nPROBLEMA ANALIZADO:")
print("Regla:", regla_id)
print("Impacto:", impacto)
print("Descripción:", descripcion)

print("\nRESPUESTA DE LA IA:")
print("Explicación:", resultado_ia["explicacion"])
print("Impacto en usuarios:", resultado_ia["impacto_usuarios"])
print("Recomendación:", resultado_ia["recomendacion"])
print("Código sugerido:", resultado_ia["codigo_sugerido"])

print("\nRecomendación guardada correctamente.")