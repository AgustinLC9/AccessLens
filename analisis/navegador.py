
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


class Navegador:

    def __init__(self):

        if getattr(sys, "frozen", False):
            carpeta_base = Path(sys._MEIPASS)
        else:
            carpeta_base = Path(__file__).resolve().parent.parent

        self.ruta_axe = (
            carpeta_base
            / "recursos"
            / "axe.min.js"
        )

    def obtener_datos(self, url):

        with sync_playwright() as playwright:

            navegador = playwright.chromium.launch(
                headless=True
            )

            try:
                pagina = navegador.new_page()

                respuesta = pagina.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=30000
                )

                titulo = pagina.title()
                url_final = pagina.url

                contenido = pagina.locator("body").inner_text(
                    timeout=10000
                )

                codigo_http = (
                    respuesta.status
                    if respuesta is not None
                    else None
                )

                codigo_axe = self.ruta_axe.read_text(
                    encoding="utf-8"
                )

                pagina.add_script_tag(
                    content=codigo_axe
                )

                resultados_axe = pagina.evaluate("""
                    async () => {
                        return await axe.run(document);
                    }
                """)

                return {
                    "titulo": titulo,
                    "url_final": url_final,
                    "contenido": contenido,
                    "codigo_http": codigo_http,
                    "resultados_axe": resultados_axe
                }

            finally:
                navegador.close()

