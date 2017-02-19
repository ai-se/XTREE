from __future__ import print_function, division

import os
import sys

# Update path
root = os.path.join(os.getcwd().split('src')[0], 'src')
if root not in sys.path:
    sys.path.append(root)

import numpy as np
import csv
import random
from tools.sk import rdivDemo


class run():
    def __init__(self, _n=-1, smote=True, _tuneit=False, dataName=None, reps=12):

        self.dataName = dataName
        self.out = [self.dataName]
        self.out_pred = []
        self.rebalance = smote
        self.train, self.test = self.categorize()
        self.reps = reps
        self._n = _n
        self.tunedParams = None if not _tuneit \
            else tuner(self.pred, self.train[_n])
        self.headers = createTbl(
            self.train[
                self._n],
            isBin=False,
            bugThres=1).headers

    def go(self):
        base = lambda X: sorted(X)[-1] - sorted(X)[0]
        newRows = lambda newTab: map(lambda Rows: Rows.cells[:-1], newTab._rows)
        after = lambda newTab: self.pred(
            train_DF,
            newTab,
            tunings=self.tunedParams,
            smoteit=True)
        frac = lambda aft: 1 - (sum([0 if a < 1 else 1 for a in aft]) \
                                / sum([0 if b < 1 else 1 for b in actual]))

        for planner in ['xtrees']:
            out = [planner]
            for _ in xrange(self.reps):
                predRows = []
                train_DF = createTbl(self.train[self._n], isBin=True)
                test_df = createTbl(self.test[self._n], isBin=True)
                actual = np.array(Bugs(test_df))
                before = self.pred(train_DF, test_df,
                                   tunings=self.tunedParams,
                                   smoteit=True)

                predRows = [row.cells for row in createTbl(
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
