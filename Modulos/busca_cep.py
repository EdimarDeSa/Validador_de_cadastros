import re

import pandas as pd
import requests


class Cep:
    def __init__(self, cep: str):
        self.__dirt_cep = cep
        api_viacep = f'http://www.viacep.com.br/ws/{self.__clean_cep}/json'

        with requests.get(api_viacep) as response:
            self.data = self.__response_verification(response)

    @property
    def __clean_cep(self) -> str:
        cleaned_cep = re.sub(r'\D+', '', self.__dirt_cep)
        cleaned_cep = cleaned_cep + "0"*(8 - len(cleaned_cep))
        return cleaned_cep

    def __response_verification(self, response):
        if response.status_code != 200:
            return self.__error_data()

        data = response.json()
        if 'erro' in data:
            return self.__error_data()

        return data

    @property
    def series(self) -> pd.Series:
        series = pd.Series(self.data)
        return series

    def __error_data(self) -> dict:
        return {
            'cep': self.__clean_cep, 'logradouro': '', 'complemento': '', 'bairro': '', 'localidade': '', 'uf': '', 'ibge': '', 'gia': '', 'ddd': '', 'siafi': ''
        }