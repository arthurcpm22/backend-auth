import sqlite3

DB_NAME = "app.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER NOT NULL,
            ativo INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def inserir_usuario(usuario):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO usuarios (nome, idade, ativo) VALUES (?, ?, ?)",
        (usuario["nome"], usuario["idade"], int(usuario["ativo"]))
    )

    conn.commit()
    conn.close()


def listar_usuarios_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome, idade, ativo FROM usuarios")
    rows = cursor.fetchall()
    conn.close()

    usuarios = []
    for r in rows:
        usuarios.append({
            "id": r[0],
            "nome": r[1],
            "idade": r[2],
            "ativo": bool(r[3]),
        })

    return usuarios

def buscar_usuario_por_id(usuario_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, idade, ativo FROM usuarios WHERE id = ?", (usuario_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {"id": row[0], "nome": row[1], "idade": row[2], "ativo": bool(row[3])}
