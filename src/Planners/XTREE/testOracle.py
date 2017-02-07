#! /Users/rkrsn/miniconda/bin/python
from __future__ import print_function, division

import os
import sys

# Update PYTHONPATH
root = os.path.abspath(os.path.join(os.getcwd().split('src')[0], 'src'))
if not root in sys.path: sys.path.append(root)

from tools.axe.abcd import _Abcd
from Prediction import *
from Planners.XTREE.lib import dEvol
from methods1 import *
import numpy as np

class data():
    """
    This data structure holds training and testing data
    """

    def __init__(self, dataName='ant', dir=root + "/Data/Jureczko"):
        projects = [Name for _, Name, __ in walk(dir)][0]
        numData = len(projects)  # Number of data
        one, two = explore(dir)
        data = [one[i] + two[i] for i in xrange(len(one))]

        def withinClass(data):
            N = len(data)
            return [(data[:n], [data[n]]) for n in range(1, N)]

        def whereis():
            for indx, name in enumerate(projects):
                if name == dataName:
                    return indx

        self.train = [dat[0] for dat in withinClass(data[whereis()])]
        self.test = [dat[1] for dat in withinClass(data[whereis()])]


class testOracle():
    def __init__(self, file='ant', tuned=True):
        self.file = file
        self.train = createTbl(data(dataName=self.file).train[-1], isBin=True)
        self.test = createTbl(data(dataName=self.file).test[-1], isBin=True)
        self.param = dEvol.tuner(rforest, data(dataName=self.file).train[-1]) if \
            tuned else None

    def main(self):
        Pd, Pf = [], []
        actual = Bugs(self.test)
        predicted = rforest(
            self.train,
            self.test,
            tunings=self.param,
            smoteit=True)
        pd, pf, _ = _Abcd(actual, predicted)
        return pd, pf


if __name__ == "__main__":
    for file in ['ant', 'camel', 'ivy',
                 'jedit', 'log4j', 'pbeans',
                 'lucene', 'poi', 'synapse',
                 'velocity', 'xalan', 'xerces']:
        PD_tuned, PF_tuned = [], []
        PD_untuned, PF_untuned = [], []

        for _ in xrange(10):
            pd, pf = testOracle(file).main()
            PD_tuned.append(pd)
            PF_tuned.append(pf)

            pd, pf = testOracle(file, tuned=False).main()
            PD_untuned.append(pd)
            PF_untuned.append(pd)

        print('### ' + file + ': Tuned')
        print("Pd, Pf\n{}, {}".format(np.mean(PD_tuned), np.mean(PF_tuned)))
        print('### ' + file + ': Untuned')
        print("Pd, Pf\n{}, {}".format(np.mean(PD_untuned), np.mean(PF_untuned)))
