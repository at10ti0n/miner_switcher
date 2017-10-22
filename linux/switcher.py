import os
import subprocess
import time
import copy
import requests
import configparser
from datetime import datetime
import sys


def config_read ():
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')
    print(str(datetime.now()) + ' - Config have been read successfully')
    return config


def start_miner(info, config):
    zecminer_dir = str(config['Path']['zecminerdir'])
    claymore_dir = str(config['Path']['claymoredir'])
    ccminer_dir = str(config['Path']['ccminerdir'])
    if zecminer_dir != '' and info['algorithm'] == 'Equihash':
        if info['currency'] == 'ZEC' and str(config['Path']['zecbatname']) != '':
            subprocess.Popen(zecminer_dir + config['Path']['zecbatname'], cwd=zecminer_dir)
        elif info['currency'] == 'ZCL' and str(config['Path']['zclbatname']) != '':
            subprocess.Popen(zecminer_dir + config['Path']['zclbatname'], cwd=zecminer_dir)
        elif info['currency'] == 'ZEN' and str(config['Path']['zenbatname']) != '':
            subprocess.Popen(zecminer_dir + config['Path']['zenbatname'], cwd=zecminer_dir)
        elif info['currency'] == 'HUSH' and str(config['Path']['hushbatname']) != '':
            print(config['Path']['hushbatname'])
            subprocess.Popen(zecminer_dir + config['Path']['hushbatname'], cwd=zecminer_dir)
        else:
            print('Miner bat not found. Closing Switcher in 10 sec')
            time.sleep(10)
            sys.exit()
    elif claymore_dir != '' and info['algorithm'] == 'Ethash':
        if info['currency'] == 'ETH' and str(config['Path']['ethbatname']) != '':
            subprocess.Popen(claymore_dir + config['Path']['ethbatname'], cwd=claymore_dir)
        elif info['currency'] == 'ETC' and str(config['Path']['etcbatname']) != '':
            subprocess.Popen(claymore_dir + config['Path']['etcbatname'], cwd=claymore_dir)
        elif info['currency'] == 'MUSIC' and str(config['Path']['musicbatname']) != '':
            subprocess.Popen(claymore_dir + config['Path']['musicbatname'], cwd=claymore_dir)
        elif info['currency'] == 'UBQ' and str(config['Path']['ubqbatname']) != '':
            print(config['Path']['hushbatname'])
            subprocess.Popen(claymore_dir + config['Path']['ubqbatname'], cwd=claymore_dir)
        elif info['currency'] == 'KMD' and str(config['Path']['kmdbatname']) != '':
            print(config['Path']['hushbatname'])
            subprocess.Popen(claymore_dir + config['Path']['kmdbatname'], cwd=claymore_dir)
        elif info['currency'] == 'EXP' and str(config['Path']['expbatname']) != '':
            print(config['Path']['expbatname'])
            subprocess.Popen(claymore_dir + config['Path']['expbatname'], cwd=claymore_dir)
        elif info['currency'] == 'SOIL' and str(config['Path']['soilbatname']) != '':
            print(config['Path']['soilbatname'])
            subprocess.Popen(claymore_dir + config['Path']['soilbatname'], cwd=claymore_dir)
        else:
            print('Miner bat not found. Closing Switcher in 10 sec')
            time.sleep(10)
            sys.exit()
    elif ccminer_dir != '' and info['algorithm'] == 'Lyra2REv2':
        if info['currency'] == 'VTC' and str(config['Path']['vtcbatname']) != '':
            subprocess.Popen(ccminer_dir + config['Path']['vtcbatname'], cwd=ccminer_dir)
        elif info['currency'] == 'MONA' and str(config['Path']['monabatname']) != '':
            print(config['Path']['monabatname'])
            subprocess.Popen(ccminer_dir + config['Path']['monabatname'], cwd=ccminer_dir)
        else:
            print('Miner bat not found. Closing Switcher in 10 sec')
            time.sleep(10)
            sys.exit()
    else:
        print("Check config. You didn't select currency or didn't setup path to miner. Closing Switcher in 10 sec")
        time.sleep(10)
        sys.exit()
    return info


def stop_miner():
    os.system('pkill miner')
    os.system('pkill EthDcrMiner64')


