
'''
Chi square feature ranker
Jared Kramer

This script conducts feature selection using chi square values as the evaluation metric.
The input is a p value (used to grade significance), the training data in vector form and
The test data in vector form.

The script uses a series of nested dictionaries to calculate chi square values for each feature in
a training data set. These nested dictionaries represent the observed and expected distribution of features.
In this case, teh data is degree of freedom = 2, there are three class labels and features are either present or absent.
Chi square essentially calculates the difference between the observed and expected distributions of features.
The code for this is on line

After performing the calculations over training data, the script outputs a versions of the training and test data
that only contain features significant as determined by the p value.

'''


import sys
from collections import defaultdict
import time

def rank_features():

    # Load data and initialize data structures
    # train = open("examples/train.vectors.txt", 'r').read().strip().split("\n")
    train = open(train_in, 'r').read().strip().split("\n")
    global feat_list
    feat_list = []

    # these dictionaries represent the distributions
    observed = defaultdict(lambda: defaultdict(lambda: defaultdict(int))) #the tuple [0] is the count feature present, [1] is feature absent
    expected = defaultdict(lambda: defaultdict(lambda: defaultdict(int))) #the tuple [0] is the count feature present, [1] is feature absent
    chi_squares = defaultdict(float)

    f_present_total, f_absent_total = "f_present_total", "f_absent_total"
    present, absent, col_total= "present", "absent", "col_total"

    every_word = set()
    doc_count = defaultdict(int)

    #get doc counts and set of all features
    for vector in train:
        vector = vector.split()
        doc_count[vector[0]] += 1
        for chunk in vector[1:]:
            every_word.add(chunk.split(":")[0]) # features are formatted feat_name:feat_value
    print "Total number of features:", len(every_word) # number of features

    # populate the observed distribution
    for vector in train:
        vector = vector.split()
        label = vector[0]
        doc_words = {chunk.split(":")[0] for chunk in vector[1:]}
        for w in every_word:
            if w in doc_words:
                observed[w][label][present] += 1 # add one to feature present in doc of that label
            else:
                observed[w][label][absent] += 1 # add one to feature present in doc of that label

    # still populating observed distribution
    num_of_docs = float(sum(doc_count.values()))
    for w in observed:
        count = 0
        for label in doc_count:
            count += observed[w][label][present]
        observed[w]["all_classes"][f_present_total] = count
        observed[w]["all_classes"][f_absent_total] = num_of_docs - count
        for label in doc_count:
            observed[w][label][col_total] = observed[w][label][absent] + observed[w][label][present]

    # populate expected distributiom
    for w in observed:
        for label in doc_count:
            expected[w][label][present] = (observed[w]["all_classes"][f_present_total] * observed[w][label][col_total]) / num_of_docs
            expected[w][label][absent] = (observed[w]["all_classes"][f_absent_total] * observed[w][label][col_total]) / num_of_docs

    # calculate chi square values
    for w in observed:
        running_sum = 0
        for label in doc_count:
            for state in {present, absent}:
                running_sum += ((observed[w][label][state] - expected[w][label][state])**2) / expected[w][label][state]
        chi_squares[w] = running_sum

    # sort by chi square
    sorted_chi = sorted(chi_squares, key=chi_squares.get, reverse=True)
    for w in sorted_chi:
        feat_list.append((w, chi_squares[w]))

def select_features(vector, train=True):
    vector = vector.split()
    if train: train_out.write(vector[0] + " ")
    else: test_out.write(vector[0] + " ")
    for chunk in vector:
        parts = chunk.split(":")
        if parts[0] in selected:
            if train: train_out.write(chunk+" ")
            else: test_out.write(chunk+" " )

#### #### #### #### #### #### #### MAIN
start_time = time.time()

#chi square distribution table for degree of freedom = 2
distribution = {
0.1:4.605,
0.05:5.991,
0.025:7.378,
0.01:9.210,
0.001:13.816
}

if len(sys.argv) > 1:
    # Command line arguments
    p, train_in, test_in, = sys.argv[1:]
    p = float(p)
else:
    # Debugging Arguments
    p = 0.05
    train_in = "train.vectors.txt"
    test_in = "test.vectors.txt"
#this creates a feature list sorted by chi square values
rank_features()

train_out = open(str(p) + "_" + train_in, 'w')
test_out = open(str(p) + "_" + test_in, 'w')
train_in = open(train_in, 'r').read().strip().split("\n")
test_in = open(test_in, 'r').read().strip().split("\n")

selected = set()
thresh = distribution[p]
for feature_tuple in feat_list:
    if feature_tuple[1] >= thresh:
        selected.add(feature_tuple[0])

print "Total number of post feature-selection features", len(selected)

for vector in train_in:
    select_features(vector)
    train_out.write("\n")
for vector in test_in:
    select_features(vector, train=False)
    test_out.write("\n")

print time.time() - start_time, "seconds"
