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
presetUrls = ['https://web.tmxmoney.com/financials.php?qm_symbol=', 'https://web.tmxmoney.com/pricehistory.php?qm_symbol=', 'https://web.tmxmoney.com/quote.php?qm_symbol=', 'https://web.tmxmoney.com/earnings.php?qm_symbol=']
types = ['balance sheet','history','quote', 'earningsdate']
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

    def start_requests(self):
        balancesheet = """
        function main(splash)
            assert(splash:autoload("https://code.jquery.com/jquery-2.1.3.min.js"))
            local url = splash.args.url
            splash:go(url)
            splash:wait(10)
            splash:set_viewport_full()
            splash:runjs("$('a[rv-on-click=\\"binders.periods.setSelected\\"]')[1].click()")
            splash:wait(5)
            splash:runjs("$('a[rv-on-click=\\"binders.types.setSelected\\"]')[1].click()")
            splash:wait(5)
            return {
                html = splash:html()
            }
        end
        """
        for preset in range(0,len(presetUrls)):
            for ticker in tickers:
                ticker = ticker['ticker']
                if (types[preset] == 'balance sheet'):
                    request = SplashRequest(presetUrls[preset]+ticker, self.parse,
                        endpoint='execute',
                        args={'lua_source': balancesheet, 'wait': 2},
                    )
                else:
                    request = SplashRequest(presetUrls[preset]+ticker, self.parse,
                        endpoint='render.html',
                        args={'wait': 2},
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
            rows = response.css('.BalanceSheet > tr')
            self.log(rows)
            data = {}
            for row in rows:
                self.log(row)
                key = row.css('td.qmod-table-title > span::text').get()
                value = row.css('td.qmod-textr::text')[0].get()
                data[key] = value
            assets = data['Total Assets']
            cAssets = data['Current Assets']
            liabilities = data['Total Liabilities']
            cLiabilities = data['Current Liabilities']
            equity = data['Stockholders Equity']
            try:
                cAssets = float(cAssets)
            except:
                cAssets = 0
            try:
                assets = float(assets)
            except:
                assets = 0
            try:
                cLiabilities = float(cLiabilities)
            except:
                cLiabilities = 0
            try:
                liabilities = float(liabilities)
            except:
                liabilities = 0
            try:
                equity = float(equity)
            except:
                equity = 0
            debtEquity = liabilities / equity if equity else 0
            currentRatio = cAssets / cLiabilities if cLiabilities else 0
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
            price = float(price)
            prevClose = float(data['Prev. Close:'])
            difference = price / prevClose
            try:
                pe = float(data['P/E Ratio:'].strip()) * difference
            except:
                pe = 0
            try:
                pb = float(data['P/B Ratio:'].strip()) * difference
            except:
                pb = 0
            try:
                yd = float(data['Yield:'].strip()) / difference
            except:
                yd = 0
            try:
                marketCap = float(data['Market Cap (Dil. Avg Shrs):'].replace(',','').strip()) * difference
            except:
                marketCap = 0
            today = datetime.now().strftime('%d/%m/%Y')
            stocks.update({'ticker':response.meta['ticker'], 'date':today}, {'ticker':response.meta['ticker'], 'date':today,'price':price, 'pe':pe, 'pb':pb,'yd':yd, 'marketCap':marketCap}, upsert=True)
        elif type == 'earningsdate':
            rows = response.css('div.earningstable > table > tbody > tr')
            rows.pop(0)
            for row in rows:
                data = row.css('td')
                date = data[1].css('td::text').get()
                date = datetime.strptime(date, '%m/%d/%Y')
                eps = data[2].css('td::text').get()
                earnings.update({'ticker':response.meta['ticker'], 'month':date.strftime('%m'), 'year':date.strftime('%Y')}, {'ticker':response.meta['ticker'], 'month':date.strftime('%m'), 'year':date.strftime('%Y'),'eps':eps,'date':date.strftime('%d/%m/%Y')}, upsert=True)
