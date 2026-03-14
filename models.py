from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from database import Base
from datetime import datetime

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, autoincrement=True, primary_key=True)
    nome = Column(String(100), nullable=False)
    sobrenome = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    telefone = Column(String, unique=True, nullable=False)
    data_nascimento = Column(DateTime, nullable=False)
    status = Column(Boolean, nullable=False, default=True)

class Servico(Base):
    __tablename__ = 'servicos'

    id = Column(Integer, autoincrement=True, primary_key=True)
    nome_cliente = Column(String(100), nullable=False)
    descricao = Column(String, nullable=False)
    valor = Column(Float, nullable=False)
    data_servico = Column(DateTime, default=datetime.utcnow)
    prazo = Column(DateTime)
    status = Column(String, nullable=False, default='pendente')

    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)



