def limpa_texto(texto: str, filtro):
    return ''.join(filter(filtro, texto))


def apenas_letras_e_espacos(d: str):
    return d.isalpha() or d.isspace()


def apenas_digitos(d: str):
    return d.isdigit()


def sanitiza_cpf(cpf: str) -> str:
    digitos_limpos = limpa_texto(cpf, apenas_digitos)
    completa_11_digitos = digitos_limpos.zfill(11)
    return completa_11_digitos


def sanitiza_nome(nome: str) -> str:
    nome_limpo = limpa_texto(nome, apenas_letras_e_espacos)
    nome_capitalizado = ' '.join([parte_do_nome.title() for parte_do_nome in nome_limpo.split()])
    return nome_capitalizado


if __name__ == '__main__':
    nome = sanitiza_nome('edimar fr3eitas de Sá')
    print(nome)
    cpf = sanitiza_cpf('048d245.251-01')
    print(cpf)