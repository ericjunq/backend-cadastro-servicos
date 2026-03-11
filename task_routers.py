from fastapi import APIRouter, Depends, HTTPException
from schemas import ServicoSchema
from dependencies import get_db
from sqlalchemy.orm import Session
from models import Servico
from security import get_current_user
from models import Usuario

task_router = APIRouter(prefix='/servico', tags=['servicos'])

@task_router.post('/cadastrar_servico')
async def cadastrar_servico(servico_schema: ServicoSchema, db : Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    novo_servico = Servico(
        nome_cliente=servico_schema.nome_cliente,
        descricao=servico_schema.descricao,
        valor=servico_schema.valor,
        data_servico=servico_schema.data_servico,
        prazo=servico_schema.prazo,
        status=servico_schema.status,
        usuario_id = usuario.id
    )
    db.add(novo_servico)
    db.commit()
    db.refresh(novo_servico)

    return novo_servico




