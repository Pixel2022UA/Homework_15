import json
import os
import pathlib
from datetime import date

import pytest
import responses
from django.core.management import call_command
from dotenv import load_dotenv
from freezegun import freeze_time

from .exchange_provider import MonoExchange, PrivatExchange, NacBankExchange, OpenExchange, LayerExchange
from .models import Rate
from .views import index

root = pathlib.Path(__file__).parent

load_dotenv()

openexch_api = os.getenv("API_OpenExch")
layer_api = os.getenv("API_ApiLayer")
headers = {"apikey": layer_api}

@pytest.fixture
def mocked():
    def inner(file_name):
        return json.load(open(root / "fixtures" / file_name))

    return inner


@responses.activate
def test_exchange_mono(mocked):
    mocked_response = mocked("mono_response.json")
    responses.get(
        "https://api.monobank.ua/bank/currency",
        json=mocked_response,
    )
    e = MonoExchange("mono", "USD", "UAH")
    e.get_rate()
    assert e.pair.sell == 37.4406


@responses.activate
def test_privat_rate(mocked):
    mocked_response = mocked("privat_response.json")
    responses.get(
        "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11",
        json=mocked_response,
    )
    e = PrivatExchange("privat", "USD", "UAH")
    e.get_rate()
    assert e.pair.sell == 37.45318

@responses.activate
def test_nacbank_rate(mocked):
    mocked_response = mocked("nacbank_response.json")
    responses.get(
        "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json",
        json=mocked_response,
    )
    e = NacBankExchange("nacbank", "USD", "UAH")
    e.get_rate()
    assert e.pair.sell == 36.5686

@responses.activate
def test_openexch_rate(mocked):
    mocked_response = mocked("openexch_response.json")
    responses.get(
        f"https://openexchangerates.org/api/latest.json?app_id={openexch_api}&base=USD&symbols=UAH",
        json=mocked_response,
    )
    e = OpenExchange("openexch", "USD", "UAH")
    e.get_rate()
    assert e.pair.sell == 37.073792



@pytest.mark.django_db
def test_data_exists_for_today():
    today = date.today()
    data_exists = Rate.objects.filter(date=today).exists()
    assert data_exists


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "db_init.yaml")


@freeze_time("2023-06-04")
@pytest.mark.django_db
def test_index_view():
    response = index(None)
    assert response.status_code == 200
    assert json.loads(response.content) == {
        "current_rates": [
            {
                "id": 1,
                "date": "2023-06-04",
                "vendor": "mono",
                "currency_a": "USD",
                "currency_b": "EUR",
                "sell": 1.3,
                "buy": 1.4,
            },
            {
                "id": 2,
                "date": "2023-06-04",
                "vendor": "privat",
                "currency_a": "USD",
                "currency_b": "EUR",
                "sell": 1.3,
                "buy": 1.4,
            },
        ]
    }
