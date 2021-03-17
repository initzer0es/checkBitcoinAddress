from .utilities import Utilities
from blockcypher import get_address_details
import requests


class CheckBitcoinAddress:
    def __init__(self, my_address, bitcoin_abuse_api_token):
        self._SESSION = requests.Session()
        self._MY_ADDRESS = my_address
        self._API_TOKEN = bitcoin_abuse_api_token

    def get(self, params):
        headers = {
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
        headers.update(params['headers'])
        try:
            return self._SESSION.get(params['url'], headers=headers, params=params['params']).text
        except:
            return '?'

    def check_address(self):
        U = Utilities()
        count = 1
        for current_address in self._MY_ADDRESS:
            list_of_params = [
                {
                    'url': 'https://www.bitcoinabuse.com/api/reports/check',
                    'headers': {
                        'authority': 'www.bitcoinabuse.com',
                        'sec-fetch-site': 'none',
                    },
                    'params': (
                        ('address', current_address),
                        ('api_token', self._API_TOKEN),
                    ),
                },
                {
                    'url': 'https://api.coindesk.com/v1/bpi/currentprice/USD.json',
                    'headers': {
                        'authority': 'api.coindesk.com',
                        'cache-control': 'max-age=0',
                        'sec-fetch-site': 'none',
                    },
                    'params': None,
                }
            ]
            response = str(get_address_details(current_address))
            for current_param in list_of_params:
                response += self.get(current_param)
            info = U.get_info(response)
            U.print_info(info, count)
            count += 1
