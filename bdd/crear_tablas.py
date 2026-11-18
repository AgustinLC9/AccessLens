from bdd.conexion import ConexionBD


def crear_tablas():
    bd = ConexionBD()
    conexion = bd.conectar()

    cursor = conexion.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS analisis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_inicio TEXT NOT NULL,
            fecha_fin TEXT,
            estado TEXT NOT NULL DEFAULT 'pendiente',
            total_paginas INTEGER NOT NULL DEFAULT 0,
            paginas_completadas INTEGER NOT NULL DEFAULT 0,
            paginas_fallidas INTEGER NOT NULL DEFAULT 0,
            puntaje_general REAL
        );

        CREATE TABLE IF NOT EXISTS paginas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            analisis_id INTEGER NOT NULL,
            url TEXT NOT NULL,
            titulo TEXT,
            url_final TEXT,
            estado TEXT NOT NULL DEFAULT 'pendiente',
            puntaje REAL,
            error TEXT,
            duracion_ms INTEGER,

            FOREIGN KEY (analisis_id)
                REFERENCES analisis(id)
                ON DELETE CASCADE,

            UNIQUE (analisis_id, url)
        );

        CREATE TABLE IF NOT EXISTS problemas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pagina_id INTEGER NOT NULL,
            regla_id TEXT NOT NULL,
            impacto TEXT NOT NULL,
            descripcion TEXT,
            ayuda TEXT,
            elementos_afectados TEXT,

            FOREIGN KEY (pagina_id)
                REFERENCES paginas(id)
                ON DELETE CASCADE,

            UNIQUE (pagina_id, regla_id)
        );

        CREATE TABLE IF NOT EXISTS recomendaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            problema_id INTEGER NOT NULL UNIQUE,
            explicacion TEXT,
            impacto_usuarios TEXT,
            recomendacion TEXT,
            codigo_sugerido TEXT,
            fecha_generacion TEXT,

            FOREIGN KEY (problema_id)
                REFERENCES problemas(id)
                ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS idx_paginas_analisis
        ON paginas(analisis_id);

        CREATE INDEX IF NOT EXISTS idx_problemas_pagina
        ON problemas(pagina_id);

        CREATE INDEX IF NOT EXISTS idx_analisis_fecha
        ON analisis(fecha_inicio);
    """)

    conexion.commit()
    conexion.close()

    print("Tablas creadas correctamente.")


if __name__ == "__main__":
    crear_tablas()