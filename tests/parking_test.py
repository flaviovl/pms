import pytest
from pms.parking import Estacionamento


@pytest.fixture
def valid_park():
    return Estacionamento(
        capacidade_maxima=15,
        valor_fracao=10.00,
        valor_diaria_diurna=120.00,
        valor_evento=70.00,
        valor_mensalista=600,
        desconto_hora_cheia=0.75,
        desconto_diaria_notura=0.45,
    )


@pytest.mark.entrada_dados
@pytest.mark.estacionamento
def test_capacidade_maxima(valid_park):
    """Testa inicialização de atributo do metodo contrutor capacidade maxima"""
    assert valid_park.capacidade_maxima == 15


@pytest.mark.entrada_dados
def test_valor_fracao(valid_park):
    """Testa inicialização de atributo do metodo contrutor valor fracao"""
    assert valid_park.valor_fracao == 10.0


@pytest.mark.entrada_dados
def test_valor_diaria_diurna(valid_park):
    """Testa inicialização de atributo do metodo contrutor valor diaria diurna"""
    assert valid_park.valor_diaria_diurna == 120.00


@pytest.mark.entrada_dados
def test_valor_mensalista(valid_park):
    """Testa inicialização de atributo do metodo contrutor valor mensalista"""
    assert valid_park.valor_mensalista == 600.00


@pytest.mark.entrada_dados
def test_valor_evento(valid_park):
    """Testa inicialização de atributo do metodo contrutor valor evento"""
    assert valid_park.valor_evento == 70.00


@pytest.mark.estacionamento
def test_valor_hora_cheia(valid_park):
    """
    Testa calculo do valor hora cheia = 25% desconto
    do valor de 4 x valor de fracao(15min).
    """
    assert valid_park.valor_hora_cheia == 30
