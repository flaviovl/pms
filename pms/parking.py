import re
from datetime import date, datetime, time
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
        self.__bilhetes_ativos = {}

    #  ===============================================================================
    @classmethod
    def alterar_desconto_seguradora(cls, percentual: float) -> None:
        """
        Metodo responsavel em alterar o percentual do desconto da parcecia
        com seguradoras. Valor padrão é 10% de desconto;

        Obs: Valor do percentual é o mesmo para todos os contratantes.
        Desconto da Seguradora é padrão para todos os estacionamentos
        """
        if not isinstance(percentual, Number):
            raise TypeError("Não é um numero")
        cls.__desconto_seguradora = percentual

    @classmethod
    def alterar_percentual_contratante(cls, percentual: float) -> None:
        """
        Metodo responsavel em alterar o percentual do contratante.
        Valor padrão do contratante = 50%;

        Obs: Valor do percentual é o mesmo para todos os contratantes.
        """
        if not isinstance(percentual, Number):
            raise TypeError("Não é um numero")
        cls.__percetual_contratante = percentual

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
    # Getters computed methods

    @property
    def valor_hora_cheia(self) -> float:
        """
        Metodo responsavel em calcular o valor cobrado por hora.
        Valor da Hora é um percentual de quatro vezes o valor da
        fração de 15min.

        Returns:
            float: valor da hora
        """
        return (self.__valor_fracao * 4) * self.__desconto_hora_cheia

    @property
    def valor_diaria_noturna(self) -> float:
        """
        Metodo responsavel por calcular o valor da diária noturna.
        Valor da diária notura é um percentual da diaria diurna.

        Returns:
            float: valor diária noturna
        """
        return self.__valor_diaria_diurna * self.__desconto_diaria_notura

    @property
    def get_vagas_livres(self) -> int:
        """
        Metodo responsavel em calcular o numero de vagas livres.

        Returns:
            int: numero de vagas livres
        """
        return self.__capacidade_maxima - self.__contador_veiculos

    @property
    def get_vagas_ocupadas(self) -> int:
        """
        Metodo responsavel retornar vagas ocupadas

        Returns:
            int: numero de vagas ocupadas
        """
        return self.__contador_veiculos

    @property
    def registro_entrada_ativo(self) -> dict:
        """
        Metodo responsavel retornar veiculos ativos no
        registro do estacionamento

        Returns:
            dict: veiculos ativos
        """
        return self.__registro_entrada_ativo

    @property
    def registro_saida(self) -> dict:
        """
        Metodo responsavel retornar registro de veiculos n
        o controle saisa

        Returns:
            dict: veiculos ativos
        """
        return self.__registro_saida

    @property
    def registro_mensalista(self) -> list:
        """
        Metodo responsavel retornar lista dos veiculos
        cadastrados como mensalista.

        Returns:
            list: veiculos mensalista
        """
        return self.__registro_mensalistas

    @property
    def registro_evento(self) -> list:
        """
        Metodo responsavel retornar lista dos veiculos
        cadastrados em um evento.

        Returns:
            list: veiculos cadastrados em evento
        """
        return self.__registro_eventos

    @property
    def get_esta_cheio(self) -> bool:
        return self.__contador_veiculos >= self.__capacidade_maxima

    # =================================================================================

    def registrar_veiculos_mensalista(self, placa: str):
        """
        Metodo responsavel por adicionar um novo veiculo no registro de mensalista

        Args:
            placa (str): placa do veiculo
        """
        self.__registro_mensalistas.append(placa)

    def registrar_evento(self, placa: str):
        """
        Metodo responsavel por adicionar um novo veiculo no registro de um evento

        Args:
            placa (str): placa do veiculo
        """
        self.__registro_eventos.append(placa)

    # =================================================================================
    def registrar_entrada_veiculo(
        self,
        placa: str,
        data_hora_entrada: datetime,
        desc_seguradora: bool = False,
    ):
        if self.get_esta_cheio:
            raise EstacionamentoCheioException("Estacionamento com lotação máxima")

        self.e_valido_dados_entrada(placa, data_hora_entrada)

        tipo_acesso = self.buscar_tipo_acesso(placa)

        self.__contador_veiculos += 1
        self.__registro_entrada_ativo[placa] = {
            "dt_entrada": data_hora_entrada,
            "desc_seguradora": desc_seguradora,
            "tipo_acesso": tipo_acesso,
        }

    # ---------------------------------------------------------------------------------

    def e_valido_dados_entrada(self, placa: str, data_hora_entrada: datetime):
        """Validar os dados de entrada de um veículo no estacionamento"""

        if not placa:
            raise DescricaoEmBrancoException("Placa é um campos obrigatorio")

        if not data_hora_entrada:
            raise DescricaoEmBrancoException("Data hora é um campos obrigatorio")

        # Placa Válida padrão Mercosul = 'AAA0A00'
        if not (re.match("[A-Z]{3}[0-9][0-9A-Z][0-9]{2}", placa)):
            raise ValorAcessoInvalidoException("Placa invalida")

        if not isinstance(data_hora_entrada, datetime):
            raise DataHoraInvalidaException("Formato data/hora inválido")

    # ---------------------------------------------------------------------------------
    def buscar_tipo_acesso(self, placa: str) -> str:
        if placa in self.__registro_mensalistas:
            return "MENSALISTA"
        elif placa in self.__registro_eventos:
            return "EVENTO"
        else:
            return "ROTATIVO"

    # =================================================================================
    def registrar_saida_veiculo(self, placa: str, data_hora_saida: datetime):

        if self.__contador_veiculos <= 0:
            raise EstacionamentoVazioException("Estacionamento vazio")

        self.e_valido_dados_saida(placa, data_hora_saida)

        veiculo = self.__registro_entrada_ativo[placa]
        data_hora_entrada = veiculo["dt_entrada"]
        duracao_min = self.calcular_duracao_min(data_hora_entrada, data_hora_saida)
        custo = self.computar_custo(veiculo, data_hora_saida)

        self.__contador_veiculos -= 1
        self.__registro_entrada_ativo.pop(placa)
        self.__registro_saida[placa] = {
            "entrada": data_hora_entrada,
            "saida": data_hora_saida,
            "duracao": duracao_min,
            "custo": custo,
        }

    # ------------------------------------------------------------------------------------

    def e_valido_dados_saida(self, placa: str, data_hora_saida: datetime):
        """Validar os dados de entrada de um veículo no estacionamento"""
        if not placa:
            raise DescricaoEmBrancoException("Placa é um campos obrigatorio")

        if not data_hora_saida:
            raise DescricaoEmBrancoException("Data hora é um campos obrigatorio")

        if not (re.match("[A-Z]{3}[0-9][0-9A-Z][0-9]{2}", placa)):
            raise ValorAcessoInvalidoException("Placa invalida")

        if not isinstance(data_hora_saida, datetime):
            raise DataHoraInvalidaException("Formato data/hora inválido")

        if placa not in self.__registro_entrada_ativo:
            raise VeiculoNaoRegistrado("A entrada do veiculo nao foi registrada")

    # ------------------------------------------------------------------------------------
    def calcular_duracao_min(
        self, data_hora_entrada: datetime, data_hora_saida: datetime
    ):
        duracao_sec = (data_hora_saida - data_hora_entrada).seconds

        return duracao_sec / 60

    # ------------------------------------------------------------------------------------
    def computar_custo(self, veiculo: dict, data_hora_saida: datetime):
        """
        Aplicar calculo de custo de acordo com o tipo de acesso

        Args:
            veiculo (dict): registro do veiculo registradado na entrada
            data_hora_saida (datetime): data e hora que o veiculo saiu do estacionamento

        Raises:
            DataHoraInvalidaException: Data Hora saída menor ou igual a entrada

        Returns:
            float: valor a ser cobrado com ou sem desconto da seguradora
        """
        tipo_acesso = veiculo["tipo_acesso"]
        data_hora_entrada = veiculo["dt_entrada"]
        duracao_sec = (data_hora_saida - data_hora_entrada).seconds

        if duracao_sec <= 0:
            raise DataHoraInvalidaException("Data Hora saída menor ou igual a entrada")

        if tipo_acesso == "MENSALISTA":
            custo = 0.00

        elif tipo_acesso == "EVENTO":
            custo = self.__valor_evento

        else:
            custo = self.calcular_custo_rotativo(data_hora_entrada, data_hora_saida)

        # Aplicar desconto da seguradora
        if veiculo["desc_seguradora"]:
            custo = custo * self.__desconto_seguradora

        return custo

    # =================================================================================
    def calcular_custo_rotativo(self, data_hora_entrada, data_hora_saida):
        """
        Calcular o custo com base no tempo que o veiculo permaneceu no estacionamento
        ou regras de horario de entrada e saída.

        Args:
            data_hora_entrada (datetime): data e hora que o veiculo entrou no estacionamento
            data_hora_saida (datetime): data e hora que o veiculo saiu do estacionamento

        Returns:
            float: valor a ser cobrado sem desconto
        """
        if (
            data_hora_saida.day == data_hora_entrada.day + 1
            and data_hora_entrada.hour >= 21
            and data_hora_saida.hour < 8
        ):
            return self.valor_diaria_noturna

        duracao_min = self.calcular_duracao_min(data_hora_entrada, data_hora_saida)
        fracao_15min = round(duracao_min / 15)

        if fracao_15min < 4:
            return fracao_15min * self.__valor_fracao  # type: ignore

        if fracao_15min >= 36:
            return self.__valor_diaria_diurna

        duracao_hora = fracao_15min / 4
        return duracao_hora * self.valor_hora_cheia

    # =================================================================================

    @property
    def get_total_apurado_contratante(self) -> float:
        """
        Metodo responsavel em calcular valor do contratante.

        Returns:
            float: valor total do contratante
        """
        return self.get_total_apurado * self.__percetual_contratante

    @property
    def get_total_apurado(self) -> float:
        """
        Metodo responsavel em calcular todo o valor de entrada de um
        estacionamento.
        Entrada = acessos(rotativo e evento) + veiculos mensalista.

        Returns:
            float: valor total apurado
        """
        mensalistas = len(self.__registro_mensalistas) * self.__valor_mensalista
        return (
            sum(registro.get("custo") for _, registro in self.__registro_saida.items())
            + mensalistas
        )


# =================================================================================
