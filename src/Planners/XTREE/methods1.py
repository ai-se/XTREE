#! /Users/rkrsn/anaconda/bin/python
from pdb import set_trace
from os import environ, getcwd
from os import walk
from os.path import expanduser
from pdb import set_trace
import sys

# Update PYTHONPATH
HOME = expanduser('~')
axe = HOME + '/git/axe/axe/'  # AXE
pystat = HOME + '/git/pystats/'  # PySTAT
cwd = getcwd()  # Current Directory
sys.path.extend([axe, pystat, './where2'])
from tools.axe.dtree import *
from tools.axe.table import *
# from w2 import *
from lib.w2 import where2, prepare, leaves
from lib.makeAmodel import makeAModel
import matplotlib.mlab as mlab
# import matplotlib.pyplot as plt
import smote


def explore(dir):
  datasets = []
  for (dirpath, dirnames, filenames) in walk(dir):
    datasets.append(dirpath)

  training = []
  testing = []
  for k in datasets[1:]:
    train = [[dirPath, fname] for dirPath, _, fname in walk(k)]
    test = [train[0][0] + '/' + train[0][1].pop(-1)]
    training.append(
        [train[0][0] + '/' + p for p in train[0][1] if not p == '.DS_Store'])
    testing.append(test)
  return training, testing


def newTable(tbl, headerLabel, Rows):
  tbl2 = clone(tbl)
  newHead = Sym()
  newHead.col = len(tbl.headers)
  newHead.name = headerLabel
  tbl2.headers = tbl.headers + [newHead]
  return clone(tbl2, rows=Rows)


def createTbl(
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
  makeaModel = makeAModel()
  _r = []
  for t in data:
    m = makeaModel.csv2py(t, _smote=_smote, duplicate=duplicate)
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

  return newTable(tbl, headerLabel, Rows)


def test_createTbl():
  dir = '../Data/camel/camel-1.6.csv'
  newTbl = createTbl([dir], _smote=False)
  newTblSMOTE = createTbl([dir], _smote=True)
  print(len(newTbl._rows), len(newTblSMOTE._rows))


def drop(test, tree):
  loc = apex(test, tree)
  return loc


if __name__ == '__main__':
  test_createTbl()
