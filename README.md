Chi_Square
==========

Chi Square Feature Selection

These scripts conduct feature selection using chi square values as the evaluation metric.
The input is a p value (used to grade significance), the training data in vector form and
The test data in vector form.

The main script uses a series of nested dictionaries to calculate chi square values for each feature in
a training data set. These nested dictionaries represent the observed and expected distribution of features.
In this case, teh data is degree of freedom = 2, there are three class labels and features are either present or absent. Chi square essentially calculates the difference between the observed and expected distributions of features.
The code for this is on line

After performing the calculations over training data, the script outputs a versions of the training and test data
that only contain features significant as determined by the p value.

Usage: The command line arguments are as follows: 1 = p value, a number from {0.1, 0.05, 0.025, 0.01, 0.001}
2 = training data 3 = test data
