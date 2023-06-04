from django import forms
from .models import Rate
import datetime


class RateForm(forms.Form):
    currency_a = forms.ChoiceField(
        choices=[("UAH", "UAH"), ("USD", "USD"), ("EUR", "EUR")],
        label="Выберите валюту:",
    )
    amount_a = forms.DecimalField(label="Сумма обмена:")
    currency_b = forms.ChoiceField(
        choices=[("UAH", "UAH"), ("USD", "USD"), ("EUR", "EUR")], label="Поменять на:"
    )

    def clean(self):
        cleaned_data = super().clean()
        if not Rate.objects.filter(date=datetime.datetime.now().date()).exists():
            raise forms.ValidationError(
                "Нет доступных значений курса для выбранных валют на текущую дату."
            )
        return cleaned_data
