from pydantic import BaseModel, EmailStr


class UsuarioCreate(BaseModel):
    email: EmailStr
    nome: str
    senha: str
    idade_str: str
    ativo_str: str

from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nome: Optional[str] = None
    senha: Optional[str] = None
    role: Optional[str] = None  # "admin" ou "user"
    idade_str: Optional[str] = None
    ativo_str: Optional[str] = None


class UsuarioOut(BaseModel):
    id: int
    email: EmailStr
    nome: str
    role: str
    idade: int
    ativo: bool


class UsuariosListOut(BaseModel):
    total: int
    usuarios: list[UsuarioOut]


class LoginIn(BaseModel):
    email: EmailStr
    senha: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
