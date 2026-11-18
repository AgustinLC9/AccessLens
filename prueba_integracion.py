
import time

from analisis.navegador import Navegador
from analisis.procesador_resultados import ProcesadorResultados
from bdd.repositorios import RepositorioAnalisis


url = "https://example.com"

navegador = Navegador()
procesador = ProcesadorResultados()
repositorio = RepositorioAnalisis()

# 1. Crear un análisis en la base de datos
analisis_id = repositorio.crear_analisis([url])

# Obtener el ID de la página registrada
paginas = repositorio.obtener_paginas(analisis_id)
pagina_id = paginas[0][0]

# 2. Analizar la página
inicio = time.perf_counter()

resultado = navegador.obtener_datos(url)

duracion_ms = int(
    (time.perf_counter() - inicio) * 1000
)

# 3. Procesar resultados de axe-core
resultados_axe = resultado["resultados_axe"]

problemas = procesador.procesar_problemas(
    resultados_axe
)

resumen = procesador.obtener_resumen(
    resultados_axe
)

# 4. Guardar información de la página
repositorio.guardar_pagina(
    pagina_id=pagina_id,
    titulo=resultado["titulo"],
    url_final=resultado["url_final"],
    estado="completado",
    duracion_ms=duracion_ms
)

# 5. Guardar problemas detectados
repositorio.guardar_problemas(
    pagina_id,
    problemas
)

# Mostrar resultados
print("ANALISIS COMPLETADO")
print("ID del análisis:", analisis_id)
print("ID de la página:", pagina_id)
print("Título:", resultado["titulo"])
print("Duración:", duracion_ms, "ms")

print("\nRESUMEN:")
print(resumen)

print("\nResultados guardados correctamente.")
