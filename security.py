from pwdlib import PasswordHash
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from models import Usuario


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACESS_TOKEN_EXPIRES_DAYS = int(os.getenv("ACESS_TOKEN_EXPIRES_DAYS"))

oauth_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


password_hash = PasswordHash.recommended()

def criptografar_senha(senha: str) -> str:
    return password_hash.hash(senha)

def verificar_senha(senha: str , hash: str) -> bool:
    return password_hash.verify(senha, hash)

def criar_token(data : dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=ACESS_TOKEN_EXPIRES_DAYS)
    to_encode.update({"exp" : expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail='Token Inválido')
    
    except JWTError:
        raise HTTPException(status_code=401, detail='Token Inválido')

    usuario = db.query(Usuario).filter(Usuario.email == email).first()

    if usuario is None:
        raise HTTPException(status_code=401, detail='Usuário não encontrado')
    
    return usuario 