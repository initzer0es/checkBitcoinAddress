from .utilities import Utilities, Colorama


class CheckBitcoinAddress(Utilities):
    def __init__(self, params):
        super().__init__()
        self.__list_address = params['p1']
        self.__api_token = params['p2']
        self.__count = None
        self.__address = None
        self.__response = None
        self.__json_data = None
        self.__list_info_1 = None
        self.__list_info_2 = None
        self.__list_info_3 = None
        self.__list_info_4 = None
        self.__report_count = None
        self.__last_report = None
        self.__transactions = None
        self.__total_received = None
        self.__last_transactions = None
        self.__btc_price = None
        self.__list_pattern_abuse = [
            '"created_at":"(.*?)"',
            '"abuse_type_id":([0-9]+),',
            '"abuse_type_other":(.*?),',
            '"description":"(.*?)","created_at"',
        ]
        self.__list_pattern_other = [
            '"count":([0-9]+),',
            '"last_seen":"(.*?)"',
            'transacted (.*) times on the Bitcoin blockchain.',
            'total of ([0-9]+.[0-9]+) BTC .* and',
            r'opacity="1">(\+[0-9]+.[0-9]+|\-[0-9]+.[0-9]+) BTC<\/span>',
        ]
        self.__pattern_btc_price = r'"USD","rate":"([0-9]+|[0-9]+,[0-9]+)\.'

    def set_response(self, list_params):
        self.__response = ''
        for params in list_params:
            self.__response += super().request(params)

    def clean_date_time(self, string):
        if (string != super().get_empty()):
            list_split_string = string.split('T')
            date = list_split_string[0]
            time = list_split_string[1].split('.')[0]
            return f'{date} {time}'

    def set_abuse_type(self, type):
        ret = {
            '1': 'Ransomware',
            '2': 'Darknet Market',
            '3': 'Bitcoin Tumbler',
            '4': 'Blackmail Scam',
            '5': 'Sextortion',
        }
        return ret.get(type, 'Other')

    def set_abuse_info(self):
        list_abuse_info = []
        for pattern in self.__list_pattern_abuse:
            list_abuse_info.append(
                super().regex(
                    pattern,
                    self.__response,
                    True
                )
            )
        self.__list_info_1 = list_abuse_info[0]
        self.__list_info_2 = list_abuse_info[1]
        self.__list_info_3 = list_abuse_info[2]
        self.__list_info_4 = list_abuse_info[3]

    def set_json_data(self):
        self.__json_data = {}
        self.__json_data[self.__address] = []
        self.set_abuse_info()
        for i in range(len(self.__list_info_3)):
            created_at = self.clean_date_time(self.__list_info_1[i])
            abuse_type = self.set_abuse_type(self.__list_info_2[i])
            abuse_type_other = self.__list_info_3[i]
            description = self.__list_info_4[i]
            self.__json_data[self.__address].append({
                'created_at': created_at,
                'abuse_type': abuse_type,
                'abuse_type_other': abuse_type_other,
                'description': description
            })

    def set_other_info(self):
        list_other_info = []
        for pattern in self.__list_pattern_other:
            list_other_info.append(
                super().regex(
                    pattern,
                    self.__response
                )
            )
        self.__report_count = list_other_info[0]
        self.__last_report = list_other_info[1]
        self.__transactions = list_other_info[2]
        self.__total_received = list_other_info[3]
        self.__last_transactions = list_other_info[4]

    def set_btc_price(self):
        self.__btc_price = super().regex(self.__pattern_btc_price, self.__response)

    def convert_btc_to_usd(self, btc):
        try:
            btc = float(btc)
            usd = int(self.__btc_price.replace(',', ''))
            value = round(btc * usd)
            return f'{value:,}'
        except:
            return '?'

    def get_converted_value(self, as_received):
        if (as_received):
            return self.convert_btc_to_usd(self.__total_received)
        return self.convert_btc_to_usd(self.__last_transactions)

    def set_all_info(self):
        list_string_info = [
            f'[{super().current_time()}]',
            '->',
            f' {super().get_release_name()} ',
            f' #{self.__count} ',
            f' https://www.bitcoinabuse.com/reports/{self.__address} ',
            '{',
            '        Current BTC Price: ',
            f' {self.__btc_price} USD ',
            '             Report Count: ',
            f' {self.__report_count} ',
            '              Last Report: ',
            f' {self.__last_report} ',
            '    Transactions (in-out): ',
            f' {self.__transactions} ',
            '           Total Received: ',
            f' {self.__total_received} BTC => {self.get_converted_value(True)} USD ',
            '        Last Transactions: ',
            f' {self.__last_transactions} BTC => {self.get_converted_value(False)} USD ',
            '}',
        ]
        self.__string_info = {
            's1': self.set_color(list_string_info[0], Colorama.L_Black),
            's2': self.set_color(list_string_info[1], Colorama.L_White),
            's3': self.set_color(list_string_info[2], Colorama.Black, Colorama.B_L_Black),
            's4': self.set_color(list_string_info[3], Colorama.L_White, Colorama.B_Magenta),
            's5': self.set_color(list_string_info[4], Colorama.L_Yellow, Colorama.B_Red),
            's6': self.set_color(list_string_info[5], Colorama.L_White),
            's7': self.set_color(list_string_info[6], Colorama.L_Yellow),
            's8': self.set_color(list_string_info[7], Colorama.Black, Colorama.B_L_Yellow),
            's9': self.set_color(list_string_info[8], Colorama.Red),
            's10': self.set_color(list_string_info[9], Colorama.Black, Colorama.B_Red),
            's11': self.set_color(list_string_info[10], Colorama.L_Red),
            's12': self.set_color(list_string_info[11], Colorama.Black, Colorama.B_L_Red),
            's13': self.set_color(list_string_info[12], Colorama.Yellow),
            's14': self.set_color(list_string_info[13], Colorama.Black, Colorama.B_Yellow),
            's15': self.set_color(list_string_info[14], Colorama.Green),
            's16': self.set_color(list_string_info[15], Colorama.Black, Colorama.B_Green),
            's17': self.set_color(list_string_info[16], Colorama.L_Cyan),
            's18': self.set_color(list_string_info[17], Colorama.Black, Colorama.B_L_Cyan),
            's19': self.set_color(list_string_info[18], Colorama.L_White),
        }

    def check_address(self):
        self.__count = 1
        for address in self.__list_address:
            self.__address = address
            self.set_response([
                {
                    'url': 'https://www.bitcoinabuse.com/api/reports/check',
                    'headers': {
                        'authority': 'www.bitcoinabuse.com',
                        'sec-fetch-site': 'none',
                    },
                    'params': (
                        ('address', self.__address),
                        ('api_token', self.__api_token),
                    )
                },
                {
                    'url': f'https://www.blockchain.com/btc/address/{self.__address}',
                    'headers': {
                        'authority': 'www.blockchain.com',
                        'cache-control': 'max-age=0',
                        'sec-fetch-site': 'same-origin',
                    },
                    'params': None
                },
                {
                    'url': 'https://api.coindesk.com/v1/bpi/currentprice/USD.json',
                    'headers': {
                        'authority': 'api.coindesk.com',
                        'cache-control': 'max-age=0',
                        'sec-fetch-site': 'none',
                    },
                    'params': None
                }
            ])
            self.set_json_data()
            self.set_other_info()
            self.set_btc_price()
            self.set_all_info()
            super().display_info(self.__string_info, self.__transactions)
            super().write_log(self.__address, self.__json_data)
            self.__count += 1
        super().sleep()
