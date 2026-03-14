from fastapi import APIRouter, Depends, HTTPException
from schemas import UsuarioSchema, UsuarioResponse, UsuarioUpdateSchema
from sqlalchemy.orm import Session
from dependencies import get_db
from models import Usuario
from security import verificar_senha, criptografar_senha, criar_token, get_current_user, criar_refreshtoken, verificar_refresh_token
from validations import validar_telefone, validar_cpf
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError

auth_router = APIRouter(prefix='/users', tags=['usuarios'])

# ROTA PARA CADASTRO
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
    
    cpf_valido = validar_cpf(usuarioschema.cpf)
    if not cpf_valido:
        raise HTTPException(status_code=400, detail='CPF inválido')
    
    telefone_valido = validar_telefone(usuarioschema.telefone)
    if not telefone_valido:
        raise HTTPException(status_code=400, detail='Telefone inválido')
    
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

# ROTA PARA LOGIN
@auth_router.post('/login')
async def login(form_data : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario_db = db.query(Usuario).filter(
        Usuario.email == form_data.username
    ).first()
    if not usuario_db:
        raise HTTPException(
            status_code=404,
            detail='Usuário não encontrado'
        )
    
    if not verificar_senha(form_data.password, usuario_db.senha_hash):
        raise HTTPException(status_code=401, detail='Senha incorreta')
    
    access_token = criar_token(
        data={'sub': usuario_db.email, 'type': 'access'}
    )

    refresh_token = criar_refreshtoken(
        data={'sub': usuario_db.email, 'type': 'refresh'}
    )

    return {
        'access_token' : access_token,
        'refresh_token': refresh_token,
        'token_type' : 'bearer'   
    }


# ROTA PARA EDITAR PERFIL DE USUÁRIO 
@auth_router.patch('/editar_usuario/{usuario_id}')
async def editar_usuario(usuario_id: int, usuario_update: UsuarioUpdateSchema, db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')
    
    dados_update = usuario_update.dict(exclude_unset=True)

    if 'email' in dados_update:
        email_existente = db.query(Usuario).filter(Usuario.email == dados_update['email']).first()
        if email_existente and email_existente.id != usuario.id:
            raise HTTPException(status_code=400, detail='Email já cadastrado')
    
    if 'telefone' in dados_update:
        if not validar_telefone(dados_update['telefone']):
            raise HTTPException(status_code=400, detail='Telefone inválido')
        
        telefone_existente = db.query(Usuario).filter(Usuario.telefone == dados_update['telefone']).first()
        if telefone_existente and telefone_existente.id != usuario.id:
            raise HTTPException(status_code=400, detail='Telefone já cadastrado')

    for campo, valor in dados_update.items():
        setattr(usuario, campo, valor)
    
    db.commit()
    db.refresh(usuario)

    return usuario

@auth_router.post('/refresh')
async def refresh_token(refresh_token: str):
    email = verificar_refresh_token(refresh_token)
    if not email:
        raise HTTPException(status_code=401, detail='Refresh token inválido')
    
    novo_access_token = criar_token(
        data={'sub': email}
    )

    return {
        'access_token' : novo_access_token,
        'token_type': 'bearer'
    }