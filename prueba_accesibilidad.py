
from analisis.navegador import Navegador


navegador = Navegador()

resultado = navegador.obtener_datos(
    "https://example.com"
)

resultados_axe = resultado["resultados_axe"]

print("PAGINA:", resultado["titulo"])

print("\nPROBLEMAS DETECTADOS:")

for problema in resultados_axe["violations"]:
    print("\nRegla:", problema["id"])
    print("Impacto:", problema["impact"])
    print("Descripcion:", problema["description"])
    print("Ayuda:", problema["help"])
    print("Elementos afectados:", len(problema["nodes"]))

print("\nRESUMEN:")
print("Reglas incumplidas:", len(resultados_axe["violations"]))
print("Reglas aprobadas:", len(resultados_axe["passes"]))
print("Reglas incompletas:", len(resultados_axe["incomplete"]))
