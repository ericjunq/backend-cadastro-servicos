from fastapi import APIRouter, Depends, HTTPException
from schemas import UsuarioSchema, LoginSchema, UsuarioResponse
from sqlalchemy.orm import Session
from dependencies import get_db
from models import Usuario
from security import verificar_senha, criptografar_senha, criar_token

auth_router = APIRouter(prefix='/users', tags=['usuarios'])

@auth_router.post('/cadastro', response_model=UsuarioResponse)
async def cadastrar_usuario(usuarioschema : UsuarioSchema, db : Session = Depends(get_db)):
    email_existente = db.query(Usuario).filter(
        Usuario.email == usuarioschema.email
    ).first()
    if email_existente:
        raise HTTPException(
            status_code=400,
            detail='Email já cadastrado'
        )
    
    senha_hash = criptografar_senha(usuarioschema.senha)

    novo_usuario = Usuario(
        nome = usuarioschema.nome,
        sobrenome=usuarioschema.sobrenome,
        email=usuarioschema.email,
        senha_hash=senha_hash,
        cpf=usuarioschema.cpf,
        telefone=usuarioschema.telefone,
        data_nascimento=usuarioschema.data_nascimento
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    
    return novo_usuario

@auth_router.post('/login')
async def login(usuarioschema : LoginSchema, db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(
        Usuario.email == usuarioschema.email
    ).first()
    if not usuario_db:
        raise HTTPException(
            status_code=404,
            detail='Usuário não encontrado'
        )
    if not verificar_senha(usuarioschema.senha, usuario_db.senha_hash):
        raise HTTPException(status_code=401, detail='Senha incorreta')
    
    acess_token = criar_token(
        data={'sub': usuario_db.email}
    )
    return {
        'access_token' : acess_token,
        'token_type' : 'bearer'   
    }