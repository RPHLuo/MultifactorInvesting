import pymongo
class CIFAR10Sequence(Sequence):

        def __init__(self, x_set, y_set, batch_size):
            pymongo
            self.x, self.y = x_set, y_set

            self.batch_size = batch_size

        def __len__(self):
            return math.ceil(len(self.x) / self.batch_size)

        def __getitem__(self, idx):
            batch_x = self.x[idx * self.batch_size:(idx + 1) *
            self.batch_size]
            batch_y = self.y[idx * self.batch_size:(idx + 1) *
            self.batch_size]

            return np.array([i
                resize(imread(file_name), (200, 200))
                   for file_name in batch_x]), np.array(batch_y)
