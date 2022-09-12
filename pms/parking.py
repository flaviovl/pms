import re
from datetime import date, datetime, time
from enum import Enum
from numbers import Number

from .exceptions import (
    DataHoraInvalidaException,
    DescricaoEmBrancoException,
    EstacionamentoCheioException,
    EstacionamentoVazioException,
    ValorAcessoInvalidoException,
    VeiculoExisteRegistroException,
    VeiculoNaoRegistrado,
)


class ParkingTicketStatus(Enum):
    ROTATIVO, MENSALISTA, EVENTO, DIARIA = 1, 2, 3, 4


class Estacionamento:
    __desconto_seguradora: float = 0.90
    __percetual_contratante: float = 0.50

    def __init__(
        self,
        capacidade_maxima: int,
        valor_fracao: float,
        valor_diaria_diurna: float,
        valor_evento: float,
        valor_mensalista: float,
        desconto_hora_cheia: float,
        desconto_diaria_notura: float,
    ):
        self.__capacidade_maxima = capacidade_maxima
        self.__valor_fracao = valor_fracao
        self.__valor_diaria_diurna = valor_diaria_diurna
        self.__desconto_hora_cheia = desconto_hora_cheia
        self.__desconto_diaria_notura = desconto_diaria_notura
        self.__valor_mensalista = valor_mensalista
        self.__valor_evento = valor_evento
        self.__contador_veiculos: int = 0
        self.__registro_entrada_ativo: dict = {}
        self.__registro_saida: dict = {}
        self.__registro_eventos: list = []
        self.__registro_mensalistas: list = []
        self.__horario_abertura: time = time(8, 0)
        self.__fechamento: time = time(23, 59, 59)

    #  ===============================================================================
    # Getters and Setter (property)

    @property
    def capacidade_maxima(self):
        return self._capacidade_maxima

    @capacidade_maxima.setter
    def __capacidade_maxima(self, valor) -> int:
        if valor is None:
            raise DescricaoEmBrancoException("Capacidade maxima não pode ser em branco")

        if valor <= 0 or not isinstance(valor, int):
            raise ValorAcessoInvalidoException("Somente numeros inteiros são aceitos")

        self._capacidade_maxima = valor

    @property
    def valor_fracao(self):
        return self._valor_fracao

    @valor_fracao.setter
    def __valor_fracao(self, valor) -> float:
        if valor is None:
            raise DescricaoEmBrancoException("Valor fracao não pode ser em branco")

        if valor < 0 or not isinstance(valor, Number):
            raise ValorAcessoInvalidoException("Somente numeros positivos são aceitos")

        self._valor_fracao = valor

    @property
    def valor_diaria_diurna(self):
        return self._valor_diaria_diurna

    @valor_diaria_diurna.setter
    def __valor_diaria_diurna(self, valor) -> float:
        if valor is None:
            raise DescricaoEmBrancoException(
                "Valor diaria diurna não pode ser em branco"
            )

        if valor < 0 or not isinstance(valor, Number):
            raise ValorAcessoInvalidoException("Somente numeros positivos são aceitos")

        self._valor_diaria_diurna = valor

    @property
    def valor_evento(self):
        return self._valor_evento

    @valor_evento.setter
    def __valor_evento(self, valor) -> float:
        if valor is None:
            raise DescricaoEmBrancoException("Valor evento não pode ser em branco")

        if valor < 0 or not isinstance(valor, Number):
            raise ValorAcessoInvalidoException("Somente numeros positivos são aceitos")

        self._valor_evento = valor

    @property
    def valor_mensalista(self):
        return self._valor_mensalista

    @valor_mensalista.setter
    def __valor_mensalista(self, valor) -> float:
        if valor is None:
            raise DescricaoEmBrancoException("Valor mensalista não pode ser em branco")

        if valor < 0 or not isinstance(valor, Number):
            raise ValorAcessoInvalidoException("Somente numeros positivos são aceitos")

        self._valor_mensalista = valor

    @property
    def desconto_hora_cheia(self):
        return self._desconto_hora_cheia

    @desconto_hora_cheia.setter
    def __desconto_hora_cheia(self, valor):
        if valor is None:
            raise DescricaoEmBrancoException(
                "Desconto hora cheia não pode ser em branco"
            )

        if valor < 0 or valor > 1 or (not isinstance(valor, Number)):
            raise ValorAcessoInvalidoException(
                "Somente numeros positivos entre 0 e 1 são aceitos"
            )

        self._desconto_hora_cheia = valor

    @property
    def desconto_diaria_notura(self):
        return self._desconto_diaria_notura

    @desconto_diaria_notura.setter
    def __desconto_diaria_notura(self, valor):
        if valor is None:
            raise DescricaoEmBrancoException(
                "Valor desconto diaria noturna não pode ser em branco"
            )

        if valor < 0 or valor > 1 or (not isinstance(valor, Number)):
            raise ValorAcessoInvalidoException(
                "Somente numeros positivos entre 0 e 1 são aceitos"
            )

        self._desconto_diaria_notura = valor

    # ===============================================================================

    @property
    def valor_hora_cheia(self) -> float:
        return 30
