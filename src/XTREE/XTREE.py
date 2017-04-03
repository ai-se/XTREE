"""
XTREE
"""
from __future__ import print_function, division

import os
import sys

# Update path
root = os.path.join(os.getcwd().split('src')[0], 'src')
if root not in sys.path:
    sys.path.append(root)

from tools.sk import *
from tools.oracle import *
import tools.pyC45 as pyC45
from random import uniform
from Utils.FileUtil import list2dataframe


def trueValue(all, test):
    set_trace()


def flatten(x):
    """
    Takes an N times nested list of list like [[a,b],[c, [d, e]],[f]]
    and returns a single list [a,b,c,d,e,f]
    """
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result


class changes():
    """
    Record changes.
    """

    def __init__(self):
        self.log = {}

    def save(self, name=None, old=None, new=None):
        if not old == new:
            delt = new / old  # if old>0 else 0
            self.log.update({name: delt})


class patches:
    def __init__(i, train, test, trainDF, testDF, tree=None, config=False):
        i.train = train
        i.trainDF = trainDF
        i.test = test
        i.testDF = testDF
        i.config = config
        i.tree = tree
        i.change = []

    def leaves(i, node):
        """
        Returns all terminal nodes.
        """
        L = []
        if len(node.kids) > 1:
            for l in node.kids:
                L.extend(i.leaves(l))
            return L
        elif len(node.kids) == 1:
            return [node.kids]
        else:
            return [node]

    def find(i, testInst, t):
        if len(t.kids) == 0:
            return t
        for kid in t.kids:
            if i.config:
                if kid.val[0] == testInst[kid.f].values[0]:
                    return i.find(testInst, kid)
            else:
                try:
                    if kid.val[0] <= testInst[kid.f].values[0] < kid.val[1]:
                        return i.find(testInst, kid)
                    elif kid.val[1] == testInst[kid.f].values[0] == i.trainDF.describe()[kid.f]['max']:
                        return i.find(testInst, kid)
                except:
                    set_trace()
        return t

    @staticmethod
    def howfar(me, other):
        common = [a for a in me.branch if a not in other.branch]
        return len(me.branch) - len(common)

    def patchIt(i, testInst, config=False):
        # 1. Find where t falls
        C = changes()  # Record changes
        testInst = pd.DataFrame(testInst).transpose()
        current = i.find(testInst, i.tree)
        node = current
        while node.lvl > -1:
            node = node.up  # Move to tree root

        leaves = flatten([i.leaves(_k) for _k in node.kids])
        try:
            if i.config:
                best = sorted([l for l in leaves if l.score < current.score], key=lambda F: i.howfar(current, F))[0]
            else:
                best = \
                    sorted([l for l in leaves if l.score <= 0.01 * current.score], key=lambda F: i.howfar(current, F))[
                        0]
        except:
            return testInst.values.tolist()[0]

        def new(old, range):
            rad = abs(min(range[1] - old, old - range[1]))
            return uniform(range[0], range[1])

        for ii in best.branch:
            before = testInst[ii[0]]
            if not ii in current.branch:
                then = testInst[ii[0]].values[0]
                now = ii[1] if i.config else new(testInst[ii[0]].values[0], ii[1])
                # print(current.branch,best.branch)
                testInst[ii[0]] = now
                C.save(name=ii[0], old=then, new=now)

        testInst[testInst.columns[-1]] = 1
        i.change.append(C.log)
        return testInst.values.tolist()[0]

    def main(i):
        newRows = []
        for n in xrange(i.testDF.shape[0]):
            if i.testDF.iloc[n][-1] > 0 or i.testDF.iloc[n][-1] == True:
                newRows.append(i.patchIt(i.testDF.iloc[n]))
            else:
                newRows.append(i.testDF.iloc[n].tolist())
        return pd.DataFrame(newRows, columns=i.testDF.columns)


def execute(train, test):
    """XTREE"""

    train_DF = list2dataframe(train)
    test_DF = list2dataframe(test)
    tree = pyC45.dtree(train_DF)
    # set_trace()
    patch = patches(train=train, test=test, trainDF=train_DF, testDF=test_DF, tree=tree)
    return patch.main()


if __name__ == '__main__':
    E = []
    for name in ['ant']:  # , 'ivy', 'jedit', 'lucene', 'poi']:
        print("##", name)
        train, test = explore(dir='../Data/Jureczko/', name=name)
        aft = [name]
        for _ in xrange(10):
            aft.append(execute(train, test))
        E.append(aft)
    rdivDemo(E)
