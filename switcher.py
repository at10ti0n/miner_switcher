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
    return config.sections


def start_miner(info):
    if info['algorithm'] == 'Equihash':
        subprocess.Popen('F:\Claymore\start — music — Peon.bat', cwd='F:\Claymore',
                         creationflags=subprocess.CREATE_NEW_CONSOLE)
    elif info['algorithm'] == 'Ethash':
        subprocess.Popen('F:\Claymore\start — music — Peon.bat', cwd='F:\Claymore',
                         creationflags=subprocess.CREATE_NEW_CONSOLE)
    return info


def stop_miner():
    os.system("taskkill /f /t /im  miner.exe")
    os.system("taskkill /f /t /im  EthDcrMiner64.exe")


def request_coins():
    coins = None
    while coins is None:
        try:
            coins = ((requests.get(
                url='https://whattomine.com/coins.json?utf8=✓&eth=true&factor%5Beth_hr%5D=79.0&factor%5Beth_p%5D=0.0&factor%5Bgro_hr%5D=0.0&factor%5Bgro_p%5D=0.0&factor%5Bx11g_hr%5D=20.0&factor%5Bx11g_p%5D=0.0&factor%5Bcn_hr%5D=0.0&factor%5Bcn_p%5D=0.0&eq=true&factor%5Beq_hr%5D=1000.0&factor%5Beq_p%5D=0.0&factor%5Blrev2_hr%5D=80000.0&factor%5Blrev2_p%5D=0.0&factor%5Bns_hr%5D=0.0&factor%5Bns_p%5D=0.0&factor%5Blbry_hr%5D=0.0&factor%5Blbry_p%5D=0.0&factor%5Bbk2b_hr%5D=0.0&factor%5Bbk2b_p%5D=0.0&factor%5Bbk14_hr%5D=0.0&factor%5Bbk14_p%5D=0.0&factor%5Bpas_hr%5D=0.0&factor%5Bpas_p%5D=0.0&bkv=true&factor%5Bbkv_hr%5D=0.0&factor%5Bbkv_p%5D=0.0&factor%5Bcost%5D=0.06&sort=Profitability24&volume=0&revenue=24h&factor%5Bexchanges%5D%5B%5D=&factor%5Bexchanges%5D%5B%5D=bittrex&factor%5Bexchanges%5D%5B%5D=bleutrade&factor%5Bexchanges%5D%5B%5D=btc_e&factor%5Bexchanges%5D%5B%5D=bter&factor%5Bexchanges%5D%5B%5D=c_cex&factor%5Bexchanges%5D%5B%5D=cryptopia&factor%5Bexchanges%5D%5B%5D=poloniex&factor%5Bexchanges%5D%5B%5D=yobit&dataset=Main&commit=Calculate&adapt_q_280x=0&adapt_q_380=0&adapt_q_fury=0&adapt_q_470=0&adapt_q_480=0&adapt_q_750Ti=0&adapt_q_10606=3&adapt_q_1070=0&adapt_q_1080=0&adapt_q_1080Ti=0%27')).json())[
            'coins']
        except:
            print("Site didn't respond. Reconnecting in 10 sec")
            time.sleep(10)
    return coins


def miner_chose(config, info):
    user_coins = {}
    coins = request_coins()
    for key, value in config['Currency'].items():
        if value == 'True':
            tag = key.upper()
            for key_coin, value_coin in coins.items():
                if value_coin['tag'] == info['temp_currency']:
                    info['temp_profit'] = value_coin['btc_revenue24']
                if value_coin['tag'] == info['currency']:
                    info['profit'] = value_coin['btc_revenue24']
                if value_coin['tag'] == tag:
                    user_coins[key_coin] = value_coin
    for key, value in user_coins.items():
        if float(value['btc_revenue24']) >= float(info['profit']) * (float(config['CheckOptions']['profitprocent']) +100) / 100:
            if not info['currency'] == value['tag']:
                if float(value['btc_revenue24']) > float(info['temp_profit']):
                    if not info['temp_currency'] == value['tag']:
                        info['check_times'] = 0
                    info['temp_profit'] = value['btc_revenue24']
                    info['temp_currency'] = value['tag']
                info['check_times'] += 1
                if int(info['check_times']) >= int(config['CheckOptions']['times']):
                    info['profit'] = value['btc_revenue24']
                    info['currency'] = value['tag']
                    info['algorithm'] = value['algorithm']
                    info['check_times'] = 0
    return info


def main():
    info = {'profit': 0, 'check_times': 200, 'currency': None, 'temp_profit': 0, 'temp_currency': None}
    config = config_read()
    a = int(input('Choose action:\n 1. Start script \n 2. Show Config \n 3. Exit \n'))
    while a == 1:
        if info['profit'] == 0:
            stop_miner()
            info = start_miner(miner_chose(config,info))
            print(str(datetime.now()) + " - Starting miner first time. Currency: " + info['currency'] + '. Profit: ' +
                  info['profit'] + ' BTC/Day')
            time.sleep(int(config['CheckOptions']['period']) * 60)
        else:
            old_info = copy.deepcopy(info)
            info = miner_chose(config, info)
            print(old_info)
            print(info)
            print(
                str(datetime.now()) + ' - Checking profit. Current currency: ' + info['currency'] + '. Profit: ' + info[
                    'profit'] + ' BTC/Day')
            if info['currency'] != old_info['currency']:
                print('Changing miner. Currency ' + info['currency'] + '. Profit: ' + info['profit'] + ' BTC/Day')
            elif info['currency'] == old_info['currency']:
                print('Curency SAME')
                # stop_miner()
                # start_miner(info)
            time.sleep(int(config['CheckOptions']['period']) * 60)


if __name__ == '__main__':
    main()



