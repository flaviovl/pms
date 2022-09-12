from datetime import datetime

import pytest
from pms.exceptions import (
    DataHoraInvalidaException,
    DescricaoEmBrancoException,
    EstacionamentoCheioException,
    EstacionamentoVazioException,
    ValorAcessoInvalidoException,
    VeiculoExisteRegistroException,
    VeiculoNaoRegistrado,
)
from pms.parking import Estacionamento

# ===========================================================================================


@pytest.mark.excecao
@pytest.mark.entrada_dados
def test_execao_valor_em_branco_capacidade_maxima():
    with pytest.raises(
        DescricaoEmBrancoException, match="Capacidade maxima não pode ser em branco"
    ):
        park_invalid = Estacionamento(None, 10.00, 120.00, 70.00, 600, 0.75, 0.45)


# ===========================================================================================
@pytest.mark.excecao
@pytest.mark.entrada_dados
def test_execao_valor_invalido_capacidade_maxima():
    with pytest.raises(
        ValorAcessoInvalidoException, match="Somente numeros inteiros são aceitos"
    ):
        park_invalid = Estacionamento(-5, 10.00, 120.00, 70.00, 600, 0.75, 0.45)


# ===========================================================================================
@pytest.mark.excecao
@pytest.mark.entrada_dados
def test_execao_valor_fracao_em_branco():
    with pytest.raises(
        DescricaoEmBrancoException, match="Valor fracao não pode ser em branco"
    ):
        park_invalid = Estacionamento(100, None, 120.00, 70.00, 600, 0.75, 0.45)


# ===========================================================================================
@pytest.mark.excecao
@pytest.mark.entrada_dados
def test_execao_valor_fracao_invalido():
    with pytest.raises(
        ValorAcessoInvalidoException, match="Somente numeros positivos são aceitos"
    ):
        park_invalid = Estacionamento(100, -5.00, 120.00, 70.00, 600, 0.75, 0.45)


# ===========================================================================================
@pytest.mark.excecao
@pytest.mark.entrada_dados
def test_execao_valor_diaria_diurna_em_branco():
    with pytest.raises(
        DescricaoEmBrancoException, match="Valor diaria diurna não pode ser em branco"
    ):
        park_invalid = Estacionamento(100, 10.0, None, 70.00, 600, 0.75, 0.45)


# ===========================================================================================
@pytest.mark.excecao
@pytest.mark.entrada_dados
def test_execao_valor_diaria_diurna_invalido():
    with pytest.raises(
        ValorAcessoInvalidoException, match="Somente numeros positivos são aceitos"
    ):
        park_invalid = Estacionamento(100, 10.0, -25, 70.00, 600, 0.75, 0.45)


# ===========================================================================================
@pytest.mark.excecao
@pytest.mark.entrada_dados
def test_execao_valor_evento_em_branco():
    with pytest.raises(
        DescricaoEmBrancoException, match="Valor evento não pode ser em branco"
    ):
        park_invalid = Estacionamento(100, 10.0, 120, None, 600, 0.75, 0.45)


# ===========================================================================================
@pytest.mark.excecao
@pytest.mark.entrada_dados
def test_execao_valor_evento_invalido():
    with pytest.raises(
        ValorAcessoInvalidoException, match="Somente numeros positivos são aceitos"
    ):
        park_invalid = Estacionamento(100, 10.0, 120, -70.00, 600, 0.75, 0.45)


# ===========================================================================================
@pytest.mark.excecao
@pytest.mark.entrada_dados
def test_execao_valor_mensalista_em_branco():
    with pytest.raises(
        DescricaoEmBrancoException, match="Valor mensalista não pode ser em branco"
    ):
        park_invalid = Estacionamento(100, 10.0, 120, 70.00, None, 0.75, 0.45)


# ===========================================================================================
@pytest.mark.excecao
@pytest.mark.entrada_dados
def test_execao_valor_mensalista_invalido():
    with pytest.raises(
        ValorAcessoInvalidoException, match="Somente numeros positivos são aceitos"
    ):
        park_invalid = Estacionamento(100, 10.0, 120, 70.00, -600, 0.75, 0.45)


# ===========================================================================================
@pytest.mark.excecao
@pytest.mark.entrada_dados
def test_execao_desconto_hora_cheia_em_branco():
    with pytest.raises(
        DescricaoEmBrancoException, match="Desconto hora cheia não pode ser em branco"
    ):
        park_invalid = Estacionamento(100, 10.0, 120, 70.00, 600, None, 0.45)


# ===========================================================================================
@pytest.mark.excecao
@pytest.mark.entrada_dados
def test_execao_desconto_hora_cheia_invalido():
    with pytest.raises(
        ValorAcessoInvalidoException,
        match="Somente numeros positivos entre 0 e 1 são aceitos",
    ):
        park_invalid = Estacionamento(100, 10.0, 120, 70.00, 600, -0.75, 0.45)


# ===========================================================================================
@pytest.mark.excecao
@pytest.mark.entrada_dados
def test_execao_desconto_diaria_notura_em_branco():
    with pytest.raises(
        DescricaoEmBrancoException,
        match="Valor desconto diaria noturna não pode ser em branco",
    ):
        park_invalid = Estacionamento(100, 10.0, 120, 70.00, 600, 0.75, None)


# ===========================================================================================
@pytest.mark.excecao
@pytest.mark.entrada_dados
def test_execao_desconto_diaria_notura_invalido():
    with pytest.raises(
        ValorAcessoInvalidoException,
        match="Somente numeros positivos entre 0 e 1 são aceitos",
    ):
        park_invalid = Estacionamento(100, 10.0, 120, 70.00, 600, 0.75, 3)


# ===========================================================================================


