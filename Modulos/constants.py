CODECS: list = ['ascii', 'big5', 'big5hkscs', 'cp037', 'cp273', 'cp424', 'cp437', 'cp500', 'cp720', 'cp737', 'cp775',
                'cp850', 'cp852', 'cp855', 'cp856', 'cp857', 'cp858', 'cp860', 'cp861', 'cp862', 'cp863', 'cp864',
                'cp865', 'cp866', 'cp869', 'cp874', 'cp875', 'cp932', 'cp949', 'cp950', 'cp1006', 'cp1026', 'cp1125',
                'cp1140', 'cp1250', 'cp1251', 'cp1252', 'cp1253', 'cp1254', 'cp1255', 'cp1256', 'cp1257', 'cp1258',
                'eucjp', 'ujis', 'u-jis', 'jisx0213', 'eucjis2004', 'eucjisx0213', 'euckr', 'korean', 'ksc5601',
                'ks_c-5601', 'ks_c-5601-1987', 'ksx1001', 'ks_x-1001', 'chinese', 'csiso58gb231280', 'euc-cn', 'euccn',
                'eucgb2312-cn', 'gb2312-1980', 'gb2312-80', 'iso-ir-58', '936', 'cp936', 'ms936', 'gb18030-2000',
                'hzgb', 'hz-gb', 'hz-gb-2312', 'csiso2022jp', 'iso2022jp', 'iso-2022-jp', 'iso2022jp-1',
                'iso-2022-jp-1', 'iso2022jp-2', 'iso-2022-jp-2', 'iso2022jp-2004', 'iso-2022-jp-2004', 'iso2022jp-3',
                'iso-2022-jp-3', 'iso2022jp-ext', 'iso-2022-jp-ext', 'csiso2022kr', 'iso2022kr', 'iso-2022-kr',
                'iso-8859-1', 'iso8859-1', '8859', 'cp819', 'latin', 'latin1', 'L1', 'iso-8859-2', 'latin2', 'L2',
                'iso-8859-3', 'latin3', 'L3', 'iso-8859-4', 'latin4', 'L4', 'iso-8859-5', 'cyrillic', 'iso-8859-6',
                'arabic', 'iso-8859-7', 'greek', 'greek8', 'iso-8859-8', 'hebrew', 'iso-8859-9', 'latin5', 'L5',
                'iso-8859-10', 'latin6', 'L6', 'iso-8859-11', 'thai', 'iso-8859-13', 'latin7', 'L7', 'iso-8859-14',
                'latin8', 'L8', 'iso-8859-15', 'latin9', 'L9', 'iso-8859-16', 'latin10', 'L10', 'cp1361', 'ms1361',
                'koi8_r', 'koi8_t', 'koi8_u', 'kz_1048', 'strk1048_2002', 'rk1048', 'maccyrillic', 'macgreek',
                'maciceland', 'maclatin2', 'maccentraleurope', 'mac_centeuro', 'macroman', 'macintosh', 'macturkish',
                'csptcp154', 'pt154', 'cp154', 'cyrillic-asian', 'csshiftjis', 'shiftjis', 'sjis', 's_jis',
                'shiftjis2004', 'shiftjisx0213', 'sjisx0213', 's_jisx0213', 'U32', 'utf32', 'UTF-32BE', 'UTF-32LE',
                'U16', 'utf16', 'UTF-16BE', 'UTF-16LE', 'U7', 'unicode-1-1-utf-7', 'U8', 'UTF', 'utf8', 'cp65001',
                'utf_8_sig']

CODECS.reverse()

SEPARADORES: set = {',', ';', '\t'}

EXTENSOES: list[tuple[str, str]] = [
    ('Todos os Arquivos', '*.csv;*.txt;*.xlsx'),
    ('Arquivos CSV', '*.csv'),
    ('Arquivos do Excel', '*.xlsx'),
    ('Arquivo de texto', '*.txt'),
]

EXTENSAO_DEFAULT = '.csv'

NOME_PARTICIPANTE: str = 'Nome completo'

STRING_COLUNA_CPF: str = 'CPF (sem pontos e traço ex: 12345678900)'  # Depricated
NOME: str = 'Nome completo'
CPF: str = 'CPF'
VALIDADE_CPF: str = 'Validade_cpf'
DUPLICADA: str = 'Duplicada'
COLABORADOR: str = 'Colaborador'


COLUNAS_SERVICO_IMPRESSORAS = ['JobId', 'pPrinterName', 'pMachineName', 'pUserName', 'pDocument', 'pDatatype', 'pStatus', 'Status', 'Priority', 'Position', 'TotalPages', 'PagesPrinted']

TEMA = 'minty'

