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