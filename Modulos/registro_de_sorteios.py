import pandas as pd


class Lottery:
    def __init__(self, lottery_id: str, product_list: list[dict]):
        self.__lottery_id = lottery_id
        self.__product_list = product_list
        self.__winner = None
    @property
    def lottery_id(self) -> str:
        return self.__lottery_id
    
    @property
    def product_list(self) -> list:
        return self.__product_list

    @product_list.setter
    def product_list(self, new_list: list[dict]) -> None:
        self.__product_list = new_list
    
    @property
    def winner(self) -> any:
        return self.__winner
    
    @winner.setter
    def winner(self, new_winner: any) -> None:
        self.__winner = new_winner


class Lotteries:
    def __init__(self):
        self.__lotteries_dict = {}

    def create_lottery(self, products: list[dict]) -> None:
        lottery_id = f'Lottery {len(self.__lotteries_dict) + 1}'
        new_lottery = Lottery(lottery_id, products)
        self.__lotteries_dict[lottery_id] = new_lottery

    @property
    def lotteries_list(self) -> list:
        return list(self.__lotteries_dict.keys())

    def get_lottery(self, lottery_id: str) -> Lottery:
        return self.__lotteries_dict.get(lottery_id, None)

    def register_winner(self, winner: pd.Series, lottery_id: str) -> None:
        lottery = self.get_lottery(lottery_id)
        if lottery is None:
            raise ValueError(f'Invalid lottery ID: {lottery_id}')
        lottery.winner = winner

    def delete_lottery(self, lottery_id: str) -> None:
        if lottery_id not in self.__lotteries_dict:
            raise ValueError(f'Invalid lottery ID: {lottery_id}')
        del self.__lotteries_dict[lottery_id]
