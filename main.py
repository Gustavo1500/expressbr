from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session
from database import engine, get_db
import models
import re
import security

# Criar tabelas
models.Base.metadata.create_all(bind=engine)

# Pydantic Entragador Schema
class EntregadorCriar(BaseModel):
    nome: str
    email: str
    cnpj: str
    veiculo: models.TipoVeiculo
    senha: str

    @field_validator('cnpj')
    @classmethod
    def validar_cpf(cls, v: str):
        cnpj_limpo = re.sub(r'[^0-9]', '', v)
        if len(cnpj_limpo) != 14:
            raise ValueError('O CNPJ deve conter exatamente 14 números.')
        return cnpj_limpo

class PedidoCriarSchema(BaseModel):
    cep_origem: str
    cep_destino: str
    peso: float

    # Validador de CEP
    @field_validator('cep_origem', 'cep_destino')
    @classmethod
    def validar_cep(cls, v: str):
        cep_limpo = v.strip()
        if not re.match(r"^\d{5}-?\d{3}$", cep_limpo):
            raise ValueError('CEP inválido: Use o formato XXXXX-XXX ou apenas números.')
        return cep_limpo

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
    
    # Verificar se usuário já existe na DB
    usuario_existente = db.query(models.Entregador).filter(
        (models.Entregador.email == usuario.email) | (models.Entregador.cnpj == usuario.cnpj)
    ).first()

    if usuario_existente:
        raise HTTPException(status_code=400, detail="Email ou CNPJ já cadastrados.")
    
    # Criptografar senha
    senha_criptografada = security.get_password_hash(usuario.senha)

    novo_usuario = models.Entregador(
        nome=usuario.nome,
        email=usuario.email,
        cnpj=usuario.cnpj,
        veiculo=usuario.veiculo,
        senha_hash=senha_criptografada
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return {
        "mensagem": "Usuário criado com sucesso!"
        }

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
    ):

    usuario = db.query(models.Entregador).filter(models.Entregador.email == form_data.username).first()

    if not usuario or not security.verify_password(form_data.password, usuario.senha_hash):
        raise HTTPException(
            status_code=401,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token = security.criar_token_acesso(data={"sub": usuario.email})

    return {"access_token": access_token, "token_type": "bearer"}


def get_usuario_atual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    exception_silenciosa = HTTPException(
        status_code=401,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decodificar o Token
        payload = security.jwt.decode(
            token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise exception_silenciosa
    except Exception:
        raise exception_silenciosa

    # Buscar o usuário do token no banco de dados
    usuario = db.query(models.Entregador).filter(models.Entregador.email == email).first()
    
    if usuario is None:
        raise exception_silenciosa
        
    return usuario

@app.post("/criarpedidos")
def create_pedidos(
    pedido_dados: PedidoCriarSchema, 
    db: Session = Depends(get_db),
    entregador_logado: models.Entregador = Depends(get_usuario_atual)
    ):
    """
    Se logado permitir entregador de criar pedido,
    caso contrário, bloquear o seu acesso
    """
    
    # Calcula o valor baseado no peso
    valor_calculado = 10.0 + (pedido_dados.peso * 2.5)

    novo_pedido = models.Pedido(
        cep_origem=pedido_dados.cep_origem,
        cep_destino=pedido_dados.cep_destino,
        peso=pedido_dados.peso,
        valor=valor_calculado,
        entregador_id=entregador_logado.id # Atrela o ID do entregador logado ao pedido
    )

    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)

    return {"mensagem": f"Pedido criado, {entregador_logado.nome}. Bom trabalho!"}

@app.get("/pedidos")
def get_pedidos(
    entregador_logado: models.Entregador = Depends(get_usuario_atual)
    ):
    """
    Se logado mostrar todos os pedidos no nome do usuário,
    caso contrário, bloquear o seu acesso
    """
    pedidos = entregador_logado.pedidos

    return {"pedidos": pedidos}
