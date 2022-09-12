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


# ==============================================================================


@pytest.mark.funcional
@pytest.mark.registro_entrada_saida
def test_registrar_entrada_um_veiculo(park):
    placa = "LUV1530"
    vagas_ocupadas_inicio = park.get_vagas_ocupadas
    park.registrar_entrada_veiculo(placa, datetime(2022, 9, 3, 12, 0))
    vagas_ocupadas_fim = park.get_vagas_ocupadas

    assert vagas_ocupadas_fim == vagas_ocupadas_inicio + 1
    assert placa in park.registro_entrada_ativo


# ==============================================================================
@pytest.mark.funcional
@pytest.mark.registro_entrada_saida
def test_registrar_saida_um_veiculo(park):
    placa = "LUV1530"
    vagas_ocupadas_inicio = park.get_vagas_ocupadas

    park.registrar_entrada_veiculo(placa, datetime(2022, 9, 3, 12, 0))
    park.registrar_saida_veiculo(placa, datetime(2022, 9, 3, 18, 0))
    vagas_ocupadas_fim = park.get_vagas_ocupadas

    assert vagas_ocupadas_inicio == vagas_ocupadas_fim
    assert placa not in park.registro_entrada_ativo
    assert placa in park.registro_saida


# ==============================================================================

placa = [
    "HPR1040",
    "JEE1240",
    "LUV1530",
]


@pytest.mark.funcional
@pytest.mark.registro_entrada_saida
@pytest.mark.parametrize("placa", placa)
def test_registrar_veiculo_mensalista(park, placa):
    park.registrar_veiculos_mensalista(placa)
    assert placa in park.registro_mensalista


@pytest.mark.funcional
@pytest.mark.registro_entrada_saida
@pytest.mark.parametrize("placa", placa)
def test_registrar_veiculo_evento(park, placa):
    park.registrar_evento(placa)
    assert placa in park.registro_evento


# ==============================================================================
