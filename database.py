import sqlite3
from datetime import datetime

DB_NAME = "prisioneros.db"

def conectar():
    return sqlite3.connect(DB_NAME)

def crear_tabla():
    conn = conectar()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS reclusos (
            id INTEGER PRIMARY KEY,
            cedula TEXT,
            apellidos TEXT,
            nombres TEXT,
            fecha_nacimiento TEXT,
            edad INTEGER,
            natural_de TEXT,
            delito TEXT,
            tribunal TEXT,
            sentencia TEXT,
            pena_impuesta TEXT,
            sala_resguardo TEXT,
            tipo_sangre TEXT,
            foto_path TEXT,
            fecha_registro TEXT
        )
    """)
    # Asegurar columna tipo_sangre en bases antiguas
    try:
        c.execute("ALTER TABLE reclusos ADD COLUMN tipo_sangre TEXT")
    except:
        pass
    conn.commit()
    conn.close()

def obtener_proximo_id():
    """Devuelve el menor ID libre (empezando desde 1)"""
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT id FROM reclusos ORDER BY id")
    ids = [fila[0] for fila in c.fetchall()]
    conn.close()
    if not ids:
        return 1
    # Buscar el primer hueco
    for i, id_val in enumerate(ids, start=1):
        if i != id_val:
            return i
    return ids[-1] + 1

def insertar_recluso(datos):
    conn = conectar()
    c = conn.cursor()
    nuevo_id = obtener_proximo_id()
    c.execute("""
        INSERT INTO reclusos (id, cedula, apellidos, nombres,
            fecha_nacimiento, edad, natural_de, delito, tribunal,
            sentencia, pena_impuesta, sala_resguardo, tipo_sangre, foto_path, fecha_registro)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        nuevo_id,
        datos["cedula"],
        datos["apellidos"],
        datos["nombres"],
        datos["fecha_nacimiento"],
        datos["edad"],
        datos["natural_de"],
        datos["delito"],
        datos["tribunal"],
        datos["sentencia"],
        datos["pena_impuesta"],
        datos["sala_resguardo"],
        datos.get("tipo_sangre", ""),
        datos.get("foto_path", ""),
        datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    ))
    conn.commit()
    conn.close()

def obtener_todos():
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT id, cedula, apellidos, nombres, fecha_nacimiento, edad, "
              "natural_de, delito, tribunal, sentencia, pena_impuesta, "
              "sala_resguardo, tipo_sangre, foto_path, fecha_registro "
              "FROM reclusos ORDER BY id DESC")
    filas = c.fetchall()
    conn.close()
    return filas

def obtener_por_id(id_recluso):
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT id, cedula, apellidos, nombres, fecha_nacimiento, edad, "
              "natural_de, delito, tribunal, sentencia, pena_impuesta, "
              "sala_resguardo, tipo_sangre, foto_path, fecha_registro "
              "FROM reclusos WHERE id=?", (id_recluso,))
    fila = c.fetchone()
    conn.close()
    return fila

def actualizar_recluso(id_recluso, datos):
    conn = conectar()
    c = conn.cursor()
    c.execute("""
        UPDATE reclusos SET cedula=?, apellidos=?, nombres=?,
            fecha_nacimiento=?, edad=?, natural_de=?, delito=?, tribunal=?,
            sentencia=?, pena_impuesta=?, sala_resguardo=?, tipo_sangre=?, foto_path=?
        WHERE id=?
    """, (
        datos["cedula"],
        datos["apellidos"],
        datos["nombres"],
        datos["fecha_nacimiento"],
        datos["edad"],
        datos["natural_de"],
        datos["delito"],
        datos["tribunal"],
        datos["sentencia"],
        datos["pena_impuesta"],
        datos["sala_resguardo"],
        datos.get("tipo_sangre", ""),
        datos.get("foto_path", ""),
        id_recluso
    ))
    conn.commit()
    conn.close()

def eliminar_recluso(id_recluso):
    conn = conectar()
    c = conn.cursor()
    c.execute("DELETE FROM reclusos WHERE id=?", (id_recluso,))
    conn.commit()
    conn.close()