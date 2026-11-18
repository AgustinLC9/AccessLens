
from analisis.procesador_resultados import ProcesadorResultados

procesador = ProcesadorResultados()

# Simular una respuesta de axe-core
resultados_axe = {
    "violations": [
        {
            "id": "color-contrast",
            "impact": "serious",
            "description": "El contraste entre texto y fondo es insuficiente."
        },
        {
            "id": "image-alt",
            "impact": "critical",
            "description": "Una imagen no tiene texto alternativo."
        },
        {
            "id": "landmark-one-main",
            "impact": "moderate",
            "description": "Falta el landmark principal."
        },
        {
            "id": "region",
            "impact": "moderate",
            "description": "Contenido fuera de regiones."
        },
        {
            "id": "heading-order",
            "impact": "minor",
            "description": "La jerarquía de encabezados presenta problemas."
        }
    ],
    "passes": [],
    "incomplete": [],
    "inapplicable": []
}

# Obtener puntaje directamente desde resultados axe-core
resultado = procesador.obtener_puntaje_resultados(
    resultados_axe
)

print("RESULTADO DEL PUNTAJE:")
print(resultado)
