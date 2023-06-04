import abc
import dataclasses
import enum
import os

from dotenv import load_dotenv
import requests

load_dotenv()

openexch_api = os.getenv("API_OpenExch")
layer_api = os.getenv("API_ApiLayer")
headers = {"apikey": layer_api}


class ExchangeCodes(enum.Enum):
    USD = 840
    EUR = 978
    UAH = 980


@dataclasses.dataclass(frozen=True)
class SellBuy:
    sell: float
    buy: float


class ExchangeBase(abc.ABC):
    """
    Base class for exchange providers, should define get_rate() method
    """

    def __init__(self, vendor, currency_a, currency_b):
        self.vendor = vendor
        self.currency_a = currency_a
        self.currency_b = currency_b
        self.pair: SellBuy = None

    @abc.abstractmethod
    def get_rate(self):
        raise NotImplementedError("Method get_rate() is not implemented")


class MonoExchange(ExchangeBase):
    def get_rate(self):
        a_code = ExchangeCodes[self.currency_a].value
        b_code = ExchangeCodes[self.currency_b].value
        r = requests.get("https://api.monobank.ua/bank/currency")
        r.raise_for_status()
        for rate in r.json():
            currency_code_a = rate["currencyCodeA"]
            currency_code_b = rate["currencyCodeB"]
            if currency_code_a == a_code and currency_code_b == b_code:
                self.pair = SellBuy(rate["rateSell"], rate["rateBuy"])
                return


class PrivatExchange(ExchangeBase):
    def get_rate(self):
        r = requests.get(
            "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11"
        )
        r.raise_for_status()
        for rate in r.json():
            if rate["ccy"] == self.currency_a and rate["base_ccy"] == self.currency_b:
                self.pair = SellBuy(float(rate["sale"]), float(rate["buy"]))


class NacBankExchange(ExchangeBase):
    def get_rate(self):
        spread = 0.36
        r = requests.get(
            "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
        )
        r.raise_for_status()
        for elem in r.json():
            if elem["r030"] == ExchangeCodes[self.currency_a].value:
                self.pair = SellBuy(elem["rate"], elem["rate"] - spread)

    f"""
        В следующих 2 случаях сделана имитация buy  т.к. провайдер бесплатно не дает менять базовую валюту при 
    запросе. Для этого добавлена случайная величина spread в каждую функцию для реальности. 
    Так же это причина почему там нет курса EUR/UAH, т.к. базовая валюта вегда доллар. 
    """


class OpenExchange(ExchangeBase):
    def get_rate(self):
        spread = 0.55
        url = f"https://openexchangerates.org/api/latest.json?app_id={openexch_api}&base=USD&symbols=UAH"
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
        if data["base"] == self.currency_a:
            self.pair = SellBuy(data["rates"]["UAH"], data["rates"]["UAH"] - spread)


class LayerExchange(ExchangeBase):
    def get_rate(self):
        spread = 0.43
        url = "https://api.apilayer.com/fixer/latest?symbols=UAH&base=USD"
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        if data["base"] == self.currency_a:
            self.pair = SellBuy(data["rates"]["UAH"], data["rates"]["UAH"] - spread)
