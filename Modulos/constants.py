from ttkbootstrap.constants import *

ICONE = './icons/icons8-lottery-50.png'

CODECS: list = [
    'utf_8_sig',
    'cp65001',
    'utf8',
    'UTF',
    'U8',
    'unicode-1-1-utf-7',
    'U7',
    'UTF-16LE',
    'UTF-16BE',
    'utf16',
    'U16',
    'UTF-32LE',
    'UTF-32BE',
    'utf32',
    'U32',
    's_jisx0213',
    'sjisx0213',
    'shiftjisx0213',
    'shiftjis2004',
    's_jis',
    'sjis',
    'shiftjis',
    'csshiftjis',
    'cyrillic-asian',
    'cp154',
    'pt154',
    'csptcp154',
    'macturkish',
    'macintosh',
    'macroman',
    'mac_centeuro',
    'maccentraleurope',
    'maclatin2',
    'maciceland',
    'macgreek',
    'maccyrillic',
    'rk1048',
    'strk1048_2002',
    'kz_1048',
    'koi8_u',
    'koi8_t',
    'koi8_r',
    'ms1361',
    'cp1361',
    'L10',
    'latin10',
    'iso-8859-16',
    'L9',
    'latin9',
    'iso-8859-15',
    'L8',
    'latin8',
    'iso-8859-14',
    'L7',
    'latin7',
    'iso-8859-13',
    'thai',
    'iso-8859-11',
    'L6',
    'latin6',
    'iso-8859-10',
    'L5',
    'latin5',
    'iso-8859-9',
    'hebrew',
    'iso-8859-8',
    'greek8',
    'greek',
    'iso-8859-7',
    'arabic',
    'iso-8859-6',
    'cyrillic',
    'iso-8859-5',
    'L4',
    'latin4',
    'iso-8859-4',
    'L3',
    'latin3',
    'iso-8859-3',
    'L2',
    'latin2',
    'iso-8859-2',
    'L1',
    'latin1',
    'latin',
    'cp819',
    '8859',
    'iso8859-1',
    'iso-8859-1',
    'iso-2022-kr',
    'iso2022kr',
    'csiso2022kr',
    'iso-2022-jp-ext',
    'iso2022jp-ext',
    'iso-2022-jp-3',
    'iso2022jp-3',
    'iso-2022-jp-2004',
    'iso2022jp-2004',
    'iso-2022-jp-2',
    'iso2022jp-2',
    'iso-2022-jp-1',
    'iso2022jp-1',
    'iso-2022-jp',
    'iso2022jp',
    'csiso2022jp',
    'hz-gb-2312',
    'hz-gb',
    'hzgb',
    'gb18030-2000',
    'ms936',
    'cp936',
    '936',
    'iso-ir-58',
    'gb2312-80',
    'gb2312-1980',
    'eucgb2312-cn',
    'euccn',
    'euc-cn',
    'csiso58gb231280',
    'chinese',
    'ks_x-1001',
    'ksx1001',
    'ks_c-5601-1987',
    'ks_c-5601',
    'ksc5601',
    'korean',
    'euckr',
    'eucjisx0213',
    'eucjis2004',
    'jisx0213',
    'u-jis',
    'ujis',
    'eucjp',
    'cp1258',
    'cp1257',
    'cp1256',
    'cp1255',
    'cp1254',
    'cp1253',
    'cp1252',
    'cp1251',
    'cp1250',
    'cp1140',
    'cp1125',
    'cp1026',
    'cp1006',
    'cp950',
    'cp949',
    'cp932',
    'cp875',
    'cp874',
    'cp869',
    'cp866',
    'cp865',
    'cp864',
    'cp863',
    'cp862',
    'cp861',
    'cp860',
    'cp858',
    'cp857',
    'cp856',
    'cp855',
    'cp852',
    'cp850',
    'cp775',
    'cp737',
    'cp720',
    'cp500',
    'cp437',
    'cp424',
    'cp273',
    'cp037',
    'big5hkscs',
    'big5',
    'ascii',
]

SEPARADORES: set = {',', ';', '\t'}

EXTENSOES: list[tuple[str, str]] = [
    ('Todos os Arquivos', '*.csv;*.xlsx;*.txt'),
    ('Arquivos CSV', '*.csv'),
    ('Arquivos do Excel', '*.xlsx'),
    ('Arquivo de texto', '*.txt'),
]

EXTENSAO_DEFAULT = '.csv'

NOME_PARTICIPANTE = NOME = 'Nome completo'
STRING_COLUNA_CPF: str = 'CPF (sem pontos e traço ex: 12345678900)'  # Depricated
CPF: str = 'CPF'
VALIDADE_CPF: str = 'Validade_cpf'
DUPLICADA: str = 'Duplicada'
COLABORADOR: str = 'Colaborador'
ENDERECO = 'Endereço completo'

COLUNAS_SERVICO_IMPRESSORAS = [
    'JobId',
    'pPrinterName',
    'pMachineName',
    'pUserName',
    'pDocument',
    'pDatatype',
    'pStatus',
    'Status',
    'Priority',
    'Position',
    'TotalPages',
    'PagesPrinted',
]

COLUNAS_DA_TELA_DE_SORTEIOS = [
    dict(text='Código', width=120),
    dict(text='Nome', width=370),
    dict(text='Qtd', width=40),
    dict(text='CC', width=80),
    dict(text='Fechamento CC', width=120),
    dict(text='Responsável CC', width=200),
]

COLUNAS_DA_TABELA_DE_PREMIOS = [
    'codigo',
    'nome',
    'quantidade',
    'cc',
    'data_fechamento_cc',
    'responsavel_cc',
]

COLUNAS_DA_TABELA_DE_PARTICIPANTES = [
    'Nome completo',
    'RG',
    'Endereço completo',
    'Email',
    'Data de nascimento',
    'Telefone',
    'aceite_novidades',
    'CPF',
    'CEP',
    'Data',
    'Dia_do_evento',
    'Duplicada',
    'Validade_cpf',
    'Colaborador',
]

LINHAS_TESTE = [
    (
        str(11111111111 * i).zfill(11),
        f'Produto {i}',
        f'{i}',
        '12345',
        '12/01/2024',
        'Marta Rosa Nunes',
    )
    for i in range(5)
]

# Cores
BRANCO = 'FFFFFF'
PRETO = '000000'
VERDE = '008000'
AMARELO = 'FFFF00'

ENGLISH_ZEN = """Beautiful is better than ugly. 
Explicit is better than implicit. 
Simple is better than complex. 
Complex is better than complicated.
Flat is better than nested. 
Sparse is better than dense.  
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!"""

PORTUGUESE_ZEN = """Bonito é melhor que feio.
Explícito é melhor que implícito.
Simples é melhor que complexo.
Complexo é melhor que complicado.
Plano é melhor que aninhado.
Esparso é melhor que denso.
A legibilidade conta.
Casos especiais não são especiais o suficiente para quebrar as regras.
Embora a praticidade supere a pureza.
Os erros nunca devem passar silenciosamente.
A menos que seja explicitamente silenciado.
Diante da ambiguidade, recuse a tentação de adivinhar.
Deveria haver uma - e de preferência apenas uma - maneira óbvia de fazer isso.
Embora essa forma possa não ser óbvia à primeira vista, a menos que você seja holandês.
Agora é melhor do que nunca.
Embora nunca muitas vezes é melhor do que *para já*.
Se a implementação for difícil de explicar, é uma má ideia.
Se a implementação for fácil de explicar, pode ser uma boa ideia.
Namespaces são uma ótima ideia - vamos fazer mais desses!"""
