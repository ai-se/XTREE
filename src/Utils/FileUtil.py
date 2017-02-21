from __future__ import print_function, division

import os
import sys

# Update PYTHONPATH
root = os.path.join(os.getcwd().split('src')[0], 'src')
if root not in sys.path:
    sys.path.append(root)

from pdb import set_trace
from pandas import read_csv, concat
from pandas.io.common import EmptyDataError
from tools.axe.dtree import *
from AxeUtils.w2 import where2, prepare, leaves
from AxeUtils.MakeAModel import MakeAModel


def new_table(tbl, headerLabel, Rows):
    tbl2 = clone(tbl)
    newHead = Sym()
    newHead.col = len(tbl.headers)
    newHead.name = headerLabel
    tbl2.headers = tbl.headers + [newHead]
    return clone(tbl2, rows=Rows)


def list2dataframe(lst):
    try:
        data = [read_csv(elem) for elem in lst]
    except EmptyDataError:
        return read_csv(lst)
    return concat(data, ignore_index=True)


def create_tbl(
        data,
        settings=None,
        _smote=False,
        isBin=False,
        bugThres=1,
        duplicate=False):
    """
    kwargs:
    _smote = True/False : SMOTE input data (or not)
    _isBin = True/False : Reduce bugs to defects/no defects
    _bugThres = int : Threshold for marking stuff as defective,
                      default = 1. Not defective => Bugs < 1
    """
    model = MakeAModel()
    _r = []
    for t in data:
        m = model.csv2py(t, _smote=_smote, duplicate=duplicate)
        _r += m._rows
    m._rows = _r
    # Initialize all parameters for where2 to run
    prepare(m, settings=None)
    tree = where2(m, m._rows)  # Decision tree using where2
    tbl = table(t)

    headerLabel = '=klass'
    Rows = []
    for k, _ in leaves(tree):  # for k, _ in leaves(tree):
        for j in k.val:
            tmp = j.cells
            if isBin:
                tmp[-1] = 0 if tmp[-1] < bugThres else 1
            tmp.append('_' + str(id(k) % 1000))
            j.__dict__.update({'cells': tmp})
            Rows.append(j.cells)

    return new_table(tbl, headerLabel, Rows)


def test_createTbl():
    dir = '../Data/camel/camel-1.6.csv'
    newTbl = create_tbl([dir], _smote=False)
    newTblSMOTE = create_tbl([dir], _smote=True)
    print(len(newTbl._rows), len(newTblSMOTE._rows))


def drop(test, tree):
    loc = apex(test, tree)
    return loc


if __name__ == '__main__':
    test_createTbl()
    set_trace()
