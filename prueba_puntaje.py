
from analisis.procesador_resultados import ProcesadorResultados

procesador = ProcesadorResultados()

problemas_prueba = [
    {"impacto": "critical"},
    {"impacto": "serious"},
    {"impacto": "serious"},
    {"impacto": "moderate"},
    {"impacto": "moderate"},
    {"impacto": "moderate"},
    {"impacto": "minor"}
]

puntaje = procesador.calcular_puntaje(problemas_prueba)
clasificacion = procesador.clasificar_puntaje(puntaje)

print("PUNTAJE:", puntaje)
print("CLASIFICACIÓN:", clasificacion)
