How to correct setup the config file

DON'T FORGET IN YOUR USERRATES CHANGE '%' TO '%%' OR SWITCHER WILL SEND ERRORS IF FUTURE IT SCRIPT WILL BE INTERESTING FOR
ANYBODDY WILL DO THIS AUTOMATIC.

[Currency]
//ETH: False
//ETC: False
//ZCL: False
//ZEC: False
//ZEN: False
//MUSIC: False
//UBQ: False
//KMD: False
//HUSH: False
//EXP: True
//SOIL: False

If set to True script will check this currency for profit info

[CheckOptions]
//Times: 2
//Period: 1
//ProfitProcent: 0

Times - how many successfully times(profit is bigger then you mining currently) will be check till switcher change the miner
Period - Period of time between each check in minutes (min 1 / max unlimited)
ProfitProcent - difference between currency which is mining and new one
    Example:
    current profit = 0,1 BTC/DAY,
    ProfitProcent - 10 (mean 10%),
    New currency profit  must be bigger then 0,1*110% = 0.11)
    only if new currency profit will be bigger then 0.11 BTC/DAY switcher will change mining
    Don't put value 0 it may cause very often mining switching.

[Path]
//ClaymoreDir: - path to Claymore (ETHHASH) example: F:\Claymore\
//ZecMinerDir: - path to ZECminer (Nvidia -Equihash, won't stop ZEC AMD miner - maybe in future will add support if someone will need) example: F:\Claymore\
//ETHbatname: - name of bat ETH example: ETH-ethermine.bat
//ZCLbatname:  - name to bat ZCL example: ZCLstart.bat
//ETCbatname:  - name to bat ETC
//ZECbatname: - etc.


[UrlPath]
//Url: https://whattomine.com/coins.json? - don't change this!
//UserRates: - here put your search request for Whattomine.com which start fro utf8 ..

example:
 search request from Whattomine.com  looks like:
    https://whattomine.com/coins?utf8=?&eth=true&factor%5Bet....................
  You need to take all symbols starts from utf8 and paste to UserRates:
    utf8=?&eth=true&factor%5Bet....................

Save and start.