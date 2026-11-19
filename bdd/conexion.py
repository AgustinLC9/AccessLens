
import sys
import sqlite3
from pathlib import Path


class ConexionBD:

    def __init__(self):

        if getattr(sys, "frozen", False):
            # Cuando se ejecuta como aplicación .exe
            carpeta_base = Path(sys.executable).resolve().parent
        else:
            # Cuando se ejecuta desde Python
            carpeta_base = Path(__file__).resolve().parent.parent

        self.ruta_proyecto = carpeta_base
        self.ruta_bd = self.ruta_proyecto / "accesslens.db"

    def conectar(self):

        conexion = sqlite3.connect(
            self.ruta_bd,
            timeout=30
        )

        conexion.execute("PRAGMA foreign_keys = ON")

        return conexion
