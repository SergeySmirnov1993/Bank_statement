import requests
import json


NB_API = 'https://nbg.gov.ge/gw/api/ct/monetarypolicy/currencies/en/json/?currencies={}&date={}'


def parce_tbs_statement(sheet):
    data = {}
    for row in sheet.values:
        if row[0] is not None:
            if row[2] == 'Income':
                format_date = f'{row[0].year}-{row[0].month}-{row[0].day}'
                if format_date in data.keys():
                    day_values = data[format_date]
                    currency = day_values.get(row[4])
                    day_values[row[4]] = currency + row[3] if currency else row[3]
                    data[format_date] = day_values
                else:
                    data[format_date] = {row[4]: row[3]}
        else:
            break
    return data


def exchange_rate(currency, date):
    response = requests.get(NB_API.format(currency, date))
    data = json.loads(response.content)
    rate = data[0]['currencies'][0]['rate']
    return rate


def calculate(sheet):
    data = parce_tbs_statement(sheet)
    total = 0
    for day in data.keys():
        for currency, val in data[day].items():
            if currency != 'GEL':
                rate = exchange_rate(currency, day)
                val = val * rate
                total += val
            else:
                total += val
    return total

