from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "super_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Função para hashear senhas
def hash_password(password: str):
    return pwd_context.hash(password)

#Verifica se a senha informada base com o hash salvo
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Cria um token JWT
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Função para criar o token de recuperação
def create_recovery_token(email: str):
    """
    Cria um token de recuperação de senha para o usuário.
    """
    expiration_time = datetime.utcnow() + timedelta(hours=1)  # Token válido por 1 hora
    payload = {
        "sub": email,  # Armazenar o e-mail do usuário no payload
        "exp": expiration_time  # Definir tempo de expiração
    }
    
    # Gerar o token de recuperação JWT
    recovery_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    return recovery_token

# Verifica e decodifica o token de recuperação
def verify_recovery_token(token: str):
    """
    Verifica a validade do token de recuperação de senha.
    Retorna o email se o token for válido, caso contrário, gera uma exceção.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise JWTError("Token inválido: email não encontrado.")
        return email
    except JWTError:
        raise JWTError("Token inválido ou expirado.")

# Verifica e decodifica o token de verificação de e-mail
def verify_email_token(token: str):
    """
    Verifica a validade do token de verificação de e-mail.
    Retorna o e-mail se o token for válido, caso contrário, gera uma exceção.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None or payload.get("type") != "email_verification":
            raise JWTError("Token inválido ou tipo de token incorreto.")
        return email
    except JWTError:
        raise JWTError("Token inválido ou expirado.")

def generate_email_verification_token(email: str):
    """
    Gera um token de verificação de e-mail.
    """
    expiration_time = datetime.utcnow() + timedelta(hours=24)  # Token válido por 24 horas
    payload = {
        "sub": email,
        "exp": expiration_time,
        "type": "email_verification"
    }
    
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)