from sequence import MongoSequence
import sequence
#ms = MongoSequence(20, query={'ticker':'AEM'})
#x = ms.__getitem__(index=0)
x = sequence.getAll('AEM')
print(x)
print(x.shape)
