from datetime import datetime
import scrapy
import pymongo
from scrapy_splash import SplashRequest
mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
tsx60data = mongoClient['tsx60data']
stocks = tsx60data['stocks']
constituents = tsx60data['constituents']
earnings = tsx60data['earnings']
tickers = constituents.find()
presetUrls = ['https://web.tmxmoney.com/pricehistory.php?qm_symbol=', 'https://web.tmxmoney.com/earnings.php?qm_symbol=', 'https://web.tmxmoney.com/financials.php?qm_symbol=', 'https://web.tmxmoney.com/quote.php?qm_symbol=']
types = ['history', 'earningsdate', 'balance sheet', 'quote']

balancesheet = """
function main(splash)
    assert(splash:autoload("https://code.jquery.com/jquery-2.1.3.min.js"))
    local url = splash.args.url
    splash:go(url)
    splash:wait(25)
    splash:set_viewport_full()
    splash:runjs("$('a[rv-on-click=\\"binders.periods.setSelected\\"]')[1].click()")
    splash:wait(30)
    splash:runjs("$('a[rv-on-click=\\"binders.types.setSelected\\"]')[1].click()")
    splash:wait(30)
        return {
        html = splash:html()
    }
end
"""
class StockSpider(scrapy.Spider):
    name = 'PriceSpider'
    custom_settings = {
        'SPLASH_URL': 'http://localhost:8050',
        'DOWNLOADER_MIDDLEWARES' : {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        }
    }

    def reCrawl(ticker, preset):
        if (types[preset] == 'balance sheet'):
            request = SplashRequest(presetUrls[preset]+ticker, self.parse,
                endpoint='execute',
                args={'lua_source': balancesheet, 'wait': 2, 'timeout': 90},
            )
        else:
            request = SplashRequest(presetUrls[preset]+ticker, self.parse,
                endpoint='render.html',
                args={'wait': 2, 'timeout': 90},
            )
        request.meta['ticker'] = ticker
        request.meta['type'] = preset
        yield request;

    def start_requests(self):
        for ticker in tickers:
            ticker = ticker['ticker']
            for preset in range(0,len(presetUrls)):
                if (types[preset] == 'balance sheet'):
                    request = SplashRequest(presetUrls[preset]+ticker, self.parse,
                        endpoint='execute',
                        args={'lua_source': balancesheet, 'wait': 2, 'timeout': 90},
                    )
                else:
                    request = SplashRequest(presetUrls[preset]+ticker, self.parse,
                        endpoint='render.html',
                        args={'wait': 2, 'timeout': 90},
                    )
                request.meta['ticker'] = ticker
                request.meta['type'] = preset
                yield request;

    def parse(self, response):
        type = types[response.meta['type']]
        if type == 'history':
            dataKeys = ['date', 'open', 'high', 'low', 'close', 'volume']
            for row in response.css('.qm_historyData_row'):
                stockdata = {}
                index = 0
                for data in row.css('td'):
                    if (index < len(dataKeys)):
                        stockdata[dataKeys[index]] = data.css('td::text').get()
                        index += 1
                stockdata['date'] = datetime.strptime(stockdata['date'], '%m/%d/%Y').strftime('%d/%m/%Y')
                stockdata['ticker'] = response.meta['ticker']
                stocks.update({'ticker':stockdata['ticker'], 'date':stockdata['date']},stockdata, upsert=True)
        elif type == 'balance sheet':
            price = response.css('.quote-price.priceLarge > span::text').get().replace(',','')
            rows = response.css('.BalanceSheet > tr')
            data = {}
            for row in rows:
                key = row.css('td.qmod-table-title > span::text').get()
                valuesText = row.css('td.qmod-textr::text')
                values = []
                for val in values:
                    values.append(val.get())
                data[key] = values
            cAssets = []
            assets = []
            cLiabilities = []
            liabilities = []
            equity = []
            debtEquity = 0
            currentRatio = 0
            if not data:
                self.reCrawl(response.meta['ticker'],response.meta['preset'])
            for index in range(0,len(data['Total Assets'])):
                try:
                    cAssets.append(float(data['Current Assets'][index].replace(',','')))
                except:
                    cAssets.append(0)
                try:
                    assets.append(float(data['Total Assets'][index].replace(',','')))
                except:
                    assets.append(0)
                try:
                    cLiabilities.append(float(data['Current Liabilities'][index].replace(',','')))
                except:
                    cLiabilities.append(0)
                try:
                    liabilities.append(float(data['Total Liabilities'][index].replace(',','')))
                except:
                    liabilities.append(0)
                try:
                    equity.append(float(data['Stockholders Equity'][index].replace(',','')))
                except:
                    equity.append(0)
                if equity and (cAssets or cLiabilities):
                    debtEquity = liabilities / equity
                    currentRatio = cAssets / cLiabilities if cLiabilities else 0
                    break
            last_day = stocks.find({ "ticker" : response.meta['ticker'] }).sort("date", -1).limit(1)[0]
            if last_day['close'] == price:
                today = last_day['date']
            else:
                today = datetime.now().strftime('%d/%m/%Y')
            stocks.update({'ticker':response.meta['ticker'], 'date':today}, {'ticker':response.meta['ticker'], 'date':today,'debtEquity':debtEquity, 'currentRatio':currentRatio}, upsert=True)
        elif type == 'quote':
            price = response.css('.quote-price.priceLarge > span::text').get()
            rows = response.css('tr > td > table > tbody > tr')
            data = {}
            for row in rows:
                tabledatas = row.css('td')
                key = tabledatas[0].css('td::text').get()
                value = tabledatas[1].css('td::text').get()
                data[key] = value
            price = float(price.replace(',',''))
            prevClose = float(data['Prev. Close:'].replace(',',''))
            difference = price / prevClose
            try:
                pe = float(data['P/E Ratio:'].replace(',','').strip()) * difference
            except:
                pe = 0
            try:
                pb = float(data['P/B Ratio:'].replace(',','').strip()) * difference
            except:
                pb = 0
            try:
                yd = float(data['Yield:'].replace(',','').strip()) / difference
            except:
                yd = 0
            try:
                marketCap = float(data['Market Cap (Dil. Avg Shrs):'].replace(',','').strip()) * difference
            except:
                marketCap = 0
            last_day = stocks.find({ "ticker" : response.meta['ticker'] }).sort("date", -1).limit(1)[0]
            if last_day['close'] == price:
                today = last_day['date']
            else:
                today = datetime.now().strftime('%d/%m/%Y')
            stocks.update({'ticker':response.meta['ticker'], 'date':today}, {'ticker':response.meta['ticker'], 'date':today,'close':price, 'pe':pe, 'pb':pb,'yd':yd, 'marketCap':marketCap}, upsert=True)
        elif type == 'earningsdate':
            rows = response.css('div.earningstable > table > tbody > tr')
            rows.pop(0)
            for row in rows:
                data = row.css('td')
                try:
                    date = data[1].css('td::text').get()
                    date = datetime.strptime(date, '%m/%d/%y')
                    eps = data[2].css('td::text').get()
                    earnings.update({'ticker':response.meta['ticker'], 'month':date.strftime('%m'), 'year':date.strftime('%Y')}, {'ticker':response.meta['ticker'], 'month':date.strftime('%m'), 'year':date.strftime('%Y'),'eps':eps,'date':date.strftime('%d/%m/%Y')}, upsert=True)
                except:
                    pass
