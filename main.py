from src.tools.checkBitcoinAddress import CheckBitcoinAddress
from src.config.config import LIST_ADDRESS, BITCOIN_ABUSE_API_TOKEN


def main():
    CBA = CheckBitcoinAddress({
        'p1': LIST_ADDRESS,
        'p2': BITCOIN_ABUSE_API_TOKEN
    })
    CBA.start_signal()
    CBA.colorama_init()
    CBA.ascii_art()
    CBA.check_directory_log()
    while (True):
        CBA.check_address()


if __name__ == '__main__':
    main()
