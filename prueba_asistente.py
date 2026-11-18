
from ia.asistente import AsistenteIA


asistente = AsistenteIA()

resultado = asistente.analizar_problema(
    regla_id="button-name",
    impacto="serious",
    descripcion="Los botones deben tener un nombre accesible.",
    ayuda="Asegurarse de que cada botón tenga un nombre accesible.",
    elemento_html='<button><img src="buscar.png"></button>'
)

print("\nEXPLICACIÓN:")
print(resultado["explicacion"])

print("\nIMPACTO EN LOS USUARIOS:")
print(resultado["impacto_usuarios"])

print("\nRECOMENDACIÓN:")
print(resultado["recomendacion"])

print("\nCÓDIGO SUGERIDO:")
print(resultado["codigo_sugerido"])