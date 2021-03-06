import numpy as np
import math
import os
from sklearn import preprocessing
from sklearn import cluster

class DataWorker(object):
    def __init__(self):
        self.cwd = os.getcwd()
        self.training = np.load("%s/data/train_inputs.npy" % self.cwd)
        self.targets = np.load("%s/data/train_targets.npy" % self.cwd)
        self.tests = np.load("%s/data/test_inputs.npy" % self.cwd)

        self.n_training, self.n_inputs = np.shape(self.training)
        self.n_tests = np.shape(self.tests)[0]
        self.training_sets = None

    def find_number_classified(self, results):
        """ Outputs the ratio of 1 to 0 from classifcation """

        n_zeros = np.shape(np.where(results == 0))[1]
        n_ones = np.shape(np.where(results == 1))[1]

        return n_zeros, n_ones

    def get_normalized_production_set(self):
        """ Return a mean centered and variance normalized data training set """
        new_training = preprocessing.scale(self.training)
        new_tests = preprocessing.scale(self.tests)

        return new_training, self.targets, new_tests

    def get_production_set(self):
        """ Return full training, target and test sets """

        return self.training, self.targets, self.tests

    def get_debug_set(self, n_mini=100):
        """ Get a mini set of test and targets for debugging purposes """
        indices = np.random.choice(self.n_training, size=n_mini)
        new_training_inputs = self.training[indices,:]
        new_training_targets = self.targets[indices]

        indices = np.random.choice(self.n_tests, size=n_mini)
        new_test_inputs = self.tests[indices, :]

        return new_training_inputs, new_training_targets, new_test_inputs

    def get_debug_set_weighted(self, n_mini=100):
        """ Get a mini set of test and targets for debugging purposes """
        indices = np.random.choice(self.n_training, size=n_mini)
        new_training_inputs = self.training[indices,:]
        new_training_targets = self.targets[indices]

        indices = np.random.choice(self.n_tests, size=n_mini)
        new_test_inputs = self.tests[indices, :]

        return new_training_inputs, new_training_targets, new_test_inputs, np.ones(n_mini)

    def split_training_into_random_sets(self, n_sets):
        random_indices = np.random.choice(self.n_training, size = self.n_training, replace=False).astype(int) #all the data indices in a random order

        all_training_sets = []
        all_target_sets = []
        total_size_of_sets = 0
        spacing = math.floor(self.n_training / n_sets)
        for i in range(n_sets):
            if i == n_sets - 1:
                # this is the last set, include remainder
                these_indices = random_indices[i*spacing:]
            else:
                # not the last set, include set of size spacing
                these_indices = random_indices[i * spacing : (i+1)*spacing]

            this_training_set = self.training[these_indices,:]
            this_targets = self.targets[these_indices]

            assert np.shape(this_training_set)[0] == np.shape(this_targets)[0] # the right size
            assert np.shape(this_training_set)[1] == self.n_inputs # right number of input dimensions
            total_size_of_sets += np.shape(this_training_set)[0]
            all_training_sets.append(this_training_set)
            all_target_sets.append(this_targets)

        assert total_size_of_sets == self.n_training
        return all_training_sets, all_target_sets

    def output_results(self, results, savename="submission.csv"):
        """ Prepare submission file given results"""
        f = open(savename, "w")
        f.write("id,target\n")
        for i in range(self.n_tests):
            f.write("%d,%d\n" % (i, results[i]))
        f.close()
