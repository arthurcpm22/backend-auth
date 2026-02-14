from fastapi import FastAPI

from .database import init_db, buscar_usuario_por_email, inserir_usuario
from .auth_utils import hash_senha
from .routes.auth import router as auth_router
from .routes.users import router as users_router

app = FastAPI()
@app.get("/health")
def health():
    return {"status": "healthy"}

app.include_router(auth_router)
app.include_router(users_router)


@app.on_event("startup")
def startup():
    init_db()

    admin_email = "admin@jf.com"
    if not buscar_usuario_por_email(admin_email):
        inserir_usuario({
            "email": admin_email,
            "nome": "Admin",
            "senha_hash": hash_senha("123456"),
            "role": "admin",
            "idade": 30,
            "ativo": True,
        })
