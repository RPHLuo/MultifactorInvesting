import pymongo
def fillList():
    mongoClient = pymongo.MongoClient("mongodb://mongo:27017/")
    tsx60data = mongoClient['tsx60data']
    constituents = tsx60data['constituents']
    list = open('./scraper/tsxlist','r')
    for line in list:
        line = line.strip()
        if line != '':
            constituents.update({'ticker':line},{'ticker':line},upsert= True)
