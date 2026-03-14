from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum

class StatusEnum(str, Enum):
    pendente = 'pendente'
    cancelado = 'cancelado'
    concluido = 'concluido'
    em_andamento = 'em andamento'

class UsuarioStatusEnum(str, Enum):
    ativo = 'ativo'
    inativo_usuario = 'inativo_usuario'
    inativo_servidor = 'inativo_servidor'
    banido = 'banido'

class UsuarioSchema(BaseModel):
    nome : str
    sobrenome : str
    email : EmailStr
    senha : str
    cpf : str
    telefone : str
    data_nascimento : datetime

class LoginSchema(BaseModel):
    email : str
    senha : str

class UsuarioUpdateSchema(BaseModel):
    nome: Optional[str] = None
    sobrenome: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    sobrenome: str
    email: str
    class Config:
        from_attributes = True

class ServicosUpdate(BaseModel):
    nome_cliente : Optional[str] = None
    descricao : Optional[str] = None
    valor : Optional[float] = None
    data_servico: Optional[datetime] = None
    prazo: Optional[datetime] = None
    status: Optional[bool] = None

class ServicoSchema(BaseModel):
    nome_cliente : str
    descricao: str 
    valor : float 
    data_servico : datetime 
    prazo : Optional[datetime] = None 
    status : StatusEnum = StatusEnum.pendente

