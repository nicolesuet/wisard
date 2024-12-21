from wisard import Wisard
import util
import sys
from encoding import thermometer
from encoding import util
import numpy as np
from wisard import Wisard
from timeit import default_timer as timer

base_path = "datasets/iris/"

bits_encoding = 20
train_data, train_label, test_data, test_label, data_min, data_max = util.load_3data(base_path)

ths = []

for t in range(len(data_max)):
    ths.append(thermometer.Thermometer(data_min[t], data_max[t], bits_encoding))

print(ths)

train_bin = []
test_bin = []

i = 0
for data in train_data:
    train_bin.append(np.array([], dtype=bool))
    t = 0
    for v in data:
        binarr = ths[t].binarize(v)
        train_bin[i] = np.append(train_bin[i], binarr)  
        t += 1

    i += 1

i = 0
for data in test_data:
    test_bin.append(np.array([], dtype=bool))
    t = 0
    for v in data:
        binarr = ths[t].binarize(v)
        test_bin[i] = np.append(test_bin[i], binarr)  
        t += 1
    i += 1
    
#Parameters
num_classes = 3
tuple_bit = 20
test_length = len(test_label)
num_runs = 20

acc_list = []
training_time = []
testing_time = []

dacc_list = []
dtraining_time = []
dtesting_time = []

bacc_list = []
btraining_time = []
btesting_time = []
entry_size = len(train_bin[0])

#Wisard
for r in range(num_runs):
    wisard = Wisard(entry_size, tuple_bit, num_classes)

    #Training
    start = timer()
    wisard.train(train_bin, train_label)
    training_time.append(timer() - start)

    #Testing
    start = timer()
    rank_result = wisard.rank(test_bin)    
    testing_time.append(timer() - start)

    #Accuracy
    num_hits = 0

    for i in range(test_length):
        if rank_result[i] == test_label[i]:
            num_hits += 1

    acc_list.append(float(num_hits)/float(test_length))

wisard_stats = wisard.stats()
