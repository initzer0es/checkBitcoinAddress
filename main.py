from src.checkBitcoinAddress import CheckBitcoinAddress
from src.color import colorama_init
from src.config import MY_ADDRESS, BITCOIN_ABUSE_API_TOKEN
from src.utilities import Utilities


colorama_init()
U = Utilities()


def main():
    U.start_signal()
    U.set_locale()
    CBA = CheckBitcoinAddress(MY_ADDRESS, BITCOIN_ABUSE_API_TOKEN)
    while True:
        CBA.check_address()
        U.sleep()


if __name__ == '__main__':
    U.ascii_art()
    main()
