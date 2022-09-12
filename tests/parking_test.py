from datetime import datetime

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


@pytest.mark.entrada_dados
def test_desconto_hora_cheia(valid_park):
    """Testa atributo desconto hora cheia"""
    assert valid_park.desconto_hora_cheia == 0.75


@pytest.mark.entrada_dados
def test_desconto_diaria_notura(valid_park):
    """Testa atributo desconto diaria noturna"""
    assert valid_park.desconto_diaria_notura == 0.45


def test_valor_diaria_noturna(valid_park):
    """
    Testa calculo do valor da diaria notura = 55%
    de desconto da diaria diurna.
    """
    assert valid_park.valor_diaria_noturna == 54


@pytest.mark.estacionamento
def test_vagas_livres(valid_park):
    """Testa atributo vagas livres"""
    assert valid_park.get_vagas_livres == 15


@pytest.mark.estacionamento
def test_get_vagas_ocupadas(valid_park):
    """Testa o numero de vagas ocupadas"""
    assert valid_park.get_vagas_ocupadas == 0


@pytest.mark.estacionamento
def test_valor_hora_cheia(valid_park):
    """
    Testa calculo do valor hora cheia = 25% desconto
    do valor de 4 x valor de fracao(15min).
    """
    assert valid_park.valor_hora_cheia == 30


@pytest.mark.estacionamento
def test_get_esta_cheio(valid_park):
    """
    Testa se o numero de veiulos estacionado
    é menor que a capacidade total
    """
    assert valid_park.get_esta_cheio == False


# ==============================================================================


@pytest.mark.funcional
@pytest.mark.registro_entrada_saida
def test_registrar_entrada_um_veiculo(valid_park):
    placa = "LUV1530"
    vagas_ocupadas_inicio = valid_park.get_vagas_ocupadas
    valid_park.registrar_entrada_veiculo(placa, datetime(2022, 9, 3, 12, 0))
    vagas_ocupadas_fim = valid_park.get_vagas_ocupadas

    assert vagas_ocupadas_fim == vagas_ocupadas_inicio + 1
    assert placa in valid_park.registro_entrada_ativo


# ==============================================================================
@pytest.mark.funcional
@pytest.mark.registro_entrada_saida
def test_registrar_saida_um_veiculo(valid_park):
    placa = "LUV1530"
    vagas_ocupadas_inicio = valid_park.get_vagas_ocupadas

    valid_park.registrar_entrada_veiculo(placa, datetime(2022, 9, 3, 12, 0))
    valid_park.registrar_saida_veiculo(placa, datetime(2022, 9, 3, 18, 0))
    vagas_ocupadas_fim = valid_park.get_vagas_ocupadas

    assert vagas_ocupadas_inicio == vagas_ocupadas_fim
    assert placa not in valid_park.registro_entrada_ativo
    assert placa in valid_park.registro_saida


# ==============================================================================

placa = [
    "HPR1040",
    "JEE1240",
    "LUV1530",
]


@pytest.mark.funcional
@pytest.mark.registro_entrada_saida
@pytest.mark.parametrize("placa", placa)
def test_registrar_veiculo_mensalista(valid_park, placa):
    valid_park.registrar_veiculos_mensalista(placa)
    assert placa in valid_park.registro_mensalista


@pytest.mark.funcional
@pytest.mark.registro_entrada_saida
@pytest.mark.parametrize("placa", placa)
def test_registrar_veiculo_evento(valid_park, placa):
    valid_park.registrar_evento(placa)
    assert placa in valid_park.registro_evento


# ==============================================================================


base_teste_fracao = [
    (  # 15min = 1 fração = 10.0
        "HPR1040",
        datetime(2022, 9, 10, 12, 0),
        datetime(2022, 9, 10, 12, 15),
        10.0,
    ),
    (  # 30min = 2 fração = 20.0
        "JEE1240",
        datetime(2022, 9, 10, 13, 0),
        datetime(2022, 9, 10, 13, 30),
        20.0,
    ),
    (  # 45min = 3 fração = 30.0
        "LUV1530",
        datetime(2022, 9, 10, 14, 0),
        datetime(2022, 9, 10, 14, 45),
        30.0,
    ),
]


@pytest.mark.funcional
@pytest.mark.valor_acesso
@pytest.mark.parametrize(
    "placa, entrada, saida, resultado",
    base_teste_fracao,
    ids=[
        "15 min",
        "30 min",
        "45 min",
    ],
)
def test_calculo_valor_acesso_fracao(valid_park, placa, entrada, saida, resultado):

    valid_park.registrar_entrada_veiculo(placa, entrada)
    valid_park.registrar_saida_veiculo(placa, saida)

    custo = valid_park.registro_saida.get(placa).get("custo")
    assert custo == resultado


