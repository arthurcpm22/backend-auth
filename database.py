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
            email TEXT NOT NULL UNIQUE,
            nome TEXT NOT NULL,
            senha_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            idade INTEGER NOT NULL,
            ativo INTEGER NOT NULL
        )
    """)

    try:
        cursor.execute(
            "ALTER TABLE usuarios ADD COLUMN role TEXT NOT NULL DEFAULT 'user'"
        )
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()


def inserir_usuario(usuario: dict):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO usuarios (email, nome, senha_hash, role, idade, ativo) VALUES (?, ?, ?, ?, ?, ?)",
        (
            usuario["email"],
            usuario["nome"],
            usuario["senha_hash"],
            usuario.get("role", "user"),
            usuario["idade"],
            int(usuario["ativo"]),
        )
    )

    conn.commit()
    conn.close()


def listar_usuarios_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, email, nome, role, idade, ativo FROM usuarios"
    )

    rows = cursor.fetchall()
    conn.close()

    usuarios = []
    for r in rows:
        usuarios.append({
            "id": r[0],
            "email": r[1],
            "nome": r[2],
            "role": r[3],
            "idade": r[4],
            "ativo": bool(r[5]),
        })

    return usuarios


def buscar_usuario_por_id(usuario_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, email, nome, role, idade, ativo FROM usuarios WHERE id = ?",
        (usuario_id,)
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "email": row[1],
        "nome": row[2],
        "role": row[3],
        "idade": row[4],
        "ativo": bool(row[5]),
    }


def buscar_usuario_por_email(email: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, email, nome, senha_hash, role, idade, ativo FROM usuarios WHERE email = ?",
        (email,)
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "email": row[1],
        "nome": row[2],
        "senha_hash": row[3],
        "role": row[4],
        "idade": row[5],
        "ativo": bool(row[6]),
    }

def atualizar_usuario(usuario_id: int, dados: dict) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE usuarios
        SET email = ?, nome = ?, role = ?, idade = ?, ativo = ?
        WHERE id = ?
        """,
        (
            dados["email"],
            dados["nome"],
            dados["role"],
            dados["idade"],
            int(dados["ativo"]),
            usuario_id,
        )
    )

    alterou = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return alterou


def deletar_usuario(usuario_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
    deletou = cursor.rowcount > 0

    conn.commit()
    conn.close()
    return deletou
