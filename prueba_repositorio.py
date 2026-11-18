
from bdd.repositorios import RepositorioAnalisis


repositorio = RepositorioAnalisis()

# Crear un análisis de prueba
analisis_id = repositorio.crear_analisis([
    "https://example.com"
])

# Obtener el ID de la página
conexion = repositorio.bd.conectar()

cursor = conexion.cursor()

cursor.execute("""
    SELECT id
    FROM paginas
    WHERE analisis_id = ?
""", (analisis_id,))

pagina_id = cursor.fetchone()[0]

conexion.close()

# Guardar información de la página
repositorio.guardar_pagina(
    pagina_id=pagina_id,
    titulo="Página de ejemplo",
    url_final="https://example.com",
    estado="completado",
    puntaje=85,
    duracion_ms=3200
)

# Simular problemas detectados por axe-core
problemas = [
    {
        "regla_id": "image-alt",
        "impacto": "critical",
        "descripcion": "Las imágenes deben tener texto alternativo.",
        "ayuda": "Agregar un atributo alt descriptivo.",
        "elementos_afectados": [
            {
                "selector": "img.logo",
                "html": '<img class="logo" src="logo.png">'
            }
        ]
    },
    {
        "regla_id": "button-name",
        "impacto": "serious",
        "descripcion": "Los botones deben tener un nombre accesible.",
        "ayuda": "Agregar un nombre accesible al botón.",
        "elementos_afectados": [
            {
                "selector": "button.buscar",
                "html": '<button class="buscar"></button>'
            }
        ]
    }
]

repositorio.guardar_problemas(
    pagina_id,
    problemas
)

print("Página y problemas guardados correctamente.")
