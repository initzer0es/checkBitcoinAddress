## About checkBitcoinAddress

`Check bitcoin address` is an automated `Python` tool designed to get some abuse information from bitcoin addresses; see screenshot below for more details.

## Screenshots

![checkBitcoinAddress](https://raw.githubusercontent.com/initzer0es/checkBitcoinAddress/master/img/screenshot.png "checkBitcoinAddress in action")

## Installation

```
git clone https://github.com/initzer0es/checkBitcoinAddress.git
```

## Recommended Python Version:

- The recommended version of Python is **3.9.x**

## Dependencies:

checkBitcoinAddress uses the [`blockcypher`](https://github.com/blockcypher/blockcypher-python), [`colorama`](https://github.com/tartley/colorama) and [`requests`](https://github.com/psf/requests) python modules.

The module can be installed using the requirements file:

- Windows:

```
pip install -r requirements.txt
```

- Linux

```
sudo pip install -r requirements.txt
```

## Configurations @`src\config.py`:

`MY_ADDRESS` comma separated bitcoin address.

`REFRESH_SECOND` sleep time in second before refreshing.

`BITCOIN_ABUSE_API_TOKEN` get api token from [bitcoinabuse](https://www.bitcoinabuse.com).

## Usage

```
python main.py
```

## Version

**Current version is 1.1**
