
import json
from datetime import datetime

from bdd.conexion import ConexionBD
from analisis.procesador_resultados import ProcesadorResultados


class RepositorioAnalisis:

    def __init__(self):
        self.bd = ConexionBD()

    # ----------------------------------
    # CREAR UN ANALISIS
    # ----------------------------------

    def crear_analisis(self, urls):
        conexion = self.bd.conectar()

        try:
            with conexion:
                cursor = conexion.cursor()

                fecha_inicio = datetime.now().astimezone().isoformat(
                    timespec="seconds"
                )

                cursor.execute("""
                    INSERT INTO analisis (
                        fecha_inicio,
                        total_paginas,
                        estado
                    )
                    VALUES (?, ?, ?)
                """, (
                    fecha_inicio,
                    len(urls),
                    "pendiente"
                ))

                analisis_id = cursor.lastrowid

                paginas = [
                    (analisis_id, url)
                    for url in urls
                ]

                cursor.executemany("""
                    INSERT INTO paginas (
                        analisis_id,
                        url
                    )
                    VALUES (?, ?)
                """, paginas)

            return analisis_id

        finally:
            conexion.close()

    # ----------------------------------
    # INICIAR UN ANALISIS
    # ----------------------------------

    def iniciar_analisis(self, analisis_id):
        conexion = self.bd.conectar()

        try:
            with conexion:
                cursor = conexion.cursor()

                cursor.execute("""
                    UPDATE analisis
                    SET estado = 'en_ejecucion',
                        fecha_fin = NULL
                    WHERE id = ?
                """, (analisis_id,))

                if cursor.rowcount == 0:
                    raise ValueError(
                        f"No existe el análisis con ID {analisis_id}"
                    )

        finally:
            conexion.close()

    # ----------------------------------
    # FINALIZAR UN ANALISIS
    # ----------------------------------

    def finalizar_analisis(self, analisis_id):
        conexion = self.bd.conectar()

        try:
            with conexion:
                cursor = conexion.cursor()

                # Contar páginas según su estado
                cursor.execute("""
                    SELECT
                        COUNT(*),
                        SUM(CASE WHEN estado = 'completado' THEN 1 ELSE 0 END),
                        SUM(CASE WHEN estado = 'fallido' THEN 1 ELSE 0 END),
                        SUM(CASE WHEN estado = 'pendiente' THEN 1 ELSE 0 END)
                    FROM paginas
                    WHERE analisis_id = ?
                """, (analisis_id,))

                total, completadas, fallidas, pendientes = cursor.fetchone()

                if total == 0:
                    raise ValueError(
                        "El análisis no tiene páginas registradas."
                    )

                completadas = completadas or 0
                fallidas = fallidas or 0
                pendientes = pendientes or 0

                # Determinar estado final
                if pendientes > 0:
                    estado = "en_ejecucion"
                    fecha_fin = None

                elif fallidas == total:
                    estado = "fallido"
                    fecha_fin = datetime.now().astimezone().isoformat(
                        timespec="seconds"
                    )

                elif fallidas > 0:
                    estado = "completado_parcial"
                    fecha_fin = datetime.now().astimezone().isoformat(
                        timespec="seconds"
                    )

                else:
                    estado = "completado"
                    fecha_fin = datetime.now().astimezone().isoformat(
                        timespec="seconds"
                    )

                # Recuperar puntajes de las páginas completadas
                cursor.execute("""
                    SELECT puntaje
                    FROM paginas
                    WHERE analisis_id = ?
                      AND estado = 'completado'
                      AND puntaje IS NOT NULL
                """, (analisis_id,))

                puntajes = [
                    fila[0]
                    for fila in cursor.fetchall()
                ]

                # Calcular puntaje general
                procesador = ProcesadorResultados()

                puntaje_general = procesador.calcular_puntaje_general(
                    puntajes
                )

                # Actualizar registro general
                cursor.execute("""
                    UPDATE analisis
                    SET estado = ?,
                        fecha_fin = ?,
                        total_paginas = ?,
                        paginas_completadas = ?,
                        paginas_fallidas = ?,
                        puntaje_general = ?
                    WHERE id = ?
                """, (
                    estado,
                    fecha_fin,
                    total,
                    completadas,
                    fallidas,
                    puntaje_general,
                    analisis_id
                ))

                if cursor.rowcount == 0:
                    raise ValueError(
                        f"No existe el análisis con ID {analisis_id}"
                    )

                return {
                    "estado": estado,
                    "total_paginas": total,
                    "paginas_completadas": completadas,
                    "paginas_fallidas": fallidas,
                    "puntaje_general": puntaje_general
                }

        finally:
            conexion.close()
            
        
    # ----------------------------------
    # MARCAR ANALISIS INTERRUMPIDO
    # ----------------------------------

    def marcar_analisis_fallido(self, analisis_id, error):
        conexion = self.bd.conectar()

        try:
            with conexion:
                cursor = conexion.cursor()

                cursor.execute("""
                    UPDATE paginas
                    SET estado = 'fallido',
                        error = ?
                    WHERE analisis_id = ?
                      AND estado = 'pendiente'
                """, (
                    f"Análisis interrumpido: {error}",
                    analisis_id
                ))

                cursor.execute("""
                    SELECT
                        COUNT(*),
                        SUM(CASE WHEN estado = 'completado' THEN 1 ELSE 0 END),
                        SUM(CASE WHEN estado = 'fallido' THEN 1 ELSE 0 END)
                    FROM paginas
                    WHERE analisis_id = ?
                """, (analisis_id,))

                total, completadas, fallidas = cursor.fetchone()

                completadas = completadas or 0
                fallidas = fallidas or 0

                cursor.execute("""
                    SELECT AVG(puntaje)
                    FROM paginas
                    WHERE analisis_id = ?
                      AND estado = 'completado'
                      AND puntaje IS NOT NULL
                """, (analisis_id,))

                puntaje_general = cursor.fetchone()[0]

                fecha_fin = datetime.now().astimezone().isoformat(
                    timespec="seconds"
                )

                cursor.execute("""
                    UPDATE analisis
                    SET estado = 'fallido',
                        fecha_fin = ?,
                        total_paginas = ?,
                        paginas_completadas = ?,
                        paginas_fallidas = ?,
                        puntaje_general = ?
                    WHERE id = ?
                """, (
                    fecha_fin,
                    total,
                    completadas,
                    fallidas,
                    round(puntaje_general) if puntaje_general is not None else None,
                    analisis_id
                ))

                if cursor.rowcount == 0:
                    raise ValueError(
                        f"No existe el análisis con ID {analisis_id}"
                    )

        finally:
            conexion.close()


    # ----------------------------------
    # LISTAR ANALISIS
    # ----------------------------------

    def listar_analisis(self):
        conexion = self.bd.conectar()

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT *
                FROM analisis
                ORDER BY fecha_inicio DESC
            """)

            return cursor.fetchall()

        finally:
            conexion.close()

    # ----------------------------------
    # GUARDAR RESULTADOS DE UNA PAGINA
    # ----------------------------------

    def guardar_pagina(
        self,
        pagina_id,
        titulo=None,
        url_final=None,
        estado="completado",
        puntaje=None,
        error=None,
        duracion_ms=None
    ):
        conexion = self.bd.conectar()

        try:
            with conexion:
                cursor = conexion.cursor()

                cursor.execute("""
                    UPDATE paginas
                    SET titulo = ?,
                        url_final = ?,
                        estado = ?,
                        puntaje = ?,
                        error = ?,
                        duracion_ms = ?
                    WHERE id = ?
                """, (
                    titulo,
                    url_final,
                    estado,
                    puntaje,
                    error,
                    duracion_ms,
                    pagina_id
                ))

                if cursor.rowcount == 0:
                    raise ValueError(
                        f"No existe la página con ID {pagina_id}"
                    )

        finally:
            conexion.close()

    # ----------------------------------
    # GUARDAR PROBLEMAS DETECTADOS
    # ----------------------------------

    def guardar_problemas(self, pagina_id, problemas):
        conexion = self.bd.conectar()

        try:
            with conexion:
                cursor = conexion.cursor()

                for problema in problemas:
                    elementos_json = json.dumps(
                        problema.get("elementos_afectados", []),
                        ensure_ascii=False
                    )

                    cursor.execute("""
                        INSERT INTO problemas (
                            pagina_id,
                            regla_id,
                            impacto,
                            descripcion,
                            ayuda,
                            elementos_afectados
                        )
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        pagina_id,
                        problema["regla_id"],
                        problema["impacto"],
                        problema.get("descripcion"),
                        problema.get("ayuda"),
                        elementos_json
                    ))

        finally:
            conexion.close()

    # ----------------------------------
    # GUARDAR RECOMENDACION DE IA
    # ----------------------------------

    def guardar_recomendacion(self, problema_id, resultado):
        conexion = self.bd.conectar()

        try:
            with conexion:
                cursor = conexion.cursor()

                fecha_generacion = datetime.now().astimezone().isoformat(
                    timespec="seconds"
                )

                cursor.execute("""
                    INSERT INTO recomendaciones (
                        problema_id,
                        explicacion,
                        impacto_usuarios,
                        recomendacion,
                        codigo_sugerido,
                        fecha_generacion
                    )
                    VALUES (?, ?, ?, ?, ?, ?)

                    ON CONFLICT(problema_id) DO UPDATE SET
                        explicacion = excluded.explicacion,
                        impacto_usuarios = excluded.impacto_usuarios,
                        recomendacion = excluded.recomendacion,
                        codigo_sugerido = excluded.codigo_sugerido,
                        fecha_generacion = excluded.fecha_generacion
                """, (
                    problema_id,
                    resultado["explicacion"],
                    resultado["impacto_usuarios"],
                    resultado["recomendacion"],
                    resultado["codigo_sugerido"],
                    fecha_generacion
                ))

        finally:
            conexion.close()

    # ----------------------------------
    # OBTENER PAGINAS
    # ----------------------------------

    def obtener_paginas(self, analisis_id):
        conexion = self.bd.conectar()

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT *
                FROM paginas
                WHERE analisis_id = ?
                ORDER BY id
            """, (analisis_id,))

            return cursor.fetchall()

        finally:
            conexion.close()

    # ----------------------------------
    # OBTENER PROBLEMAS
    # ----------------------------------

    def obtener_problemas(self, pagina_id):
        conexion = self.bd.conectar()

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT *
                FROM problemas
                WHERE pagina_id = ?
                ORDER BY id
            """, (pagina_id,))

            problemas = cursor.fetchall()

            resultados = []

            for problema in problemas:
                problema = list(problema)

                problema[6] = json.loads(
                    problema[6] or "[]"
                )

                resultados.append(problema)

            return resultados

        finally:
            conexion.close()

    # ----------------------------------
    # OBTENER RECOMENDACION
    # ----------------------------------

    def obtener_recomendacion(self, problema_id):
        conexion = self.bd.conectar()

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT *
                FROM recomendaciones
                WHERE problema_id = ?
            """, (problema_id,))

            return cursor.fetchone()

        finally:
            conexion.close()

    # ----------------------------------
    # OBTENER ANALISIS COMPLETO
    # ----------------------------------

    def obtener_analisis_completo(self, analisis_id):
        conexion = self.bd.conectar()

        try:
            cursor = conexion.cursor()

            # Obtener análisis
            cursor.execute("""
                SELECT *
                FROM analisis
                WHERE id = ?
            """, (analisis_id,))

            analisis = cursor.fetchone()

            if analisis is None:
                return None

            # Obtener páginas
            cursor.execute("""
                SELECT *
                FROM paginas
                WHERE analisis_id = ?
                ORDER BY id
            """, (analisis_id,))

            paginas = cursor.fetchall()

            resultado = {
                "analisis": analisis,
                "paginas": []
            }

            for pagina in paginas:
                pagina_id = pagina[0]

                # Obtener problemas de la página
                cursor.execute("""
                    SELECT *
                    FROM problemas
                    WHERE pagina_id = ?
                    ORDER BY id
                """, (pagina_id,))

                problemas = cursor.fetchall()

                problemas_resultado = []

                for problema in problemas:
                    problema = list(problema)

                    # Convertir elementos afectados de JSON a Python
                    problema[6] = json.loads(
                        problema[6] or "[]"
                    )

                    problema_id = problema[0]

                    # Obtener recomendación
                    cursor.execute("""
                        SELECT *
                        FROM recomendaciones
                        WHERE problema_id = ?
                    """, (problema_id,))

                    recomendacion = cursor.fetchone()

                    problemas_resultado.append({
                        "datos": problema,
                        "recomendacion": recomendacion
                    })

                resultado["paginas"].append({
                    "datos": pagina,
                    "problemas": problemas_resultado
                })

            return resultado

        finally:
            conexion.close()
