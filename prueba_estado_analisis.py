
from bdd.repositorios import RepositorioAnalisis

repositorio = RepositorioAnalisis()

# Crear un análisis de prueba
urls = [
    "https://example.com",
    "https://www.wikipedia.org",
    "https://www.python.org"
]

analisis_id = repositorio.crear_analisis(urls)

print("Análisis creado:", analisis_id)

# Iniciar el análisis
repositorio.iniciar_analisis(analisis_id)

print("Estado actualizado a en_ejecucion")

# Simular resultados de las tres páginas
paginas = repositorio.obtener_paginas(analisis_id)

repositorio.guardar_pagina(
    pagina_id=paginas[0][0],
    estado="completado"
)

repositorio.guardar_pagina(
    pagina_id=paginas[1][0],
    estado="completado"
)

repositorio.guardar_pagina(
    pagina_id=paginas[2][0],
    estado="fallido",
    error="Error de conexión de prueba"
)

# Finalizar el análisis
resultado = repositorio.finalizar_analisis(analisis_id)

print("\nRESULTADO FINAL:")
print(resultado)

# Consultar el registro guardado
analisis = repositorio.obtener_analisis_completo(analisis_id)

print("\nREGISTRO EN BASE DE DATOS:")
print(analisis["analisis"])
