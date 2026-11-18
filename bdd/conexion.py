import sqlite3
from pathlib import Path


class ConexionBD:

    def __init__(self):
        # Ruta de la carpeta principal del proyecto
        self.ruta_proyecto = Path(__file__).resolve().parent.parent

        # Ubicación del archivo de base de datos
        self.ruta_bd = self.ruta_proyecto / "accesslens.db"

    def conectar(self):
        conexion = sqlite3.connect(
            self.ruta_bd,
            timeout=30
        )
        conexion.execute("PRAGMA foreign_keys = ON")
        return conexion