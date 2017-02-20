from __future__ import print_function, division

import os
import sys

# Update path
root = os.path.join(os.getcwd().split('src')[0], 'src')
if root not in sys.path:
    sys.path.append(root)

from pdb import set_trace
from Utils.FileUtil import create_tbl
from oracle.model import rforest
from Data.handler import get_train_test


class main():
    def __init__(self, _n=-1, smote=False, _tuneit=False, dataName=None, reps=12):
        self.dataName = dataName
        self.out = [self.dataName]
        self.out_pred = []
        self.rebalance = smote
        self.train, self.test = get_train_test
        self.reps = reps
        self._n = _n

    def secondary_verification(self, train, test):
        actual = test[test.columns[-1]].values.tolist()
        predicted, distr = rforest(train, test, tunings=True, smote=self.rebalance)
        return actual, predicted, distr

    def go(self):
        def newRows(newTab):
            return map(lambda Rows: Rows.cells[:-1], newTab._rows)

        out = ["XTREE"]
        for _ in xrange(self.reps):
            train_df = create_tbl(self.train, isBin=True)
            test_df = create_tbl(self.test, isBin=True)
            newTab = xtree(train=train_df,
                           test_DF=test_df,
                           bin=False,
                           majority=True).main()
        set_trace()
        yield out