# ==============================================================================
base_teste_hora_cheia = [
    (  # 1 hora = 4 frações * desconto = 30.0
        "HPR1040",
        datetime(2022, 9, 10, 12, 0),
        datetime(2022, 9, 10, 13, 0),
        30.0,
    ),
    (  # 4 horas = 36 frações * desconto = 120.0
        "JEE1240",
        datetime(2022, 9, 10, 13, 0),
        datetime(2022, 9, 10, 17, 0),
        120.0,
    ),
    (  # 8 horas = 32 frações * desconto = 240.0
        "LUV1530",
        datetime(2022, 9, 10, 14, 0),
        datetime(2022, 9, 10, 22, 0),
        240.0,
    ),
]


@pytest.mark.funcional
@pytest.mark.valor_acesso
@pytest.mark.parametrize(
    "placa, entrada, saida, resultado",
    base_teste_hora_cheia,
    ids=[
        "1 Hora",
        "4 Horas",
        "9 Horas",
    ],
)
def test_calculo_valor_acesso_hora_cheia(valid_park, placa, entrada, saida, resultado):
    valid_park.registrar_entrada_veiculo(placa, entrada)
    valid_park.registrar_saida_veiculo(placa, saida)

    custo = valid_park.registro_saida.get(placa).get("custo")
    assert custo == resultado


# ==============================================================================
base_teste_diaria_diurna = [
    (  # 9 hora = 36 frações >= 36 = 120.0
        "HPR1040",
        datetime(2022, 9, 10, 8, 0),
        datetime(2022, 9, 10, 17, 0),
        120.0,
    ),
    (  # 10 horas = 40 frações >= 36 = 120.0
        "JEE1240",
        datetime(2022, 9, 10, 9, 0),
        datetime(2022, 9, 10, 19, 0),
        120.0,
    ),
    (  # 10 horas = 48 frações >=36 = 120.0
        "LUV1530",
        datetime(2022, 9, 10, 10, 0),
        datetime(2022, 9, 10, 22, 0),
        120.0,
    ),
]


@pytest.mark.funcional
@pytest.mark.valor_acesso
@pytest.mark.parametrize(
    "placa, entrada, saida, resultado",
    base_teste_hora_cheia,
    ids=[
        "9  Horas",
        "10 Horas",
        "12 Horas",
    ],
)
def test_calculo_valor_acesso_diaria_diurna(
    valid_park, placa, entrada, saida, resultado
):
    valid_park.registrar_entrada_veiculo(placa, entrada)
    valid_park.registrar_saida_veiculo(placa, saida)

    custo = valid_park.registro_saida.get(placa).get("custo")
    assert custo == resultado


# ==============================================================================
# entrada após 21:00hs, retirada antes 7:00hs
# Horario fechamento 00:00 (nao entra mais diária noturna)

base_teste_diaria_noturna = [
    (
        "HPR1040",
        datetime(2022, 9, 10, 21, 42),  # entrada 21:42 D
        datetime(2022, 9, 11, 7, 20),  # saida   07:20 D+1
        54.0,
    ),
    (
        "JEE1240",
        datetime(2022, 9, 8, 22, 0),  # entrada 22:00 D
        datetime(2022, 9, 9, 7, 55),  # saida   07:55 D+1
        54.00,
    ),
    (
        "LUV1530",
        datetime(2022, 9, 10, 23, 0),  # entrada 23:00 D
        datetime(2022, 9, 11, 6, 15),  # saida   06:15 D+1
        54.0,
    ),
]


@pytest.mark.funcional
@pytest.mark.valor_acesso
@pytest.mark.parametrize(
    "placa, entrada, saida, resultado",
    base_teste_diaria_noturna,
    ids=[
        ">21H | <8h",
        ">22H | <8h",
        ">23H | <7h",
    ],
)
def test_calculo_valor_acesso_diaria_noturna(
    valid_park, placa, entrada, saida, resultado
):

    valid_park.registrar_entrada_veiculo(placa, entrada)
    valid_park.registrar_saida_veiculo(placa, saida)

    custo = valid_park.registro_saida.get(placa).get("custo")
    assert custo == resultado


# ==============================================================================

base_teste_mensalista_evento = [
    (  # 30min - Fracão
        "HEE2240",
        datetime(2022, 9, 10, 13, 0),
        datetime(2022, 9, 10, 13, 30),
    ),
    (  # 1 hora - Hora Cheia
        "RPX1A40",
        datetime(2022, 9, 10, 12, 0),
        datetime(2022, 9, 10, 13, 0),
    ),
    (  # 12 horas - Diaria Diura
        "VIU1530",
        datetime(2022, 9, 10, 10, 0),
        datetime(2022, 9, 10, 22, 0),
    ),
    (  # Diaria Noturna
        "XHY1578",
        datetime(2022, 9, 8, 22, 0),  # entrada 22:00 D
        datetime(2022, 9, 9, 7, 55),  # saida   07:55 D+1
    ),
]


