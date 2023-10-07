def limpa_texto(texto, filtro) -> str:
    return ''.join(filter(filtro, str(texto)))


def apenas_letras_e_espacos(d: str) -> bool:
    return d.isalpha() or d.isspace()


def apenas_digitos(d: str) -> bool:
    return d.isdigit()


def sanitiza_cpf(cpf: str) -> str:
    digitos_limpos = limpa_texto(cpf, apenas_digitos)
    completa_11_digitos = digitos_limpos.zfill(11)
    return completa_11_digitos


def sanitiza_nome(nome: str) -> str:
    nome_limpo = limpa_texto(nome, apenas_letras_e_espacos)
    nome_capitalizado = ' '.join([parte_do_nome.title() for parte_do_nome in nome_limpo.split()])
    return nome_capitalizado
