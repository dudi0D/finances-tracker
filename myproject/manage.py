#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading
import time


def update_currency_rates():
    import requests
    import json
    from users.serializers import CurrenciesSerializer

    response = requests.get("https://www.cbr-xml-daily.ru/latest.js")
    data = json.loads(response.content)
    usd_rate = data['rates']['USD']
    eur_rate = data['rates']['EUR']
    usd_serializer = CurrenciesSerializer(data={
        'name': 'USD',
        'base': 'RUB',
        'rate': usd_rate
    })
    eur_serializer = CurrenciesSerializer(data={
        'name': 'EUR',
        'base': 'RUB',
        'rate': eur_rate
    })
    if usd_serializer.is_valid():
        usd_serializer.save()
    if eur_serializer.is_valid():
        eur_serializer.save()


def update_currency_rates_periodically(interval_seconds=3600):
    def run():
        while True:
            update_currency_rates()
            time.sleep(interval_seconds)
    thread = threading.Thread(target=run, daemon=True)
    thread.start()


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

    # Запуск Django
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Проверка, нужно ли запускать обновление курсов
    if len(sys.argv) > 1 and sys.argv[1] == "runserver":
        update_currency_rates_periodically()

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()