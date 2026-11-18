
from analisis.procesador_resultados import ProcesadorResultados

procesador = ProcesadorResultados()

# Puntajes obtenidos en el análisis
puntajes = [94, 100, 58]

puntaje_general = procesador.calcular_puntaje_general(
    puntajes
)

clasificacion = procesador.clasificar_puntaje(
    puntaje_general
)

print("PUNTAJE GENERAL:", puntaje_general)
print("CLASIFICACIÓN:", clasificacion)

print(
    "Sin páginas:",
    procesador.calcular_puntaje_general([])
)