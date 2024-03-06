#!/usr/bin/env python3
import http.client
import optparse

import os
import json
import time
import urllib
from urllib.request import Request, urlopen
from random import randrange

_current_address = None
_current_language = None
_default_url = 'http://ddddd.tech:1337/app'
_local_url = 'http://localhost:1337/app'


class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class StrLang:
    TITLE_SELECT_LANG_RU = 'Выберите язык приложения'
    TITLE_SELECT_LANG_EN = 'Select language'


_storage_file = 'd.dat'


def create_account():
    try:
        body = urlopen(Request(
            url,
            json.dumps({
                'method': "createaccount",
                'jsonrpc': "2.0",
                'id': randrange(1000000),
                'params': ["", ""],
            }).encode(),
            headers={
                'Accept': 'application/json',
            },
        )).read().decode()
    except urllib.error.HTTPError as e:
        body = e.read().decode()
    _json = json.loads(body)
    return _json['result']


def get_current_address():
    print('Your address is: ', _current_address)


def get_balance():
    try:
        body = urlopen(Request(
            url,
            json.dumps({
                'method': "getbalance",
                'jsonrpc': "2.0",
                'id': randrange(1000000),
                'params': [_current_address],
            }).encode(),
            headers={
                'Accept': 'application/json',
            },
        )).read().decode()
    except urllib.error.HTTPError as e:
        body = e.read().decode()
    _json = json.loads(body)
    return _json['result']


def send_tx(address_to_send, val_to_send, gas_val, msg):
    try:
        body = urlopen(Request(
            url,
            json.dumps({
                'method': "send_tx",
                'jsonrpc': "2.0",
                'id': randrange(1000000),
                'params': [
                    address_to_send,
                    float(val_to_send),  # value
                    int(gas_val),  # gas
                    msg
                ],
            }).encode(),
            headers={
                'Accept': 'application/json',
            },
        )).read().decode()
    except urllib.error.HTTPError as e:
        body = e.read().decode()  
    _json = json.loads(body)
    transaction_hash = _json['result']['hash']
    print('Transaction hash: ', transaction_hash)
    return transaction_hash


def sign_transaction(signer, transaction_hash):
    try:
        body = urlopen(Request(
            url,
            json.dumps({
                'method': "dumpprivkey",
                'jsonrpc': "2.0",
                'id': randrange(1000000),
                'params': [signer],
            }).encode(),
            headers={
                'Accept': 'application/json',
            },
        )).read().decode()
    except urllib.error.HTTPError as e:
        body = e.read().decode() 
    _json = json.loads(body)
    _k = _json['result']
    time.sleep(3)

    try:
        body = urlopen(Request(
            url,
            json.dumps({
                'method': "signrawtransactionwithkey",
                'jsonrpc': "2.0",
                'id': randrange(1000000),
                'params': [transaction_hash, _k],
            }).encode(),
            headers={
                'Accept': 'application/json',
            },
        )).read().decode()
    except urllib.error.HTTPError as e:
        body = e.read().decode() 
    _json = json.loads(body)
    _tx = _json['result']
    os.system('cls')
    print(f"Transaction with hash: {BColors.WARNING}{_tx}{BColors.ENDC} signed.")


def get_status():
    try:
        body = urlopen(Request(
            url,
            json.dumps({
                'method': "getblockchaininfo",
                'jsonrpc': "2.0",
                'id': randrange(1000000),
                'params': [],
            }).encode(),
            headers={
                'Accept': 'application/json',
            },
        )).read().decode()
    except urllib.error.HTTPError as e:
        body = e.read().decode()
    _json = json.loads(body)
    os.system('cls')
    print(
        f"Current chain network: {BColors.WARNING}{_json['result']['chain']}{BColors.ENDC}. Blocks: {_json['result']['blocks']}. Chainwork: {_json['result']['chainwork']}")


def get_transactions():
    os.system('cls')
    try:
        body = urlopen(Request(
            url,
            json.dumps({
                "method": "get_transactions",
                "jsonrpc": "2.0",
                'id': randrange(1000000),
                "params": [_current_address]
            }).encode(),
            headers={
                'Accept': 'application/json',
            },
        )).read().decode()
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print("Error")
    _json = json.loads(body)
    if _json['result']:
        for tx in _json['result']:
            print(f"{tx}")
    else:
        print(f"There is incoming no transactions")


