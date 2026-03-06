from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum

class StatusEnum(str, Enum):
    pendente = 'pendente'
    cancelado = 'cancelado'
    concluido = 'concluido'
    em_andamento = 'em andamento'

class UsuarioSchema(BaseModel):
    nome : str
    sobrenome : str
    email : str
    senha : str
    cpf : str
    telefone : str
    data_nascimento : datetime

class LoginSchema(BaseModel):
    email : str
    senha : str

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    sobrenome: str
    email: str
    class Config:
        from_attributes = True

class ServicoSchema(BaseModel):
    nome_cliente : str
    descricao: str 
    valor : float 
    data_do_pedido : datetime 
    prazo : Optional[datetime] = None 
    status : StatusEnum = StatusEnum.pendente
   

