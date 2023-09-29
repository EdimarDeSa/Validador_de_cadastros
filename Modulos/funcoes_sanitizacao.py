import re


def sanitiza_cpf(cpf: str) -> str:
    apenas_digitos = re.sub(r'\D+', '', cpf)
    completa_11_digitos = apenas_digitos.zfill(11)
    return completa_11_digitos


def sanitiza_nome(nome: str) -> str:
    nome_limpo = re.sub(r'[^a-zA-ZÀ-ÖØ-öø-ÿ ]', '', nome)
    nome_e_sobrenome_capitalizado = ' '.join([parte_do_nome.capitalize() for parte_do_nome in nome_limpo.split()])
    return nome_e_sobrenome_capitalizado
