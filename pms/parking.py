class Estacionamento:
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
        self.capacidade_maxima = capacidade_maxima
        self.valor_fracao = valor_fracao
        self.valor_diaria_diurna = valor_diaria_diurna
        self.desconto_hora_cheia = desconto_hora_cheia
        self.desconto_diaria_notura = desconto_diaria_notura
        self.valor_mensalista = valor_mensalista
        self.valor_evento = valor_evento
