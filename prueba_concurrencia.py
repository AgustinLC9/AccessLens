
import time

from analisis.gestor_concurrente import GestorConcurrente


urls = [
    "https://example.com",
    "https://www.wikipedia.org",
    "https://www.python.org"
]

gestor = GestorConcurrente(max_trabajadores=3)

inicio = time.perf_counter()

resultados = gestor.analizar_urls(urls)

duracion_total = time.perf_counter() - inicio

print("\nRESULTADOS DEL ANALISIS")
print("=" * 50)

for resultado in resultados:

    print("\nURL:", resultado["url"])
    print("Estado:", resultado["estado"])
    print("Duración:", resultado["duracion_ms"], "ms")

    if resultado["estado"] == "completado":
        datos = resultado["resultado"]

        print("Título:", datos["titulo"])
        print(
            "Problemas detectados:",
            len(datos["resultados_axe"]["violations"])
        )
    else:
        print("Error:", resultado["error"])

print("\n" + "=" * 50)
print("Tiempo total:", round(duracion_total, 2), "segundos")
print("Páginas procesadas:", len(resultados))
