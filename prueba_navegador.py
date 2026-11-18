
from analisis.navegador import Navegador


navegador = Navegador()

resultado = navegador.obtener_datos(
    "https://example.com"
)

print("TITULO:")
print(resultado["titulo"])

print("\nURL FINAL:")
print(resultado["url_final"])

print("\nCODIGO HTTP:")
print(resultado["codigo_http"])

print("\nCONTENIDO:")
print(resultado["contenido"])
