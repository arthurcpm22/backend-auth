from database import init_db, inserir_usuario, listar_usuarios_db
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from logging_utils import log_evento
from validation import validar_usuario

app = FastAPI()
@app.on_event("startup")
def startup():
    init_db()

USUARIOS = []

TOKENS = {
    "token-user-123": {"sub": "user1", "role": "user"},
    "token-admin-123": {"sub": "admin1", "role": "admin"},
}

security = HTTPBearer()

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(security)):
    token = creds.credentials
    user = TOKENS.get(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user

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


