from fastapi import FastAPI, BackgroundTasks, Depends
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session
from database import engine, get_db
import models
import re

# Criar tabelas
models.Base.metadata.create_all(bind=engine)

# Pydantic Entragador Schema
class EntregadorCriar(BaseModel):
    nome: str
    email: str
    cnpj: int
    veiculo: models.TipoVeiculo
    senha: str

    @field_validator('cpf')
    @classmethod
    def validar_cpf(cls, v: str):
        cpf_limpo = re.sub(r'[^0-9]', '', v)
        if len(cpf_limpo) != 11:
            raise ValueError('O CPF deve conter exatamente 11 números.')
        return cpf_limpo


app = FastAPI(title="ExpressBR")

# Home
@app.get("/")
def home():
    return "Olá"

"""
Forma de cadastrar entregadores.
Dados necessários: Nome, email (único), senha (criptografada), CNPJ e veículo (Moto ou Carro)
"""
@app.post("/cadastro")
def cadastrar(
    usuario: EntregadorCriar,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
    ):
    """
    Rota para criar novo usuário/entregador
    """
    pass


"""
Apenas entregadores logados podem criar ou ver pedidos de entrega
Dados necessários do pedido: CEP de Origem, CEP de Destino, Peso do Pacote, Valor da Corrida (calculado automatimante)
10 reais + 2.50 por kg
"""

"""
Simular o envio de um SMS para o cliente final avisando que o entregador já está a caminho
"""

"""
Função assíncrona que simula esse envio (com um asyncio.sleep(3)) exibindo um print no terminal.
Ela deve rodar em background para não atrasar a resposta da API.
"""
