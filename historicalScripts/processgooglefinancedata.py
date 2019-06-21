import requests
from datetime import datetime
tsx60ListUrl = 'https://web.tmxmoney.com/constituents_data.php?index=^TX60&index_name=S%26P%2FTSX+60+Index+%28CAD%29'
r = requests.get(tsx60ListUrl)
#with open('data/tsx60list.txt', 'wb') as f:
#    f.write(r.content)
lines = r.content.decode('ascii').split('\n')
start = False
names = []
tickers = []
print(lines)
for line in lines:
    if start and line != '':
        parts = line.split(',')
        names.append(parts[0])
        tickers.append(parts[1])
    elif line.split(',')[0] == 'Constituent Name':
        start = True

print(names)
print(tickers)
for ticker in tickers:
    f = open('data/'+ticker,'r')
    w = open ('historicalPriceData/'+ticker,'w+')
    content = f.readlines()
    content = [x.strip() for x in content]
    for line in content:
        if line != '':
            parts = line.split('\t')
            date = datetime.strptime(parts[0],'%m/%d/%Y %X')
            price = parts[1]
            w.write(date.strftime('%m/%d/%Y')+' '+price+'\n')
    f.close()
    w.close()
