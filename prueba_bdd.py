from bdd.conexion import ConexionBD


bd = ConexionBD()

conexion = bd.conectar()

print("Conexión con SQLite exitosa.")
print("Base de datos:", bd.ruta_bd)

conexion.close()