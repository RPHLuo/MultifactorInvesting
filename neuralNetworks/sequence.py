import pymongo
class MongoSequence(Sequence):
    def __init__(self, batch_size, train_set, query=None, server=None, database="tsx60data", collection="stocks"):
        self._server = server
        self._db = database
        self._collection_name = collection
        self._batch_size = batch_size
        self._query = query
        self._collection = self._connect()

        self._object_ids = [ smp["_id"] for uid in train_set for smp in self._collection.find(self._query, {'_id': True})]

        self._pid = os.getpid()
        del self._collection   #  to be sure, that we've disconnected
        self._collection = None

    def _connect(self):
        client = pymongo.MongoClient(self._server)
        db = client[self._db]
        return db[self._collection_name]

    def __len__(self):
        return int(np.ceil(len(self._object_ids) / float(self._batch_size)))

    def __getitem__(self, item):
        if self._collection is None or self._pid != os.getpid():
            self._collection = self._connect()
            self._pid = os.getpid()

        oids = self._object_ids[item * self._batch_size: (item+1) * self._batch_size]
        X = np.empty((len(oids), IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS), dtype=np.float32)
        y = np.empty((len(oids), 2), dtype=np.float32)
        for i, oid in enumerate(oids):
            smp = self._connect().find({'_id': oid}).next()
            X[i, :, :, :] = pickle.loads(smp['frame']).astype(np.float32)
            y[i] = to_categorical(not smp['result'], 2)
        return X, y
