import requests
from bs4 import BeautifulSoup
import json
import time


cryptoDic = {}
cryptoDicList = []
cryptoData = ["ID","TAG","ALGORITHM"]
workingNameList = []
workingHashList = []
dontPass = False




def backspace(n):
    # print((b'\x08').decode(), end='')     # use \x08 char to go back
    for i in range(n):
        return '\r'         # use '\r' to go back


cryptoPage = 'https://whattomine.com/calculators.json'
#page = urllib.request.urlopen(cryptoPage)
page = requests.get(cryptoPage).text
#data = json.load(requests.get(cryptoPage))#.text)
soup = BeautifulSoup(page, 'html.parser')
test = json.loads(str(soup))
for i,b in test.items():
    for c in b.items():
        cryptoDic["Name"] = c[0]
        for w in c[1].items():
            try:
                if w[0] == "id":
                    cryptoDic["ID"]=w[1]
                if w[0] == "tag":
                    cryptoDic["TAG"]=w[1]
                if w[0] == "algorithm":
                    cryptoDic["ALGORITHM"]=w[1]
            except:
                pass
            try:
                if str(w[0]) == "lagging" and str(w[1])=="True":
                    dontPass = True
            except:
                pass
        if dontPass == False:
            cryptoDicList.append(cryptoDic)
        dontPass = False
        cryptoDic = {}

print(len(cryptoDicList))
for i in cryptoDicList:
    currentPage = "http://whattomine.com/coins/"+str(i['ID'])+".json"
    try:
        page = json.loads(requests.get(currentPage).text)
    except:
        print (str(i['ID']))
    if len(page) != 1:
        workingHashList.append(int(str(page['nethash'])))
        workingNameList.append(str(page['name'])+": Nethash: ")
        #print(page)
        print("Progress: "+str(len(workingHashList))+"/"+str(len(cryptoDicList)))
        #backspace(len(workingHashList)+len(cryptoDicList)+10)
        time.sleep(0.1)
workingHashList, workingNameList = zip(*sorted(zip(workingHashList,workingNameList)))
workingHashList, workingNameList = (list(t) for t in zip(*sorted(zip(workingHashList, workingNameList))))

#workingHashList.sort()
count = 0
with open('data.txt','w') as outfile:
    for i in workingNameList:
        #json.dump(i,outfile)
        outfile.write(str(i)+str(workingHashList[count])+"\n")
        count +=1


'''
#difficulty_box = soup.find_all(class_='small_text')
#cryptoName = soup.find_all('div',style="margin-left: 50px")

for i in cryptoname:
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
        if str(i["Name"]).find("Nicehash") == -1 and i["Algorithm"] == algo:
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
            print()
            profitPerDay = blocksPerDay*i["RewardAmount"]*i["BTCRate"]
            print("ProfitPerDay",profitPerDay)
            #print(profitPerDay)
            if profitPerDay > profit:
                profit = profitPerDay
                winningCrypto = i["Name"]+i["Algorithm"]+" "+str(profit)
    return (winningCrypto)




'''
test = float(input("Please input hashrate"))
algo = input("Please input algorithm type")
print ("Best hash time in days for",algo,"coins:",bestHashTime(test,cryptoDicList,algo))
print(len(cryptoDicList))
'''
