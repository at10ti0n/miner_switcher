import os
import subprocess
import time
import copy
import requests
import configparser
from datetime import datetime


def config_read ():
    config = configparser.ConfigParser()
    config.read('config.ini')
    print('Config have be read')
    return config.sections


def start_miner(info):
    if info['algorithm'] == 'Equihash':
        subprocess.Popen('F:\Miner\sfypool.bat', cwd='F:\Miner',
                         creationflags=subprocess.CREATE_NEW_CONSOLE)
    elif info['algorithm'] == 'Ethash':
        subprocess.Popen('F:\Miner\sypool.bat', cwd='F:\Miner',
                         creationflags=subprocess.CREATE_NEW_CONSOLE)
    return info


def stop_miner():
    os.system("taskkill /f /t /im  miner.exe")
    os.system("taskkill /f /t /im  EthDcrMiner64.exe")


def request_coins(config):
    coins = None
    while coins is None:
        try:
            coins = ((requests.get(url=str(config['UrlPath']['url']) + str(config['UrlPath']['userrates']))).json())['coins']
        except:
            print("Site didn't respond. Reconnecting in 10 sec")
            time.sleep(10)
    if coins is not None:
        print('Coins received correctly')
    return coins


def user_coins_request(config,coins):
    user_coins = {}
    for key, value in config['Currency'].items():
        if value == 'True':
            tag = key.upper()
            for key_coin, value_coin in coins.items():
                if value_coin['tag'] == tag:
                    user_coins[key_coin] = value_coin
    if user_coins != {}:
        print('User Coins updated correctly')
    return user_coins


def update_profit_info(info, user_coins):
    for key, value in user_coins.items():
        if value['tag'] == info['temp_currency']:
            info['temp_profit'] = value['btc_revenue24']
            print('Temp Profit updated')
        if value['tag'] == info['currency']:
            info['profit'] = value['btc_revenue24']
            print('Current Profit updated')
    return info


def choosing_currency(user_coins):
    most_profit_currency = {'profit': 0, 'currency': None, 'algorithm': None}
    for key, value in user_coins.items():
        if float(value['btc_revenue24']) > float(most_profit_currency['profit']):
            most_profit_currency['profit'] = value['btc_revenue24']
            most_profit_currency['currency'] = value['tag']
            most_profit_currency['algorithm'] = value['algorithm']
            print('Most profitable Currency was chosen. Currency: ' + str(most_profit_currency['currency'])+'. Profit '
                  + str(most_profit_currency['profit']))
    return most_profit_currency


def miner_chose(config, info):
    coins = request_coins(config)
    user_coins = user_coins_request(config, coins)
    info = update_profit_info(info, user_coins)
    most_profit_currency = choosing_currency(user_coins)
    if float(most_profit_currency['profit']) > float(info['profit']) * (float(config['CheckOptions']['profitprocent'])
                                                                            + 100) / 100:
        info['profit'] = most_profit_currency['profit']
        info['currency'] = most_profit_currency['currency']
        info['algorithm'] = most_profit_currency['algorithm']
        # info['temp_profit'] = most_profit_currency['profit']
        # info['temp_currency'] = most_profit_currency['currency']

    return info


def main():
    info = {'profit': 0, 'check_times': 200, 'currency': None, 'temp_profit': 0, 'temp_currency': None}
    config = config_read()
    while True:
        old_info = copy.deepcopy(info)
        if info['profit'] == 0:
            stop_miner()
            info = start_miner(miner_chose(config,info))
            print(str(datetime.now()) + " - Starting miner first time. Currency: " + info['currency'] + '. Profit: ' +
                  info['profit'] + ' BTC/Day')
            time.sleep(int(config['CheckOptions']['period']) * 60)
        else:
            info = miner_chose(config, info)
            print(old_info)
            print(info)
            print(
                str(datetime.now()) + ' - Checking profit. Current currency: ' + info['currency'] + '. Profit: ' + info[
                    'profit'] + ' BTC/Day')
            if info['currency'] != old_info['currency']:
                print('Changing miner. Currency ' + info['currency'] + '. Profit: ' + info['profit'] + ' BTC/Day')
            elif info['currency'] == old_info['currency']:
                print('Currency SAME')
            time.sleep(int(config['CheckOptions']['period']) * 60)


if __name__ == '__main__':
    main()



