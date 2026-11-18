
import sys

from PySide6.QtWidgets import QApplication
from interfaz.ventana_principal import VentanaPrincipal


def main():

    aplicacion = QApplication(sys.argv)

    ventana = VentanaPrincipal()
    ventana.show()

    sys.exit(aplicacion.exec())


if __name__ == "__main__":
    main()
