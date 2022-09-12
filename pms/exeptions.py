class EstacionamentoCheioException(Exception):
    """
    Uma exceção para sinalizar que não é possível registrar uma entrada
    com o estacionamento em nenhuma vaga disponível.

    Attributes:
        message (str): Mensagem de exceção.
    """

    def __init__(self, message):
        super(EstacionamentoCheioException, self).__init__(message)
        self.message = message


class EstacionamentoVazioException(Exception):
    """
    Uma exceção para sinalizar que não é possível registrar uma saída
    com o estacionamento vazio.

    Attributes:
        message (str): Mensagem de exceção.
    """

    def __init__(self, message):
        super(EstacionamentoVazioException, self).__init__(message)
        self.message = message


class DescricaoEmBrancoException(Exception):
    """
    Uma sinal de exceção para não permitir campos em branco para os
    dados de acesso (entrada e saída) e para dados do estacionamento.

    Attributes:
        message (str): Mensagem de exceção.
    """

    def __init__(self, message):
        super(DescricaoEmBrancoException, self).__init__(message)
        self.message = message


class ValorAcessoInvalidoException(Exception):
    """
    Uma sinal de exceção para não permitir informar valores de
    acesso inválidos.

    Attributes:
        message (str): Mensagem de exceção.
    """

    def __init__(self, message):
        super(ValorAcessoInvalidoException, self).__init__(message)
        self.message = message


class VeiculoNaoRegistrado(Exception):
    """
    Uma exceção para sinalizar que o veiculo procurado não foi
    registrado.

    Attributes:
        message (str): Mensagem de exceção.
    """

    def __init__(self, message):
        super(VeiculoNaoRegistrado, self).__init__(message)
        self.message = message


class DataHoraInvalidaException(Exception):
    """
    Uma exceção para sinalizar que essa data/hora não faz
    sentido nesse contexto.

    Attributes:
        message (str): Mensagem de exceção.
    """

    def __init__(self, message):
        super(DataHoraInvalidaException, self).__init__(message)
        self.message = message


class VeiculoExisteRegistroException(Exception):
    """
    Uma exceção para sinalizar que o veiculo já foi registrado
    anteriormente (duplicação de registro).

    Attributes:
        message (str): Mensagem de exceção.
    """

    def __init__(self, message):
        super(VeiculoExisteRegistroException, self).__init__(message)
        self.message = message


class NegativeNumError(Exception):
    def __init__(self):
        super().__init__("Negative number not supported")
