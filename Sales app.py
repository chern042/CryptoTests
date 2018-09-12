import urllib.request
import requests
from bs4 import BeautifulSoup
import json


difficultyList = []
cryptoDic = {}
cryptoDicList = []
cryptoData = ["totalHashes","BlockTime","BlockAmt","algorithm"]

cryptoPage = 'https://whattomine.com/coins.json'
#page = urllib.request.urlopen(cryptoPage)
page = requests.get(cryptoPage).text
#data = json.load(requests.get(cryptoPage))#.text)
soup = BeautifulSoup(page, 'html.parser')
test = json.loads(str(soup))
for i,b in test.items():
    for c in b.items():
        cryptoDic["Name"] = c[0]
        for w in c[1].items():
            if w[0] == "algorithm":
                cryptoDic["Algorithm"]=w[1]
            if w[0] == "block_time":
                cryptoDic["BlockTime"]=w[1]
            if w[0] == "block_reward":
                cryptoDic["RewardAmount"]=w[1]
            if w[0] == "nethash":
                cryptoDic["NetHash"]=w[1]
            if w[0] == "exchange_rate":
                cryptoDic["BTCRate"]=w[1]

        cryptoDicList.append(cryptoDic)
        cryptoDic = {}
#print(cryptoDicList)

'''
#difficulty_box = soup.find_all(class_='small_text')
#cryptoName = soup.find_all('div',style="margin-left: 50px")

for i in cryptoName:
    i.text.strip()
    print(i)
    print()

for i in difficulty_box:
    i.text.strip()
    if str(i).find("/s") != -1: 
        difficultyList.append(str(i)[24:len(str(i))-6])

for i in difficultyList[:20]:
    i = i[:i.find("<")]# + i[i.find(">")+1:]
    #print(i)
'''
def bestHashTime(hashRate,listOfCrypto,algo):
    #daysToBlock = 2100000000
    profit = 0
    for i in listOfCrypto:
        if str(i["Name"]).find("Nicehash") == -1 and str.upper(i["Algorithm"]) == str.upper(algo):
            secondsToBlock = ((float(i["NetHash"])/float(hashRate)) * float(i["BlockTime"]))
            hoursToBlock = (secondsToBlock/60)/60
            print("DaysToBlock",hoursToBlock/24)
            blocksPerDay = 1/(hoursToBlock/24)
            print("BlocksPerDay:",blocksPerDay)
            print(i["Name"])
            print("NetHash",i["NetHash"])
            print("BTCRate",i["BTCRate"])
            print("Blocktime",i["BlockTime"])
            print("RewardAMT",i["RewardAmount"])
            print("fgfgf:")
            profitPerDay = blocksPerDay*i["RewardAmount"]*i["BTCRate"]
            print("ProfitPerDay",profitPerDay)
            #print(profitPerDay)
            if profitPerDay > profit:
                profit = profitPerDay
                winningCrypto = i["Name"]+", "+i["Algorithm"]+", Profit in BTC per day:"+str(profit)
    print (winningCrypto)
    return (winningCrypto)





test = float(input("Please input hashrate"))
algo = input("Please input algorithm type")
print ("Best hash time in days for",algo,"coins:",bestHashTime(test,cryptoDicList,algo))
print(len(cryptoDicList))
