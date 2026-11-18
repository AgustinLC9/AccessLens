
from analisis.navegador import Navegador
from analisis.procesador_resultados import ProcesadorResultados


navegador = Navegador()
procesador = ProcesadorResultados()

# Analizar una página
resultado = navegador.obtener_datos(
    "https://example.com"
)

resultados_axe = resultado["resultados_axe"]

# Procesar problemas
problemas = procesador.procesar_problemas(
    resultados_axe
)

# Obtener resumen
resumen = procesador.obtener_resumen(
    resultados_axe
)

print("RESUMEN:")
print(resumen)

print("\nPROBLEMAS PROCESADOS:")

for problema in problemas:
    print("\nRegla:", problema["regla_id"])
    print("Impacto:", problema["impacto"])
    print("Descripción:", problema["descripcion"])

    for elemento in problema["elementos_afectados"]:
        print("Selector:", elemento["selector"])
        print("HTML:", elemento["html"])
