from sqlalchemy import Column, Integer, String, Enum as SqlEnum
from database import Base
from enum import Enum

class TipoVeiculo(str, Enum):
    MOTO = "Moto"
    CARRO = "Carro"

class Entregador(Base):
    __tablename__ = "entregadores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    cnpj = Column(String(14), unique=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    veiculo = Column(SqlEnum(TipoVeiculo), nullable=False)
