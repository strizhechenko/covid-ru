#!/usr/bin/env python3

import argparse
import re
import sys

import bs4
import requests


def url2soup(url):
    return bs4.BeautifulSoup(requests.get(url).content, "html.parser")


def abc2int(s):
    if ',' not in s:
        return s.replace('млн', '0' * 6)
    s = s.replace('млн', '')
    f = len(s.split(',')[1])
    return s.replace(',', '') + '0' * (6 - f)


def ru(args):
    # url = "https://стопкоронавирус.рф" # https://covid19.rosminzdrav.ru
    soup = url2soup("https://стопкоронавирус.рф")
    stat = soup.find("div", attrs={"class": "cv-countdown"})
    stat_map = {
        'Проведено тестов': 'tests',
        'Случаев заболевания': 'cases',
        'Случая заболевания': 'cases',
        'Случай заболевания': 'cases',
        'Человека выздоровело': 'recovered',
        'Человек выздоровело': 'recovered',
        'Человек выздоровел': 'recovered',
        'Человека умерло': 'dead',
        'Человек умерло': 'dead',
        'Человек умер': 'dead',
    }
    for item in stat.find_all("div", attrs={"class": "cv-countdown__item"}):
        label = re.sub(r"[\t\s]+", " ", item.find("div", attrs={"class": "cv-countdown__item-label"}).text.strip())
        if 'за последние сутки' in label:
            continue
        key = stat_map.get(label)
        if not key:
            print("Didn't find key for label {0}".format(label), file=sys.stderr)
            continue
        if hasattr(args, key) and getattr(args, key):
            value = item.find("div", attrs={"class": "cv-countdown__item-value"}).text.strip().replace(" ", "")
            value = value.replace('>', '')
            if 'млн' in value:
                value = abc2int(value)
            print("{0:10} {1}".format(key, value))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--all", action='store_true', default=False, help='All available stats')
    parser.add_argument("-d", "--dead", action='store_true', default=False, help='How many people died')
    parser.add_argument("-r", "--recovered", action='store_true', default=False, help='How many people recovered')
    parser.add_argument("-t", "--tests", action='store_true', default=False, help='How many tests performed')
    parser.add_argument("-c", "--cases", action='store_true', default=False, help='How many tests were positive')
    args = parser.parse_args()
    if not any([args.all, args.dead, args.recovered, args.tests, args.cases]):
        args.all = True
    if args.all:
        args.dead = args.recovered = args.tests = args.cases = True
    ru(args)


if __name__ == '__main__':
    main()
