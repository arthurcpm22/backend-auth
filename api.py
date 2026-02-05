from fastapi import FastAPI
from logging_utils import log_evento
from validation import validar_usuario

app = FastAPI()


@app.post("/usuarios")
def criar_usuario(dados: dict):
    usuario, erro = validar_usuario(dados)

    if erro:
        log_evento("WARN", f"Erro ao criar usuário: {erro}")
        return {"erro": erro}

    log_evento("INFO", f'Usuário criado via API: {usuario["nome"]}')
    return {"usuario": usuario}
