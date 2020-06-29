#!/usr/bin/env python3

import requests


def main():
    data = requests.get("https://covid19.rosminzdrav.ru/wp-json/api/mapdata/").json()
    total = {
        'Recovered': 0,
        'Deaths': 0,
        'Observations': 0,
        'Confirmed': 0
    }
    for i in data['Items']:
        for key in total.keys():
            total[key] += i[key]
    total['Sick'] = total['Confirmed'] - total['Deaths'] - total['Recovered']
    total['Solved'] = "{0:.2f}%".format(100 * (1 - (total['Sick'] / total['Confirmed'])))
    return total


if __name__ == '__main__':
    for _key, _value in main().items():
        print("{0:12} {1}".format(_key, _value))
