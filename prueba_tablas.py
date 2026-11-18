from bdd.conexion import ConexionBD


bd = ConexionBD()
conexion = bd.conectar()

cursor = conexion.cursor()

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    AND name NOT LIKE 'sqlite_%'
""")

tablas = cursor.fetchall()

print("Tablas de AccessLens:")

for tabla in tablas:
    print("-", tabla[0])

conexion.close()