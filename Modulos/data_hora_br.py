from datetime import datetime

__all__ = ['DatasBr']


class DatasBr:
    def __init__(
        self,
        data: str = None,
        formato_data='%d/%m/%Y',
        hora: str = None,
        formato_hora='%H:%M:%S',
        data_e_hora: str = None,
    ):
        """
        Caso não seja passado nenhum parâmetro será usado a data e hora atual.
        :param data: str(dd/mm/aaaa)
        :param formato_data: str, padrão=%d/%m/%Y
        :param hora: str(hh:mm:ss)
        :param formato_hora: str, padrão=%H:%M:%S
        :param data_e_hora: str(dd/mm/aaaa hh:mm:ss)
        """
        self._formato_data = formato_data
        self._formato_hora = formato_hora
        self._data: datetime = None
        self._hora: datetime = None
        self._nomes_meses = {
            1: 'Janeiro',
            2: 'Fevereiro',
            3: 'Março',
            4: 'Abril',
            5: 'Maio',
            6: 'Junho',
            7: 'Julho',
            8: 'Agosto',
            9: 'Setembro',
            10: 'Outubro',
            11: 'Novembro',
            12: 'Dezembro',
        }
        self._nomes_semana = {
            0: 'Segunda-feira',
            1: 'Terça-feira',
            2: 'Quarta-feira',
            3: 'Quinta-feira',
            4: 'Sexta-feira',
            5: 'Sábado',
            6: 'Domingo',
        }
        self._converte(data, hora, data_e_hora)

    def _converte(self, data, hora, data_e_hora):
        if not data and not hora and not data_e_hora:
            data_e_hora = datetime.now().strftime(
                f'{self._formato_data} {self._formato_hora}'
            )

        if data_e_hora:
            data, hora = [x for x in data_e_hora.split()]

        self._data = datetime.strptime(data, self._formato_data)

        self._hora = datetime.strptime(hora, self._formato_hora)

    @property
    def data(self):
        return self._data.strftime(self._formato_data)

    @property
    def horario(self):
        return self._hora.strftime(self._formato_hora)

    @property
    def data_e_hora(self):
        return f'{self.data} {self.horario}'

    @property
    def nome_da_semana(self):
        return self._nomes_semana.get(self._data.weekday(), None)

    @property
    def nome_do_mes(self):
        return self._nomes_meses.get(self._data.month, None)

    @property
    def ano(self):
        return self._data.strftime('%Y')

    @property
    def dia(self):
        return self._data.strftime('%d')

    @property
    def mes(self):
        return self._data.strftime('%m')

    @property
    def hora(self):
        return self._data.strftime('%H')

    @property
    def minuto(self):
        return self._data.strftime('%M')

    @property
    def segundo(self):
        return self._data.strftime('%S')

    def tempo_cadastro(self):
        dias_totais = (datetime.today() - self._data).days
        anos, dias = divmod(dias_totais, 360)
        return dict(anos=anos, dias=dias)

    @property
    def __dict__(self):
        return dict(
            data=self.data,
            horario=self.horario,
            data_e_hora=self.data_e_hora,
            _formato_data=self._formato_data,
            _formato_hora=self._formato_hora,
            nome_da_semana=self.nome_da_semana,
            nome_do_mes=self.nome_do_mes,
            tempo_cadastro=self.tempo_cadastro(),
        )


if __name__ == '__main__':
    data = DatasBr(data_e_hora='04/08/2023 07:55:00')
    print(data.__dict__)