@pytest.mark.funcional
@pytest.mark.valor_acesso
@pytest.mark.parametrize(
    "placa, entrada, saida",
    base_teste_mensalista_evento,
    ids=[
        "Fracao",
        "Hora Cheia",
        "Diaria Diurna",
        "Diaria noturna",
    ],
)
def test_calcular_valor_acesso_mensalista(valid_park, placa, entrada, saida):
    """
    Mensalista não gera custo por acesso de nenhum tipo.
    Valor mensal(unico) não fica registrado na tabela de acessos.
    """
    livre = 0
    valid_park.registrar_veiculos_mensalista(placa)
    valid_park.registrar_entrada_veiculo(placa, entrada)
    valid_park.registrar_saida_veiculo(placa, saida)

    custo = valid_park.registro_saida.get(placa).get("custo")

    assert placa in valid_park.registro_mensalista
    assert custo == livre


# ==============================================================================


@pytest.mark.funcional
@pytest.mark.valor_acesso
@pytest.mark.parametrize(
    "placa, entrada, saida",
    base_teste_mensalista_evento,
    ids=[
        "Fracao",
        "Hora Cheia",
        "Diaria Diurna",
        "Diaria noturna",
    ],
)
def test_calcular_valor_acesso_evento(valid_park, placa, entrada, saida):

    valid_park.registrar_evento(placa)
    valid_park.registrar_entrada_veiculo(placa, entrada)
    valid_park.registrar_saida_veiculo(placa, saida)

    custo = valid_park.registro_saida.get(placa).get("custo")

    assert placa in valid_park.registro_evento
    assert custo == valid_park.valor_evento


# ==============================================================================
@pytest.fixture
def setup_calcular_total():

    park_fga = Estacionamento(15, 10.00, 120.00, 70.00, 600, 0.75, 0.45)

    # Registrar dois veiculos como mensalista
    park_fga.registrar_veiculos_mensalista("MEN1040")
    park_fga.registrar_veiculos_mensalista("MEN5422")

    # Registrar dois veiculos em um evento
    park_fga.registrar_evento("EVE1550")
    park_fga.registrar_evento("EVE2059")

    # Registrar acessos de mensalistas (custo acesso == 0)
    park_fga.registrar_entrada_veiculo("MEN1040", datetime(2022, 9, 11, 10, 30))
    park_fga.registrar_saida_veiculo("MEN1040", datetime(2022, 9, 11, 15, 20))
    park_fga.registrar_entrada_veiculo("MEN5422", datetime(2022, 9, 11, 11, 40))
    park_fga.registrar_saida_veiculo("MEN5422", datetime(2022, 9, 11, 18, 20))
    park_fga.registrar_entrada_veiculo("MEN1040", datetime(2022, 9, 11, 19, 15))
    park_fga.registrar_saida_veiculo("MEN1040", datetime(2022, 9, 11, 20, 30))

    # Registrar acessos por eventos (custo == valor fixo)
    park_fga.registrar_entrada_veiculo("EVE1550", datetime(2022, 9, 11, 12, 10))
    park_fga.registrar_saida_veiculo("EVE1550", datetime(2022, 9, 11, 18, 20))
    park_fga.registrar_entrada_veiculo("EVE2059", datetime(2022, 9, 11, 10, 30))
    park_fga.registrar_saida_veiculo("EVE2059", datetime(2022, 9, 11, 22, 20))

    # Registrar acesso por Fração
    park_fga.registrar_entrada_veiculo("HPR1040", datetime(2022, 9, 11, 10, 15))
    park_fga.registrar_saida_veiculo("HPR1040", datetime(2022, 9, 11, 10, 30))
    park_fga.registrar_entrada_veiculo("JEE1240", datetime(2022, 9, 11, 11, 10))
    park_fga.registrar_saida_veiculo("JEE1240", datetime(2022, 9, 11, 11, 40))
    park_fga.registrar_entrada_veiculo("LUV1530", datetime(2022, 9, 11, 15, 14))
    park_fga.registrar_saida_veiculo("LUV1530", datetime(2022, 9, 11, 15, 59))

    # Registrar acesso por Hora
    park_fga.registrar_entrada_veiculo("JPX1815", datetime(2022, 9, 11, 18, 0))
    park_fga.registrar_saida_veiculo("JPX1815", datetime(2022, 9, 11, 20, 0))

    # Registrar acesso por Diaria Diurna
    park_fga.registrar_entrada_veiculo("RPX1A40", datetime(2022, 9, 11, 10, 0))
    park_fga.registrar_saida_veiculo("RPX1A40", datetime(2022, 9, 11, 22, 0))

    # Registrar acesso por Diaria Noturna
    park_fga.registrar_entrada_veiculo("VIU1530", datetime(2022, 9, 11, 23, 15))
    park_fga.registrar_saida_veiculo("VIU1530", datetime(2022, 9, 11, 5, 50))

    return park_fga


# ==============================================================================
@pytest.mark.apurado
def test_acumulado_valor_apurado(setup_calcular_total):
    assert setup_calcular_total.get_total_apurado == 1775.0


@pytest.mark.apurado
def test_acumulado_valor_apurado_contratante(setup_calcular_total):
    assert setup_calcular_total.get_total_apurado_contratante == 887.50


# ==============================================================================
