import datetime
from pathlib import Path

from src.Models.model import Model
from src.Schemas.participants import Participant, Prize, Sorteio

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
    agora = datetime.datetime.now()

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

        esperado1 = Participant
        esperado2 = Participant(**PARTICIPANTE)

        comparacao1 = isinstance(resultado, esperado1)
        comparacao2 = resultado == esperado2

        assert comparacao1 and comparacao2

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

    def test_search_products_on_table(self):
        product_table_path = 'C:/Users/Edimar/Documents/GitHub/Validador_de_cadastros/data/Tabela de Preços Distribuição - Novembro V1.xlsx'
        self.model.read_product_table(product_table_path)
        entrada = '4750075'

        resultado: Prize = self.model.search_product(entrada)

        esperado1 = isinstance(resultado, Prize)
        esperado2 = all([
            resultado.descricao == 'ROTEADOR WIRELESS ACTION RF 1200',
            resultado.quantidade == 1,
            resultado.responsavel_cc == 'Marta Rosa Nunes',
            resultado.centro_de_custos == '25305',
            resultado.data_fechamento_cc == datetime.date(2023, 12, 26)
        ])

        comparacao = esperado1 and esperado2

        assert comparacao

    def test_insert_a_sort(self):
        premio1 = self.model.create_prize(
            descricao='Câmera VIP 1010',
            codigo='123123123',
            quantidade=2,
            centro_de_custos=': str',
            data_fechamento_cc=self.agora,
            responsavel_cc=': str',
        )
        premio2 = self.model.create_prize(
            descricao='Câmera VIP 1010',
            codigo='123123123',
            quantidade=2,
            centro_de_custos=': str',
            data_fechamento_cc=self.agora,
            responsavel_cc=': str',
        )

        sorteio = self.model.create_prize_drawing(
            nome_do_sorteio='Sorteio 1',
            dia_do_sorteio='30/11/2023',
            prizes=[premio1, premio2],
        )

        assert sorteio == 1

        sorteio2 = self.model.create_prize_drawing(
            nome_do_sorteio='Sorteio 2',
            dia_do_sorteio='30/11/2023',
            prizes=[premio1, premio2],
        )

        assert sorteio2 == 2

    def test_read_prize_draw(self):
        entrada = 1

        resultado = self.model.read_prize_draw(entrada)

        esperado1 = Sorteio

        esperado2 = all([
            resultado.vencedor is None,
            resultado.dia_do_sorteio == datetime.datetime.fromisoformat("2023-11-30T00:00:00"),
            resultado.nome_do_sorteio == 'Sorteio 1',
            resultado.id_sorteio == 1
        ])

        comparacao1 = isinstance(resultado, esperado1)
        comparacao2 = esperado2

        assert comparacao1 and comparacao2

    def test_insert_winner(self):
        entrada = '613.302.483-68'

        self.model.insert_winner(1, entrada)

        resultado = self.model.read_prize_draw(1)

        esperado = all([
            resultado.vencedor.nome == 'Nailson Rodrigues Silva ',
            resultado.dia_do_sorteio == datetime.datetime.fromisoformat("2023-11-30T00:00:00"),
            resultado.nome_do_sorteio == 'Sorteio 1',
            resultado.id_sorteio == 1
        ])

        comparacao = esperado

        assert comparacao
