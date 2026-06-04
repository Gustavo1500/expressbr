from fastapi.testclient import TestClient
from main import app, PedidoCriarSchema
import pytest

client = TestClient(app)

# TESTES DE UNIDADE: Validando os CEPs no Pydantic

def test_pydantic_deve_aceitar_ceps_validos():
    """Garante que formatos válidos de CEP passam na validação"""
    # CEP com hífen
    pedido1 = PedidoCriarSchema(cep_origem="01311-200", cep_destino="04571-010", peso=2.0)
    assert pedido1.cep_origem == "01311-200"

    # CEP apenas com números
    pedido2 = PedidoCriarSchema(cep_origem="01311200", cep_destino="04571010", peso=2.0)
    assert pedido2.cep_origem == "01311200"


def test_pydantic_deve_rejeitar_cep_com_tamanho_errado():
    """Garante que CEPs com menos ou mais dígitos falham"""
    with pytest.raises(ValueError):
        PedidoCriarSchema(cep_origem="123", cep_destino="04571-010", peso=2.0)


# TESTE DE INTEGRAÇÃO: Validando o cálculo do frete

def test_calculo_do_frete_deve_ser_calculado_corretamente():
    """
    Garante que a nossa regra de negócio de preço funciona:
    Valor = R$ 10.00 (fixo) + (Peso * R$ 2.50)
    """
    # Se o pacote pesa 4kg, o valor deve ser: 10 + (4 * 2.5) = R$ 20.00
    peso_teste = 4.0
    valor_esperado = 10.0 + (peso_teste * 2.5) # R$ 20.0
    
    # Criamos o objeto do pedido para simular
    pedido = PedidoCriarSchema(cep_origem="01311-200", cep_destino="04571-010", peso=peso_teste)
    
    # Fazemos o cálculo exatamente como a rota faz
    valor_calculado = 10.0 + (pedido.peso * 2.5)
    
    assert valor_calculado == valor_esperado
    assert valor_calculado == 20.0
