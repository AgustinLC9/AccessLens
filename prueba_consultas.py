
from bdd.repositorios import RepositorioAnalisis


repositorio = RepositorioAnalisis()

# Mostrar historial
print("HISTORIAL DE ANALISIS")

analisis_lista = repositorio.listar_analisis()

for analisis in analisis_lista:
    print(analisis)

if analisis_lista:
    analisis_id = analisis_lista[0][0]

    # Recuperar análisis completo
    resultado = repositorio.obtener_analisis_completo(
        analisis_id
    )

    print("\nANALISIS COMPLETO")
    print(resultado)

    # Probar recuperación de páginas
    print("\nPAGINAS")
    for pagina in repositorio.obtener_paginas(analisis_id):
        print(pagina)
