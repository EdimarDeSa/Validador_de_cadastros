import re



def limpeza_de_dados(cpf: str) -> str:
    apenas_digitos = re.sub(r'\D+', '', cpf)
    completa_11_digitos = apenas_digitos.zfill(11)
    return completa_11_digitos


def capitaliza_nome(nome: str) -> str:
    nome_e_sobrenome_capitalizado = ' '.join([parte_do_nome.capitalize() for parte_do_nome in nome.split()])
    return nome_e_sobrenome_capitalizado

def calcula_tempo_de_impressao_total(quantidade: int):
    total_seconds = (quantidade - 1) * 2
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes}:{seconds:02}"


def calc_linha(linha):
    step = 0.1
    return 0.02 + ((linha - 1) * step)

def calc_coluna(coluna):
    colunas = {
        1: 0.01,
        2: 0.25,
        3: 0.51,
        4: 0.75
    }
    return colunas[coluna]