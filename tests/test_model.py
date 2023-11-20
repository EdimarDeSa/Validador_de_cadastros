from pathlib import Path

from src.Models.model import Model
from src.Schemas.participants import Participant

PARTICIPANTE = {
    'Nome completo': 'Edimar Freitas de Sá',
    'RG': '600724693-4',
    'Endereço completo': 'Coronel Genuíno, 194/403',
    'Email': 'albertomaciel@mprs.mp.br',
    'Data de nascimento': '2005-09-28',
    'Telefone': '(51) 99210-9965',
    'CPF': '048+245+251=01',
    'CEP': '90.010-350',
    'Data': '28/09/2023 19:38:34',
}
PARTICIPANTES_PATH = 'C:/Users/Edimar/Documents/GitHub/Validador_de_cadastros/data/9-28-2023-Evento_de_lancamentos-_Abril.csv'
FUNCIONARIOS_PATH = 'C:/Users/Edimar/Documents/GitHub/Validador_de_cadastros/data/Colaboradores_test.csv'


class TestModel:
    model = Model()
    model.update_event_date('28/09/2023')
    model.set_hora_inicio('19:00:00')
    model.set_hora_fim('19:40:00')

    def test_insert_single_participant(self):
        entrada = PARTICIPANTE

        resultado = self.model.create_participants([entrada])

        esperado = (1,)

        comparacao = resultado == esperado

        assert comparacao

    def test_insert_a_list_of_employees(self):
        entrada = FUNCIONARIOS_PATH

        resultado = self.model.read_file(Path(entrada).resolve())
        resultado = self.model.create_employees(resultado)

        esperado = (1,)

        comparacao = resultado == esperado

        assert comparacao

    def test_read_a_single_participant(self):
        entrada = '048.245.251-01'

        resultado = self.model.read_participant_by_cpf(entrada)

        esperado = Participant

        comparacao = isinstance(resultado, esperado)

        assert comparacao

    def test_removing_a_participant(self):
        entrada = '048.245.251-01'

        resultado = self.model.delete_participant_by_cpf(entrada)

        esperado = (1,)

        comparacao = resultado == esperado

        assert comparacao

    def test_insert_a_list_of_participants(self):
        entrada = PARTICIPANTES_PATH

        resultado = self.model.read_file(Path(entrada).resolve())
        resultado = self.model.create_participants(resultado)

        esperado = 2, 3, 4, 5

        comparacao = resultado == esperado

        assert comparacao

    def test_sum_of_valid_participants(self):
        entrada = self.model.contadores

        resultado = entrada.inscricoes_validas

        esperado = 4

        comparacao = resultado == esperado

        assert comparacao

    def test_sum_of_employees(self):
        entrada = self.model.contadores

        resultado = entrada.employees

        esperado = 1

        comparacao = resultado == esperado

        assert comparacao

    def test_sum_of_cadastros_repetidos(self):
        entrada = self.model.contadores

        resultado = entrada.cadastros_repetidos

        esperado = 5

        comparacao = resultado == esperado

        assert comparacao

    def test_sum_of_cpfs_invalidos(self):
        entrada = self.model.contadores

        resultado = entrada.cpfs_invalidos

        esperado = 4

        comparacao = resultado == esperado

        assert comparacao

    def test_sum_of_out_of_time(self):
        entrada = self.model.contadores

        resultado = entrada.out_of_time

        esperado = 3

        comparacao = resultado == esperado

        assert comparacao
