from pydantic import BaseModel, EmailStr
from typing import Optional

# Esquema para registro de usuário
class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    email_verificado: Optional[bool] = False

# Esquema para login de usuário
class LoginRequest(BaseModel):
    email: EmailStr
    senha: str

# Esquema de resposta (após registro/login)
class UsuarioResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True # Permite retornar dados do SQLAlchemy para Pydantic

# Esquema para atualização de usuário
class UpdateUserRequest(BaseModel):
    id: int
    nome: Optional[str] = None
    email: Optional[EmailStr] = None