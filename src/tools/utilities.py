from ..config.config import REFRESH_SECONDS
from .colorama import Colorama, init
import json
import os
import platform
import re
import requests
import signal
import sys
import time


class Utilities:
    def __init__(self):
        self.__session = requests.Session()
        self.__headers = {
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-US,en;q=0.9',
        }
        self.__current_os = platform.system().lower()
        self.__directory_separator = self.set_directory_separator()
        self.__directory_log = f'.{self.__directory_separator}log{self.__directory_separator}'
        self.__release_name = 'Check Bitcoin Address v1.3 ~ @initzer0es'
        self.__empty = '?'

    def request(self, p):
        url = p['url']
        header = p['headers']
        params = p['params']
        self.__headers.update(header)
        try:
            return self.__session.get(url, headers=self.__headers, params=params).text
        except:
            return self.__empty

    def colorama_init(self):
        if (self.__current_os != 'linux'):
            init()

    def set_directory_separator(self):
        return '/' if ('linux' == self.__current_os) else '\\'

    def set_color(self, string, fore, back=None):
        if (back == None):
            return f'{fore}{string}{Colorama.S_Reset}'
        return f'{back}{fore}{string}{Colorama.S_Reset}'

    def get_release_name(self):
        return self.__release_name

    def get_empty(self):
        return self.__empty

    def exit_program(self):
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

    def signal_handler(self, sigint, handler):
        signal_handler_string = self.set_color(
            ' CTRL + C (keyboard interrupt) received, exiting the program... ',
            Colorama.L_Cyan,
            Colorama.B_Blue
        )
        print(signal_handler_string)
        self.exit_program()

    def start_signal(self):
        signal.signal(signal.SIGINT, self.signal_handler)

    def check_directory_log(self):
        if (not os.path.exists(self.__directory_log)):
            os.makedirs(self.__directory_log)

    def write_log(self, filename, json_data):
        with open(f'{self.__directory_log}{filename}.json', 'w') as file:
            json.dump(json_data, file, indent=4)

    def regex(self, pattern, string, as_list=False):
        try:
            if (as_list):
                list_regex = re.findall(pattern, string)
                return self.__empty if (len(list_regex) == 0) else list_regex
            return re.search(pattern, string).group(1)
        except:
            return self.__empty

    def sleep(self):
        sleep_string = self.set_color(
            f" Sleep {REFRESH_SECONDS} seconds, before updating info... ",
            Colorama.Black,
            Colorama.B_L_White
        )
        print(f'{sleep_string}\n')
        time.sleep(REFRESH_SECONDS)

    def current_time(self):
        return time.strftime('%d %B %Y - %I:%M:%S %p', time.localtime(time.time()))

    def display_info(self, variable, transactions):
        print(('%s ' * 3) % (
            variable['s1'],
            variable['s2'],
            variable['s3'],
        ))
        print('\n%s %s' % (
            variable['s4'],
            variable['s5'],
        ))
        print(variable['s6'])
        print(('%s%s,\n' * 5) % (
            variable['s7'],
            variable['s8'],
            variable['s9'],
            variable['s10'],
            variable['s11'],
            variable['s12'],
            variable['s13'],
            variable['s14'],
            variable['s15'],
            variable['s16'],
        ), end='')
        if (transactions != '0'):
            print('%s%s,' % (
                variable['s17'],
                variable['s18'],
            ))
        print('%s\n' % variable['s19'])

    def ascii_art(self):
        ascii_art = r'''
    _______           __     ___  _ __           _        ___     __   __
   / ___/ /  ___ ____/ /__  / _ )(_) /________  (_)__    / _ |___/ /__/ /______ ___ ___
  / /__/ _ \/ -_) __/  '_/ / _  / / __/ __/ _ \/ / _ \  / __ / _  / _  / __/ -_|_-<(_-<
  \___/_//_/\__/\__/_/\_\ /____/_/\__/\__/\___/_/_//_/ /_/ |_\_,_/\_,_/_/  \__/___/___/

'''
        string_ascii_art = self.set_color(ascii_art, Colorama.L_Magenta)
        print(string_ascii_art)
