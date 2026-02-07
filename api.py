from database import init_db, inserir_usuario, listar_usuarios_db, buscar_usuario_por_id, buscar_usuario_por_email
from database import init_db, inserir_usuario, listar_usuarios_db, buscar_usuario_por_id, buscar_usuario_por_email, atualizar_usuario, deletar_usuario
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from logging_utils import log_evento
from validation import validar_usuario
from auth_utils import hash_senha, verificar_senha, criar_access_token, decodificar_token
from schemas import UsuarioCreate, UsuarioOut, UsuariosListOut, LoginIn, TokenOut
from schemas import UsuarioCreate, UsuarioUpdate, UsuarioOut, UsuariosListOut, LoginIn, TokenOut

app = FastAPI()
@app.on_event("startup")
def startup():
    init_db()
    admin_email = "admin@jf.com"
    admin = buscar_usuario_por_email(admin_email)
    if not admin:
        inserir_usuario({
            "email": admin_email,
            "nome": "Admin",
            "senha_hash": hash_senha("123456"),
            "role": "admin",
            "idade": 30,
            "ativo": True,
        })

USUARIOS = []

TOKENS = {
    "token-user-123": {"sub": "user1", "role": "user"},
    "token-admin-123": {"sub": "admin1", "role": "admin"},
}

security = HTTPBearer()

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(security)):
    token = creds.credentials
    payload = decodificar_token(token)
    email = payload.get("sub")

    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = buscar_usuario_por_email(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    return user  # contém role


def require_admin(user=Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden: admin only")
    return user




@app.post("/usuarios", status_code=status.HTTP_201_CREATED)
def criar_usuario(dados: dict, user=Depends(get_current_user)):
    usuario, erro = validar_usuario(dados)
    if erro:
        log_evento("WARN", f"Falha na validação (por {user['sub']}): {erro}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=erro)

    inserir_usuario(usuario)
    log_evento("INFO", f"Usuário criado via API por {user['sub']}: {usuario['nome']}")
    return usuario


@app.get("/usuarios")
def listar_usuarios(admin=Depends(require_admin)):
    usuarios = listar_usuarios_db()
    return {"total": len(usuarios), "usuarios": usuarios}

@app.get("/usuarios/{usuario_id}")
def obter_usuario(usuario_id: int, admin=Depends(require_admin)):
    usuario = buscar_usuario_por_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return usuario


@app.put("/usuarios/{usuario_id}", response_model=UsuarioOut)
def atualizar_usuario_endpoint(usuario_id: int, dados: UsuarioUpdate, admin=Depends(require_admin)):
    atual = buscar_usuario_por_id(usuario_id)
    if not atual:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    # começa do estado atual
    novo = dict(atual)

    # atualizações simples
    if dados.email is not None:
        novo["email"] = dados.email
    if dados.nome is not None:
        novo["nome"] = dados.nome
    if dados.role is not None:
        if dados.role not in ("admin", "user"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="role inválida")
        novo["role"] = dados.role

    # idade/ativo continuam vindo como string (padrão do nosso projeto)
    payload_validacao = {
        "nome": novo["nome"],
        "idade_str": dados.idade_str if dados.idade_str is not None else str(novo["idade"]),
        "ativo_str": dados.ativo_str if dados.ativo_str is not None else ("s" if novo["ativo"] else "n"),
    }
    validado, erro = validar_usuario(payload_validacao)
    if erro:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=erro)

    # aplica os campos validados
    novo["idade"] = validado["idade"]
    novo["ativo"] = validado["ativo"]

    # troca senha se veio senha nova
    user_full = buscar_usuario_por_email(novo["email"])
    senha_hash_atual = user_full["senha_hash"] if user_full else None
    if dados.senha is not None:
        senha_hash_atual = hash_senha(dados.senha)

    # salvar no banco (email/nome/role/idade/ativo)
    ok = atualizar_usuario(usuario_id, {
        "email": novo["email"],
        "nome": novo["nome"],
        "role": novo["role"],
        "idade": novo["idade"],
        "ativo": novo["ativo"],
    })
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    # Se você quiser persistir senha_hash via UPDATE também, a gente faz no próximo passo.
    # Por enquanto, vamos manter simples: role/dados básicos.

    return novo


@app.delete("/usuarios/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_usuario_endpoint(usuario_id: int, admin=Depends(require_admin)):
    ok = deletar_usuario(usuario_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return


@app.post("/login", response_model=TokenOut)
def login(dados: LoginIn):
    user = buscar_usuario_por_email(dados.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

    if not verificar_senha(dados.senha, user["senha_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

    token = criar_access_token(subject=user["email"])
    return {"access_token": token, "token_type": "bearer"}
