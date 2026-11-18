
CONOCIMIENTO_REGLAS = {

    "landmark-one-main": {
        "nombre": "Falta de región principal",
        "significado": (
            "El documento debe contener un landmark principal "
            "que identifique el contenido principal de la página."
        ),
        "impacto": (
            "Las personas que utilizan lectores de pantalla "
            "pueden tener dificultades para localizar rápidamente "
            "el contenido principal."
        ),
        "recomendacion": (
            "Incorporar un único elemento <main> que contenga "
            "el contenido principal de la página. No debe utilizarse "
            "para encabezados, menús o contenido secundario."
        ),
        "codigo": (
            "<body>\n"
            "    <header>\n"
            "        <!-- Encabezado del sitio -->\n"
            "    </header>\n\n"
            "    <nav aria-label=\"Navegación principal\">\n"
            "        <!-- Enlaces de navegación -->\n"
            "    </nav>\n\n"
            "    <main>\n"
            "        <h1>Contenido principal</h1>\n"
            "        <!-- Contenido de la página -->\n"
            "    </main>\n\n"
            "    <footer>\n"
            "        <!-- Pie de página -->\n"
            "    </footer>\n"
            "</body>"
        )
    },

    "page-has-heading-one": {
        "nombre": "Falta de encabezado principal",
        "significado": (
            "La página debe tener un encabezado de nivel 1 "
            "que identifique su contenido principal."
        ),
        "impacto": (
            "Los encabezados permiten a las personas con lectores "
            "de pantalla comprender y recorrer la estructura "
            "del contenido."
        ),
        "recomendacion": (
            "Incorporar un encabezado <h1> descriptivo que "
            "represente el tema principal de la página. "
            "Utilizar niveles inferiores para organizar las subsecciones."
        ),
        "codigo": (
            "<main>\n"
            "    <h1>Servicios disponibles</h1>\n\n"
            "    <section>\n"
            "        <h2>Desarrollo web</h2>\n"
            "        <p>Información sobre nuestros servicios.</p>\n"
            "    </section>\n\n"
            "    <section>\n"
            "        <h2>Soporte técnico</h2>\n"
            "        <p>Información sobre asistencia técnica.</p>\n"
            "    </section>\n"
            "</main>"
        )
    },

    "region": {
        "nombre": "Contenido fuera de regiones semánticas",
        "significado": (
            "El contenido de la página debe estar organizado "
            "dentro de regiones o landmarks de accesibilidad "
            "apropiados."
        ),
        "impacto": (
            "Las personas que utilizan lectores de pantalla "
            "pueden tener dificultades para navegar y localizar "
            "distintas secciones del contenido."
        ),
        "recomendacion": (
            "Identificar el contenido señalado por el análisis "
            "y ubicarlo dentro de una región semántica adecuada. "
            "El contenido principal suele pertenecer a <main>, "
            "mientras que la navegación corresponde a <nav>."
        ),
        "codigo": (
            "<body>\n"
            "    <header>\n"
            "        <h1>Mi sitio web</h1>\n"
            "    </header>\n\n"
            "    <nav aria-label=\"Navegación principal\">\n"
            "        <a href=\"/inicio\">Inicio</a>\n"
            "        <a href=\"/contacto\">Contacto</a>\n"
            "    </nav>\n\n"
            "    <main>\n"
            "        <h2>Contenido principal</h2>\n"
            "        <p>Información de la página.</p>\n"
            "    </main>\n\n"
            "    <footer>\n"
            "        <p>Información del sitio.</p>\n"
            "    </footer>\n"
            "</body>"
        )
    },

    "color-contrast": {
        "nombre": "Contraste de colores insuficiente",
        "significado": (
            "El contraste entre el texto y su fondo puede ser "
            "insuficiente para cumplir los requisitos de WCAG."
        ),
        "impacto": (
            "Las personas con dificultades visuales pueden "
            "tener problemas para distinguir el texto."
        ),
        "recomendacion": (
            "Ajustar los colores del texto y del fondo para "
            "alcanzar una relación de contraste de al menos "
            "4.5:1 para texto normal, o 3:1 para texto grande, "
            "según WCAG AA."
        ),
        "codigo": (
            "/* Texto con contraste adecuado sobre fondo blanco */\n"
            ".texto-principal {\n"
            "    color: #595959;\n"
            "    background-color: #FFFFFF;\n"
            "}\n\n"
            "/* Aplicar la clase al contenido */\n"
            "<p class=\"texto-principal\">\n"
            "    Este texto tiene un contraste adecuado.\n"
            "</p>"
        )
    },

    "image-alt": {
        "nombre": "Imagen sin alternativa textual",
        "significado": (
            "Una imagen informativa puede carecer de una "
            "alternativa textual adecuada."
        ),
        "impacto": (
            "Las personas que utilizan lectores de pantalla "
            "pueden no recibir la información transmitida "
            "por la imagen."
        ),
        "recomendacion": (
            "Agregar un atributo alt que describa brevemente "
            "el contenido o la función de las imágenes informativas. "
            "Para imágenes puramente decorativas, utilizar alt vacío."
        ),
        "codigo": (
            "<!-- Imagen informativa -->\n"
            "<img src=\"grafico.jpg\" "
            "alt=\"Gráfico que muestra el crecimiento de ventas\">\n\n"
            "<!-- Imagen decorativa -->\n"
            "<img src=\"decoracion.jpg\" alt=\"\">"
        )
    }
}


def obtener_conocimiento(regla_id):

    return CONOCIMIENTO_REGLAS.get(regla_id)


def obtener_nombre_regla(regla_id):

    conocimiento = obtener_conocimiento(regla_id)

    if conocimiento:
        return conocimiento.get("nombre", regla_id)

    return regla_id
