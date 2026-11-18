
from bdd.conexion import ConexionBD
from bdd.repositorios import RepositorioAnalisis


bd = ConexionBD()
repositorio = RepositorioAnalisis()

conexion = bd.conectar()
cursor = conexion.cursor()

# Buscar un problema guardado anteriormente
cursor.execute("""
    SELECT id
    FROM problemas
    LIMIT 1
""")

fila = cursor.fetchone()
conexion.close()

if fila is None:
    print("No hay problemas guardados para probar.")
else:
    problema_id = fila[0]

    # Simular una respuesta de Ollama
    resultado = {
        "explicacion": "La imagen no tiene un texto alternativo.",
        "impacto_usuarios": "Las personas que utilizan lectores de pantalla no pueden conocer su contenido.",
        "recomendacion": "Agregar un atributo alt descriptivo a la imagen.",
        "codigo_sugerido": '<img src="logo.png" alt="Logo de la empresa">'
    }

    repositorio.guardar_recomendacion(
        problema_id,
        resultado
    )

    print("Recomendación guardada correctamente.")

    # Comprobar que se guardó
    conexion = bd.conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT explicacion, recomendacion
        FROM recomendaciones
        WHERE problema_id = ?
    """, (problema_id,))

    print(cursor.fetchone())

    conexion.close()