def request_coins(config):
    coins = None
    while coins is None:
        print(str(datetime.now()) + " - Requesting coins info for WhattoMine.com!")
        try:
            coins = (requests.get(url=str(config['UrlPath']['url']) + str(config['UrlPath']['userrates']), timeout=3))
        except:
            print(str(datetime.now()) + " - Site didn't respond. Reconnecting in 10 sec!")
            time.sleep(10)
    if coins is not None and coins.status_code == 200:
            coins = coins.json()['coins']
    else:
        print(str(datetime.now()) + " - WhattoMine.com Server Response isn't OK . Switcher will close in 10 sec")
        time.sleep(10)
        sys.exit()
    if not coins:
        print(str(datetime.now()) + " - You setup wrong UserRates in config file closing in 10 sec")
        time.sleep(10)
        sys.exit()
    else:
        print(str(datetime.now()) + ' - Coins info received successfully')
    return coins


def user_coins_request(config,coins):
    user_coins = {}
    for key, value in config['Currency'].items():
            if value == 'True':
                tag = key.upper()
                for key_coin, value_coin in coins.items():
                    if value_coin['tag'] == tag:
                        user_coins[key_coin] = value_coin
    return user_coins


def update_profit_info(info, user_coins):
    for key, value in user_coins.items():
        if value['tag'] == info['temp_currency']:
            info['temp_profit'] = value['btc_revenue24']
        if value['tag'] == info['currency']:
            info['profit'] = value['btc_revenue24']
    return info


def choosing_currency(user_coins):
    most_profit_currency = {'profit': 0, 'currency': None, 'algorithm': None}
    for key, value in user_coins.items():
        if float(value['btc_revenue24']) > float(most_profit_currency['profit']):
            most_profit_currency['profit'] = value['btc_revenue24']
            most_profit_currency['currency'] = value['tag']
            most_profit_currency['algorithm'] = value['algorithm']
    print(str(datetime.now()) + ' - Most profitable Currency was chosen')
    return most_profit_currency


def miner_chose(config, info):
    coins = request_coins(config)
    user_coins = user_coins_request(config, coins)
    info = update_profit_info(info, user_coins)
    most_profit_currency = choosing_currency(user_coins)
    if float(most_profit_currency['profit']) > float(info['profit']) * \
            (float(config['CheckOptions']['profitprocent'])+ 100) / 100:
        if most_profit_currency['currency'] != info['currency'] and int(info['check_times']) < \
                int(config['CheckOptions']['times']):
            if info['temp_currency'] != most_profit_currency['currency']:
                info['temp_currency'] = most_profit_currency['currency']
                info['check_times'] = 0
            info['check_times'] += 1
            info['temp_profit'] = most_profit_currency['profit']
        if most_profit_currency['currency'] != info['currency'] and int(info['check_times']) >= \
                int(config['CheckOptions']['times']):
            info['profit'] = most_profit_currency['profit']
            info['currency'] = most_profit_currency['currency']
            info['algorithm'] = most_profit_currency['algorithm']
            info['check_times'] = 0
    return info


def start(config):
    check_times = int(config['CheckOptions']['times']) + 1
    info = {'profit': 0, 'check_times': check_times, 'currency': None, 'temp_profit': 0, 'temp_currency': None}
    while True:
        if info['profit'] != 0:
            old_info = copy.deepcopy(info)
            print(old_info)
            info = miner_chose(config, info)
            print(
                str(datetime.now()) + ' - Checking profit. Current currency: ' + info['currency'] + '. Profit: ' + info[
                    'profit'] + ' BTC/Day')
            print(info)
            if info['currency'] != old_info['currency']:
                print('!!!!!!Changing miner!!!!!!!!. Currency ' + info['currency'] + '. Profit: ' + info['profit']
                      + ' BTC/Day')
                start_miner(info, config)
            elif info['currency'] == old_info['currency']:
                print('Continue mining' + info['currency'])
            time.sleep(int(config['CheckOptions']['period']) * 60)
        else:
            info = start_miner(miner_chose(config,info), config)
            print(str(datetime.now()) + " - Starting miner first time. Currency: " + info['currency'] + '. Profit: ' +
                  info['profit'] + ' BTC/Day')
            time.sleep(int(config['CheckOptions']['period']) * 60)


def main():
    stop_miner()
    config = config_read()
    start(config)


if __name__ == '__main__':
    main()



