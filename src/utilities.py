from .color import Color as c
from .config import REFRESH_SECOND
import json
import locale
import os
import re
import signal
import sys
import time


class Utilities:
    def __init__(self):
        self._release = 'Check Bitcoin Address v1.2 ~ @initzer0es'
        self._REGEX_PATTERN = [
            'USD","rate":"(.*?)"',
            '{"address":"(.*?)"',
            ',"count":(.*?),',
            ',"last_seen":"(.*?)"',
            'Transactions<\/span><\/div><\/.*?opacity="1">([0-9]+)<\/span>',
            'Total Received<\/span><\/div><\/.*?opacity="1">(.*?)<\/span>',
            'opacity="1">([0-9].[0-9]+\sBTC)<\/span><a',
            'opacity="1">([0-9]+-[0-9]+-[0-9]+)',
            '"abuse_type_id":([0-9]+),',
            '"abuse_type_other":(.*?),',
            '"description":"(.*?)","created_at',
            '"created_at":"(.*?)"',
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

    def regex(self, pattern, string, as_list=False):
        try:
            return re.findall(pattern, string) if (as_list) else re.search(pattern, string).group(1)
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

    def convert_btc_to_usd(self, btc, usd):
        try:
            btc = float(btc.split(' ')[0])
            usd = int(usd.replace(',', ''))
            return f'{round(btc * usd):,}'
        except:
            return '?'

    def get_info(self, string):
        return [self.regex(current_regex_pattern, string) for current_regex_pattern in self._REGEX_PATTERN]

    def get_converted(self, params):
        return ' => %s USD' % self.convert_btc_to_usd(params['usd'], params['btc']) if (params['iszero'] != '0') else ' => ? USD'

    def get_abuse_type(self, type):
        ret = {
            '1': 'Ransomware',
            '2': 'Darknet Market',
            '3': 'Bitcoin Tumbler',
            '4': 'Blackmail Scam',
            '5': 'Sextortion',
        }
        return ret.get(type, 'Other')

    def clean_created_at(self, string):
        date = string.split('T')[0]
        time = string.split('T')[1].split('.')[0]
        return f'{date} {time}'

    def get_json_data(self, current_address, string):
        data = {}
        data[current_address] = []
        abuse_type_id = self.regex(self._REGEX_PATTERN[8], string, True)
        abuse_type_other = self.regex(self._REGEX_PATTERN[9], string, True)
        description = self.regex(self._REGEX_PATTERN[10], string, True)
        created_at = self.regex(self._REGEX_PATTERN[11], string, True)
        for i in range(len(abuse_type_id)):
            current_created_at = self.clean_created_at(created_at[i])
            current_abuse_type = self.get_abuse_type(abuse_type_id[i])
            current_abuse_type_other = abuse_type_other[i]
            current_description = description[i]
            data[current_address].append({
                'created_at': current_created_at,
                'abuse_type': current_abuse_type,
                'abuse_type_other': current_abuse_type_other,
                'description': current_description
            })
        return data

    def write_log(self, current_address, json_data):
        from .color import LOG_DIRECTORY
        if (not os.path.exists(LOG_DIRECTORY)):
            os.makedirs(LOG_DIRECTORY)
        with open(f'{LOG_DIRECTORY}{current_address}.txt', 'w') as file:
            json.dump(json_data, file, indent=4)

    def print_info(self, info, count):
        info_btc = info[0].split('.')[0]
        info_address = info[1]
        info_report = info[2]
        info_last_report = info[3]
        info_transactions = info[4]
        info_total = info[5]
        info_last_transactions = info[6]
        info_date_last_transactions = info[7]
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
            info_last_2 = f' {info_last_transactions}{convert_last} [{info_date_last_transactions}] '
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
            'si16': self.color(f' {info_total}{convert_total} ', c.black, c.bGreen),
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
