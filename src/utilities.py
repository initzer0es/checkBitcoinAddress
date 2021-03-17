from .color import Color as c
from .config import REFRESH_SECOND
from blockcypher import satoshis_to_btc
from datetime import date
from datetime import datetime
import locale
import os
import re
import signal
import sys
import time


class Utilities:
    def __init__(self):
        self._release = 'Check Bitcoin Address v1.1 ~ @initzer0es'
        self._REGEX_PATTERN = [
            'USD","rate":"(.*?)"',
            '{"address":"(.*?)"',
            ',"count":(.*?),',
            ',"last_seen":"(.*?)"',
            "'n_tx': ([0-9]+),",
            "'total_received': ([0-9]+),",
            "'value': ([0-9]+),",
            "datetime\(([0-9]+,\s[0-9]+,\s[0-9]+),",
        ]

    def color(self, string, fore, back=None):
        if (back == None):
            return f'{fore}{string}{c.sReset}'
        return f'{back}{fore}{string}{c.sReset}'

    def exit_program(self):
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

    def signal_handler(self, sigint, handler):
        signal_handler_message = self.color(
            f' CTRL + C (Keyboard interrupt) received, exiting the program... ',
            c.lCyan,
            c.bBlue
        )
        print('%s\n\n' % signal_handler_message)
        self.exit_program()

    def start_signal(self):
        signal.signal(signal.SIGINT, self.signal_handler)

    def set_locale(self):
        locale.setlocale(locale.LC_ALL, '')

    def regex(self, pattern, string):
        try:
            return re.search(pattern, string).group(1)
        except:
            return '?'

    def current_time(self):
        return time.strftime('%d %B %Y - %I:%M:%S %p', time.localtime(time.time()))

    def sleep(self):
        sleep_message = self.color(
            f' Sleep {REFRESH_SECOND} second, before refreshing... ',
            c.black,
            c.bLWhite
        )
        print('%s\n\n' % sleep_message)
        time.sleep(REFRESH_SECOND)

    def convert_time_format(self, string):
        if (string != '?'):
            current_format = datetime.strptime(string, '%Y, %m, %d')
            return date.strftime(current_format, "%Y-%m-%d")
        return string

    def convert_satoshi_to_btc(self, string):
        try:
            return satoshis_to_btc(int(string))
        except:
            return '?'

    def convert_btc_to_usd(self, btc, usd):
        try:
            usd = int(usd.replace(',', ''))
            return f'{round(btc * usd):,}'
        except:
            return '?'

    def get_info(self, string):
        return [self.regex(current_regex_pattern, string) for current_regex_pattern in self._REGEX_PATTERN]

    def get_converted(self, params):
        return ' => %s USD' % self.convert_btc_to_usd(params['usd'], params['btc']) if (params['iszero'] != '0') else ' => ? USD'

    def print_info(self, info, count):
        info_btc = info[0].split('.')[0]
        info_address = info[1]
        info_report = info[2]
        info_last_report = info[3]
        info_transactions = info[4]
        info_total = self.convert_satoshi_to_btc(info[5])
        info_last_transactions = self.convert_satoshi_to_btc(info[6])
        info_date_last_transactions = self.convert_time_format(info[7])
        info_last_1 = info_last_2 = ''
        has_info_last = False
        convert_total = self.get_converted({
            'usd': info_total,
            'btc': info_btc,
            'iszero': info_transactions,
        })
        if (info_transactions != '0'):
            convert_last = self.get_converted({
                'usd': info_last_transactions,
                'btc': info_btc,
                'iszero': info_transactions,
            })
            info_last_1 = '        Last Transactions: '
            info_last_2 = f' {info_last_transactions} BTC{convert_last} [{info_date_last_transactions}] '
            has_info_last = True
        strings_info = {
            'si1': self.color(f'[{self.current_time()}]{c.sReset}', c.lBlack),
            'si2': self.color('->', c.lWhite),
            'si3': self.color(f' {self._release} ', c.black, c.bLBlack),
            'si4': self.color(f' #{count} ', c.lWhite, c.bMagenta),
            'si5': self.color(f' https://www.bitcoinabuse.com/reports/{info_address} ', c.lYellow, c.bRed),
            'si6': self.color('{', c.lWhite),
            'si7': self.color(f'        Current BTC Price: ', c.lYellow),
            'si8': self.color(f' {info_btc} USD ', c.black, c.bLYellow),
            'si9': self.color(f'             Report Count: ', c.red),
            'si10': self.color(f' {info_report} ', c.black, c.bRed),
            'si11': self.color(f'              Last Report: ', c.lRed),
            'si12': self.color(f' {info_last_report} ', c.black, c.bLRed),
            'si13': self.color(f'    Transactions (in-out): ', c.yellow),
            'si14': self.color(f' {info_transactions} ', c.black, c.bYellow),
            'si15': self.color(f'           Total Received: ', c.green),
            'si16': self.color(f' {info_total} BTC{convert_total} ', c.black, c.bGreen),
            'si17': self.color(info_last_1, c.lCyan),
            'si18': self.color(info_last_2, c.black, c.bLCyan),
            'si19': self.color('}', c.lWhite),
        }
        print(('%s ' * 3) % (
            strings_info['si1'],
            strings_info['si2'],
            strings_info['si3'],
        ))
        print('\n%s %s' % (
            strings_info['si4'],
            strings_info['si5'],
        ))
        print(strings_info['si6'])
        print(('%s%s,\n' * 5) % (
            strings_info['si7'],
            strings_info['si8'],
            strings_info['si9'],
            strings_info['si10'],
            strings_info['si11'],
            strings_info['si12'],
            strings_info['si13'],
            strings_info['si14'],
            strings_info['si15'],
            strings_info['si16'],
        ), end='')
        if (has_info_last):
            print('%s%s,' % (
                strings_info['si17'],
                strings_info['si18'],
            ))
        print(f"{strings_info['si19']}\n\n")

    def ascii_art(self):
        ascii_art = r'''
    _______           __     ___  _ __           _        ___     __   __
   / ___/ /  ___ ____/ /__  / _ )(_) /________  (_)__    / _ |___/ /__/ /______ ___ ___
  / /__/ _ \/ -_) __/  '_/ / _  / / __/ __/ _ \/ / _ \  / __ / _  / _  / __/ -_|_-<(_-<
  \___/_//_/\__/\__/_/\_\ /____/_/\__/\__/\___/_/_//_/ /_/ |_\_,_/\_,_/_/  \__/___/___/

'''
        message_ascii_art = self.color(ascii_art, c.lMagenta)
        print(message_ascii_art)
