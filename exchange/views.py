import datetime
import decimal

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from .forms import RateForm
from .models import Rate


class DecimalAsFloatJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super().default(o)


def exchange(request):
    form = RateForm(request.POST or None)
    context = {"form": form}
    if request.method == "POST":
        if form.is_valid():
            currency_a = form.cleaned_data["currency_a"]
            amount_a = form.cleaned_data["amount_a"]
            currency_b = form.cleaned_data["currency_b"]
            amount_b = calculate_amount_b(currency_a, amount_a, currency_b)
            context = {"form": form, "amount_b": amount_b, "currency_b": currency_b}
            return render(request, "exchange.html", context)
    return render(request, "exchange.html", context)


def calculate_amount_b(currency_a, amount_a, currency_b):
    today = timezone.now().date()
    if currency_a == "UAH":
        if currency_b == "USD" or currency_b == "EUR":
            rate_sell = (
                Rate.objects.filter(currency_a=currency_b, currency_b="UAH", date=today)
                .order_by("sell")
                .first()
            )
            if rate_sell:
                return round(amount_a / rate_sell.sell, 2)
    elif currency_a == "USD" or currency_a == "EUR":
        if currency_b == "UAH":
            rate_buy = (
                Rate.objects.filter(currency_a=currency_a, currency_b="UAH", date=today)
                .order_by("buy")
                .last()
            )
            if rate_buy:
                return round(amount_a * rate_buy.buy, 2)
    return None


def index(request):
    current_date = datetime.date.today()
    current_rates = Rate.objects.filter(date=current_date).all().values()
    return JsonResponse(
        {"current_rates": list(current_rates)}, encoder=DecimalAsFloatJSONEncoder
    )
