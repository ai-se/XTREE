from __future__ import print_function, division

import os
import sys

# Update path
root = os.path.join(os.getcwd().split('src')[0], 'src')
if root not in sys.path:
    sys.path.append(root)

from pdb import set_trace
from oracle.model import rforest
from Data.handler import get_train_test
from XTREE.XTREE import execute
from random import seed
from Utils.FileUtil import list2dataframe
from tools.stats import scott_knott


def secondary_verification(train, test, patched):
    test = list2dataframe(test)
    before = test[test.columns[-1]].values.tolist()
    after, distr = rforest(train, patched)
    return before, after, distr


def impact(before, after):
    return (1 - sum(after) / sum(before)) * 100


def change_efficacy(n_reps=1):
    source, target = get_train_test()
    out = []
    for train, test in zip(source, target):
        res = [test.split('/')[-2].title()]
        for itr in xrange(n_reps):
            seed(itr)
            patched = execute(train, test)
            before, after, __ = secondary_verification(train, test, patched)
            if impact(before, after):
                set_trace()

            res.append(impact(before, after))
        out.append(res)

    scott_knott.sk_chart(out)


def change_succinctness():
    pass


if __name__ == "__main__":
    change_efficacy(n_reps=4)
