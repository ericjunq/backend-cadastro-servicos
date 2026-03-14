from fastapi import APIRouter, Depends, HTTPException
from schemas import ServicoSchema, ServicosUpdate
from dependencies import get_db
from sqlalchemy.orm import Session
from models import Servico, Usuario
from security import get_current_user
from datetime import datetime
from sqlalchemy import func

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


@task_router.patch('/atualizar_servico/{id}')
async def alterar_servico(id: int, servico_update: ServicosUpdate, db : Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    servico = db.query(Servico).filter(Servico.id == id, Servico.usuario_id == usuario.id).first()

    if not servico:
        raise HTTPException(status_code=404, detail='Serviço não encontrado')
    
    dados_update = servico_update.dict(exclude_unset=True)

    for campo, valor in dados_update.items():
        setattr(servico, campo, valor)
    
    db.commit()
    db.refresh(servico)

    return servico

@task_router.get('/meus_servicos')
async def Listar_meus_pedidos(nome_cliente: str | None = None, data_servico: datetime | None = None, prazo : datetime | None = None, db : Session = Depends(get_db), usuario : Usuario = Depends(get_current_user)):
    servicos = db.query(Servico).filter(Servico.usuario_id == usuario.id)

    if nome_cliente:
        servicos = servicos.filter(Servico.nome_cliente.contains(nome_cliente))
    
    if data_servico:
        servicos = servicos.filter(
        func.date(Servico.data_servico) == data_servico.date()
    )

    if prazo:
        servicos = servicos.filter(
        func.date(Servico.prazo) == prazo.date()
    )
    return servicos.all()

    





