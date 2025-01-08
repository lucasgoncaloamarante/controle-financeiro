from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from ..auth import hash_password, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, create_recovery_token, generate_email_verification_token, verify_email_token
from ..database import SessionLocal
from .models import Usuario
from .schemas import UsuarioCreate, LoginRequest, UsuarioResponse, UpdateUserRequest  # ADIÇÃO
from .email import send_password_reset_email, send_email_verification  # ADIÇÃO

router = APIRouter()

#Dependência para sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota de registro
@router.post("/register", response_model=UsuarioResponse)
def register_user(user: UsuarioCreate, db: Session = Depends(get_db)):
    # Verifica se o email já está cadastrado
    db_user = db.query(Usuario).filter(Usuario.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")
    
    # Hash da senha
    hashed_password = hash_password(user.senha)

    # Cria o novo usuário incluindo o nome
    db_user = Usuario(
        nome=user.nome,  # Incluindo o nome do usuário
        email=user.email,
        senha_hash=hashed_password,
        email_verificado=user.email_verificado
    )

    # Adiciona e salva o usuário no banco de dados
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # Atualiza com os dados salvos

    # Gerar token de verificação e enviar email
    token = generate_email_verification_token(user.email)
    send_email_verification(user.email, token)

    # Retorna o usuário com ID e email, conforme o esquema UsuarioResponse
    return UsuarioResponse(id=db_user.id, email=db_user.email)

# Rota para confirmar o e-mail  # ADIÇÃO
@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    email = verify_email_token(token)
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    user.email_verificado = True
    db.commit()
    return {"msg": "E-mail verificado com sucesso."}

# Rota de login
@router.post("/login")
def login_for_access_token(form_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == form_data.email).first()
    if not user or not verify_password(form_data.senha, user.senha_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")

    if not user.email_verificado:  # ADIÇÃO
        raise HTTPException(status_code=403, detail="E-mail não verificado.")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = generate_access_token(data={"sub": user.email}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

# Rota para atualizar dados do usuário (nome ou email)  # ADIÇÃO
@router.put("/update_user")
def update_user(request: UpdateUserRequest, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.id == request.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    # Atualiza nome ou email
    if request.nome:
        user.nome = request.nome
    if request.email and user.email != request.email:
        user.email = request.email
        user.verificado = False  # ADIÇÃO: Requer nova verificação
        token = generate_email_verification_token(user.email)
        send_email_verification(user.email, token)

    db.commit()
    db.refresh(user)

    return {"msg": "Dados atualizados. Verifique seu e-mail se houver alteração."}

# Rota para desativar usuário (adição de status ativo/inativo)  # ADIÇÃO
@router.put("/toggle_user")
def toggle_user(email: str, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    user.ativo = not user.ativo  # Inverte o status ativo/inativo
    db.commit()
    return {"msg": f"Usuário {'ativado' if user.ativo else 'desativado'} com sucesso."}

# Rota para atualizar a senha
@router.put("/update_password")
def update_password(email: str, nova_senha: str, db: Session = Depends(get_db)):
    # Verifica se o usuário existe pelo email
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    # Cria um novo hash para a nova senha
    hashed_password = hash_password(nova_senha)

    # Atualiza a senha do usuário
    user.senha_hash = hashed_password
    db.commit()
    db.refresh(user)

    return {"msg": "Senha atualizada com sucesso."}

# Endpoint de recuperação de senha
@router.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    # Gerar token de recuperação
    token = create_recovery_token(user.email)  # Função que cria o token de recuperação (ex: JWT).
    
    # Enviar o e-mail de recuperação
    send_password_reset_email(user.email, token)
    
    return {"message": "Um e-mail de recuperação foi enviado."}

@router.post("/reset-password")
def reset_password(token: str, nova_senha: str, db: Session = Depends(get_db)):
    # Verificar se o token é válido
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Token inválido.")
    except JWTError:
        raise HTTPException(status_code=400, detail="Token inválido ou expirado.")
    
    # Verifica se o usuário existe
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    # Cria um novo hash para a nova senha
    hashed_password = hash_password(nova_senha)

    # Atualiza a senha do usuário
    user.senha_hash = hashed_password
    db.commit()
    db.refresh(user)

    return {"msg": "Senha atualizada com sucesso."}

# Rota para deletar um usuário
@router.delete("/delete_user")
def delete_user(email: str, db: Session = Depends(get_db)):
    # Verifica se o usuário existe
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    # Deleta o usuário
    db.delete(user)
    db.commit()

    return {"msg": "Usuário deletado com sucesso."}