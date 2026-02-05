from fastapi import FastAPI, HTTPException, status
from validation import validar_usuario
from logging_utils import log_evento

app = FastAPI()


@app.post("/usuarios", status_code=status.HTTP_201_CREATED)
def criar_usuario(dados: dict):
    usuario, erro = validar_usuario(dados)

    if erro:
        log_evento("WARN", f"Erro ao criar usuário: {erro}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=erro
        )

    log_evento("INFO", f'Usuário criado via API: {usuario["nome"]}')
    return usuario
