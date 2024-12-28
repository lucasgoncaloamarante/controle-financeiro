from pydantic import BaseModel, EmailStr

# Esquema para registro de usuário
class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str

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