@pytest.fixture
def park_valid():
    return Estacionamento(
        capacidade_maxima=3,
        valor_fracao=10.00,
        valor_diaria_diurna=120.00,
        valor_evento=70.00,
        valor_mensalista=600,
        desconto_hora_cheia=0.75,
        desconto_diaria_notura=0.45,
    )


# ===========================================================================================
@pytest.mark.excecao
@pytest.mark.registro_entrada_saida
def test_excecao_registrar_entrada_estacionamento_cheio(park_valid):
    """caso de teste de excecao registro de entrada veiculo com estacionamento cheio"""

    park_valid.registrar_entrada_veiculo("JEE1240", datetime(2022, 9, 2, 11, 0))
    park_valid.registrar_entrada_veiculo("HPR1040", datetime(2022, 9, 1, 10, 0))
    park_valid.registrar_entrada_veiculo("NWK7820", datetime(2022, 9, 2, 11, 0))

    assert park_valid.get_vagas_ocupadas == 3

    with pytest.raises(
        EstacionamentoCheioException, match="Estacionamento com lotação máxima"
    ):
        park_valid.registrar_entrada_veiculo("LUV1530", datetime(2022, 9, 3, 12, 0))


# ===========================================================================================
@pytest.mark.excecao
@pytest.mark.registro_entrada_saida
def test_excecao_registrar_entrada_sem_informar_placa(park_valid):
    """caso de teste de excecao registrar entrada de veiculo sem informar placa"""

    with pytest.raises(
        DescricaoEmBrancoException, match="Placa é um campos obrigatorio"
    ):
        park_valid.registrar_entrada_veiculo(None, datetime(2022, 9, 1, 10, 0))


# ===========================================================================================
@pytest.mark.excecao
@pytest.mark.registro_entrada_saida
def test_excecao_registrar_entrada_sem_informar_datahora(park_valid):
    """caso de teste de excecao registrar entrada de veiculo sem informar data e horario de entrada"""

    with pytest.raises(
        DescricaoEmBrancoException, match="Data hora é um campos obrigatorio"
    ):
        park_valid.registrar_entrada_veiculo("XPT7587", None)


# ===========================================================================================
@pytest.mark.excecao
@pytest.mark.registro_entrada_saida
def test_excecao_registrar_entrada_placa_invalida(park_valid):
    """
    Caso de teste de excecao registrar entrada de um veiculo informando uma placa inválida.
    Inclui os padrões: Antigo: 'AAA0000' e Mercosul: 'AAA0A00'
    """

    with pytest.raises(ValorAcessoInvalidoException, match="Placa invalida"):
        park_valid.registrar_entrada_veiculo("a1b153b", datetime(2022, 9, 3, 12, 0))


# ===========================================================================================
@pytest.mark.excecao
@pytest.mark.registro_entrada_saida
def test_excecao_registrar_entrada_datahora_invalida(park_valid):
    """
    Caso de teste de excecao registrar entrada de um veiculo informando uma datahora inválida.
    Tipo válido: Datetime
    Padrão: Datetime(ano, mes, dia, hora, minuto, segundo)
    """

    with pytest.raises(ValueError):
        park_valid.registrar_entrada_veiculo("AAA0A00", datetime(2022, 14, 3, 12, 0))


# ===========================================================================================
@pytest.mark.excecao
@pytest.mark.registro_entrada_saida
def test_excecao_registrar_entrada_datahora_tipo_invalido(park_valid):
    """
    Caso de teste de excecao registrar entrada de um veiculo informando uma data/hora tipo inválido.
    Tipo válido: Datetime
    Padrão: Datetime(ano, mes, dia, hora, minuto, segundo)
    """

    with pytest.raises(DataHoraInvalidaException, match="Formato data/hora inválido"):
        park_valid.registrar_entrada_veiculo("AAA0A00", "‘01/03/2018 12:30’")


# ===========================================================================================
@pytest.mark.excecao
@pytest.mark.registro_entrada_saida
def test_excecao_registrar_saida_datahora_menor_entrada(park_valid):
    """
    Caso de teste de excecao registrar saida de um veiculo informando uma data/hora menor ou
    que a data/hora de entrada.
    """
    park_valid.registrar_entrada_veiculo("LUV1A30", datetime(2022, 9, 3, 18, 0))

    with pytest.raises(
        DataHoraInvalidaException, match="Data Hora saída menor ou igual a entrada"
    ):
        park_valid.registrar_saida_veiculo("LUV1A30", datetime(2022, 9, 3, 18, 0))


# ===========================================================================================--
@pytest.mark.excecao
@pytest.mark.registro_entrada_saida
def test_registrar_saida_levanta_excecao_estacionamento_vazio(park_valid):
    """Caso de teste de excecão registrar saída de um veiculo com estacionamento vazio"""

    assert park_valid.get_vagas_ocupadas == 0
    with pytest.raises(EstacionamentoVazioException, match="Estacionamento vazio"):
        park_valid.registrar_saida_veiculo("LUV1530", datetime(2022, 9, 3, 18, 0))


# ===========================================================================================
@pytest.mark.excecao
@pytest.mark.registro_entrada_saida
def test_registrar_saida_levanta_excecao_veiculo_nao_regitrado(park_valid):
    """Caso de teste levantar excecao em saida de veiculo que não tenha sido registrado sua entrada"""

    park_valid.registrar_entrada_veiculo("NWK7820", datetime(2022, 9, 2, 11, 0))
    assert park_valid.get_vagas_ocupadas == 1

    with pytest.raises(
        VeiculoNaoRegistrado, match="A entrada do veiculo nao foi registrada"
    ):
        park_valid.registrar_saida_veiculo("LUV1530", datetime(2022, 9, 3, 18, 0))


# ===========================================================================================
