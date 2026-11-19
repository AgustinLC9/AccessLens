
import time

from analisis.gestor_concurrente import GestorConcurrente


URLS = [
    "https://example.com",
    "https://www.python.org",
    "https://www.wikipedia.org",
    "https://www.w3.org"
]


def ejecutar_secuencial(urls):

    print("\n========== PRUEBA SECUENCIAL ==========")

    gestor = GestorConcurrente()

    resultados = []

    inicio = time.perf_counter()

    for url in urls:
        resultado = gestor.analizar_pagina(url)
        resultados.append(resultado)

    duracion = time.perf_counter() - inicio

    return resultados, duracion


def ejecutar_concurrente(urls):

    print("\n========== PRUEBA CONCURRENTE ==========")

    gestor = GestorConcurrente(max_trabajadores=3)

    inicio = time.perf_counter()

    resultados = gestor.analizar_urls(urls)

    duracion = time.perf_counter() - inicio

    return resultados, duracion


def mostrar_resultados(nombre, resultados, duracion):

    completados = sum(
        1 for r in resultados
        if r["estado"] == "completado"
    )

    fallidos = sum(
        1 for r in resultados
        if r["estado"] == "fallido"
    )

    print(f"\n--- {nombre} ---")
    print(f"Tiempo total: {duracion:.2f} segundos")
    print(f"Páginas completadas: {completados}")
    print(f"Páginas fallidas: {fallidos}")


def main():

    print("======================================")
    print(" COMPARACIÓN DE RENDIMIENTO")
    print(" ACCESSLENS")
    print("======================================")

    print(f"\nCantidad de páginas: {len(URLS)}")

    resultados_secuenciales, tiempo_secuencial = (
        ejecutar_secuencial(URLS)
    )

    resultados_concurrentes, tiempo_concurrente = (
        ejecutar_concurrente(URLS)
    )

    mostrar_resultados(
        "EJECUCIÓN SECUENCIAL",
        resultados_secuenciales,
        tiempo_secuencial
    )

    mostrar_resultados(
        "EJECUCIÓN CONCURRENTE",
        resultados_concurrentes,
        tiempo_concurrente
    )

    print("\n========== COMPARACIÓN ==========")

    if tiempo_secuencial > 0:

        diferencia = tiempo_secuencial - tiempo_concurrente

        porcentaje = (
            diferencia / tiempo_secuencial
        ) * 100

        print(
            f"Tiempo secuencial: {tiempo_secuencial:.2f} segundos"
        )

        print(
            f"Tiempo concurrente: {tiempo_concurrente:.2f} segundos"
        )

        print(
            f"Diferencia: {diferencia:.2f} segundos"
        )

        print(
            f"Variación del tiempo: {porcentaje:.2f}%"
        )

        if diferencia > 0:
            print("La ejecución concurrente fue más rápida.")

        elif diferencia < 0:
            print("La ejecución secuencial fue más rápida.")

        else:
            print("Ambas ejecuciones tardaron lo mismo.")

    print("\n======================================")


if __name__ == "__main__":
    main()
