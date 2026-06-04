from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from database import Base
from enum import Enum

class TipoVeiculo(str, Enum):
    MOTO = "Moto"
    CARRO = "Carro"

class Entregador(Base):
    __tablename__ = "entregadores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False) # CORRIGIDO: Removido primary_key daqui
    email = Column(String, unique=True, index=True, nullable=False)
    cnpj = Column(String(14), unique=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    veiculo = Column(SqlEnum(TipoVeiculo), nullable=False)

    # RELACIONAMENTO: Diz ao SQLAlchemy que o entregador tem uma lista de pedidos
    # 'back_populates' garante que as duas tabelas se atualizem no Python automaticamente
    pedidos = relationship("Pedido", back_populates="entregador")


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    cep_origem = Column(String(9), nullable=False) # Ex: 01311-200
    cep_destino = Column(String(9), nullable=False)
    peso = Column(Float, nullable=False) # Peso em KG (ex: 4.5)
    valor = Column(Float, nullable=False) # Valor em Reais (calculado via código)

    # CHAVE ESTRANGEIRA: Guarda o ID do entregador dono deste pedido
    entregador_id = Column(Integer, ForeignKey("entregadores.id"), nullable=False)

    # Permite acessar o entregador do pedido via 'pedido.entregador'
    entregador = relationship("Entregador", back_populates="pedidos")