def faucet():
    try:
        urlopen(Request(
            url,
            json.dumps({
                'method': "faucet",
                'jsonrpc': "2.0",
                'id': randrange(1000000),
                'params': [_current_address],
            }).encode(),
            headers={
                'Accept': 'application/json',
            },
        )).read().decode()
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(body)


def set_lang(lang_type):
    if lang_type == 'en':
        _current_language = 'en'
    if lang_type == 'ru':
        _current_language = 'ru'


def change_lang():
    os.system('cls')
    print(
        f"{BColors.WARNING}{StrLang.TITLE_SELECT_LANG_EN if _current_language == 'en' else StrLang.TITLE_SELECT_LANG_RU}(en|ru): {BColors.ENDC}"
    )
    input_lang_type = input()
    if input_lang_type == 'ru':
        set_lang('ru')
    else:
        set_lang('en')
    os.system('cls')


os.system('cls')

parser = optparse.OptionParser()

parser.add_option('-n', '--network',
                  action="store", dest="url",
                  help="Chain network", default="http://ddddd.tech:1337/app")

options, args = parser.parse_args()

print(f"Using networks: {options.url}")
url = options.url

start = 1
acc = {}
set_lang('en')
if os.path.isfile(_storage_file):
    with open('d.dat', 'r') as fp:
        _current_address = fp.read()

while start > 0:
    print('\r\n'+BColors.WARNING+'DDDDD chain command line client.'+BColors.ENDC+'\r\nCommands are: '
          '\r\n'+BColors.OKGREEN+'address'+BColors.ENDC+' - '
          'Show current address\r\n'+BColors.OKGREEN+'balance'+BColors.ENDC+' - Get balance\r\n'

          ''+BColors.OKGREEN+'create'+BColors.ENDC+' - Create account\r\n'+BColors.OKGREEN+'exit'+''
          ''+BColors.ENDC+'- Exit app\r\n'+BColors.OKGREEN+'faucet'+BColors.ENDC+' - Increase balance\r\n'
          ''+BColors.OKGREEN+'get'+BColors.ENDC+' - Show incoming transactions\r\n'+BColors.OKGREEN+'send'
          ''+BColors.ENDC+' - Send transaction\r\n'+BColors.OKGREEN+'status'+BColors.ENDC+' - Get network status\r\n')
    input_command = input('enter command: ')
    match input_command:
        case "create":
            if not _current_address:
                _current_address = create_account()
                with open(_storage_file, 'w') as fp:
                    fp.write(_current_address)
                os.system('cls')
                print(f"Create account with address: {_current_address}")
            else:
                os.system('cls')
                print(f"Your address is: {BColors.WARNING}{_current_address}{BColors.ENDC}")
        case "address":
            if _current_address:
                os.system('cls')
                print(f"Your address is: {BColors.WARNING}{_current_address}{BColors.ENDC}")
            else:
                os.system('cls')
                print(f"Create account before!")
        case "balance":
            if _current_address:
                balance = get_balance()
                os.system('cls')
                print(f"Your balance is: {balance}")
            else:
                os.system('cls')
                print(f"{BColors.WARNING}Error{BColors.ENDC}")
        case "faucet":
            if _current_address:
                faucet()
                balance = get_balance()
                os.system('cls')
                print(f"Your balance is: {balance}")
            else:
                os.system('cls')
                print(f"{BColors.WARNING}Error{BColors.ENDC}")
        case "get":
            if _current_address:
                os.system('cls')
                get_transactions()
            else:
                os.system('cls')
                print(f"{BColors.WARNING}Error{BColors.ENDC}")
        case "lang":
            change_lang()
        case "send":
            if _current_address:
                address_to = input('to: ')
                value_to_send = input('value: ')
                gas_value = input('gas: ')
                message = input('message (optional): ')
                tx_hash = send_tx(address_to, value_to_send, gas_value, message)
                choise = input('sign transaction? (y/n): ')
                if choise == "y":
                    try:
                        sign_transaction(_current_address, tx_hash)
                    except http.client.RemoteDisconnected as rde:
                        print("Error!")
            else:
                os.system('cls')
                print(f"{BColors.WARNING}Error{BColors.ENDC}")
        case "status":
            get_status()
        case "transactions":
            if _current_address:
                get_transactions()
            else:
                os.system('cls')
                print(f"{BColors.WARNING}Error{BColors.ENDC}")
        case "exit":
            exit("Shoutdown client now...")
        case "xset":
            addr = input('')
            _current_address = addr
            os.system('cls')
        case _:
            os.system('cls')
            print(f"{BColors.FAIL}Wrong commang{BColors.ENDC}")
