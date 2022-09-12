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
