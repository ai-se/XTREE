from __future__ import print_function, division

import os
import sys

# Update path
root = os.path.join(os.getcwd().split('src')[0], 'src')
if root not in sys.path:
    sys.path.append(root)

import numpy as np
from Utils.FileUtil import create_tbl
from oracle.model import rforest

class main():
    def __init__(self, _n=-1, smote=True, _tuneit=False, dataName=None, reps=12):

        self.dataName = dataName
        self.out = [self.dataName]
        self.out_pred = []
        self.rebalance = smote
        self.train, self.test = self.categorize()
        self.reps = reps
        self._n = _n

    def secondary_verification(self, train, test):
        actual = test[test.columns[-1]].values.tolist()
        predicted, distr = rforest(train, test, tunings=self.tunedParams, smoteit=True)
        return actual, predicted, distr

    def go(self):

        def newRows(newTab):
            return map(lambda Rows: Rows.cells[:-1], newTab._rows)

        frac = lambda aft: 1 - (sum([0 if a < 1 else 1 for a in aft]) \
                                / sum([0 if b < 1 else 1 for b in actual]))

        for planner in ['xtrees']:
            out = [planner]
            for _ in xrange(self.reps):
                predRows = []
                train_DF = create_tbl(self.train[self._n], isBin=True)
                test_df = create_tbl(self.test[self._n], isBin=True)
                actual = np.array(Bugs(test_df))
                before = self.pred(train_DF, test_df,
                                   tunings=self.tunedParams,
                                   smoteit=True)

                predRows = [row.cells for row in create_tbl(
                    self.test[self._n], isBin=True)._rows if row.cells[-2] > 0]

                predTest = genTable(test_df, rows=predRows, name='Before_temp')

                "Apply Different Planners"
                if planner == 'xtrees':
                    newTab = xtrees(train=self.train[-1],
                                    test_DF=predTest,
                                    bin=False,
                                    majority=True).main()
                    genTable(test_df, rows=newRows(newTab), name='After_xtrees')
                # set_trace()
                elif planner == 'XTREE':
                    newTab = xtrees(train=self.train[-1],
                                    test_DF=predTest,
                                    bin=False,
                                    majority=False).main()

                elif planner == 'BIC':
                    newTab = HOW(train=self.train[-1],
                                 test=self.test[-1],
                                 test_df=predTest).main()

                elif planner == 'CD':
                    newTab = strawman(train=self.train[-1], test=self.test[-1]).main()

                elif planner == 'CD+FS':
                    newTab = strawman(train=self.train[-1], test=self.test[-1]
                                      , prune=True).main()

                out.append(frac(after(newTab)))
            # self.logResults(out)
            yield out
