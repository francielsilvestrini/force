#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

class Utils(object):
    datetime_format = '%Y-%m-%d %H:%M:%S'
    date_format = '%Y-%m-%d'

    @staticmethod
    def strtodatetime(datetime_str):
        datetime_str = datetime_str.replace(' ', '-')
        datetime_str = datetime_str.replace(':', '-')
        dt_list = datetime_str.split('-')

        fmt = Utils.datetime_format.replace(' ', '-')
        fmt = fmt.replace(':', '-')
        fmt = fmt.replace('%', '')
        fmt_list = fmt.split('-')

        d = {}
        for i, k in enumerate(fmt_list):
            d[k] = int(dt_list[i])

        return datetime(d['Y'], d['m'], d['d'], d['H'], d['M'], d['S'])

    @staticmethod
    def current_datetime_str():
        return datetime.today().strftime(Utils.datetime_format)

    @staticmethod
    def current_date_str():
        return datetime.today().strftime(Utils.date_format)
