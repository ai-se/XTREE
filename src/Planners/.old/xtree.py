"""
XTREE
"""
from __future__ import print_function, division
import pandas as pd, numpy as np
from pdb import set_trace
import sys
sys.path.append('..')
from tools.sk import *
from tools.misc import *
from tools.oracle import *
import tools.pyC45 as pyC45
from tools.Discretize import discretize
from timeit import time
from random import uniform
from numpy.random import normal as randn
from tools.tune.dEvol import tuner

def trueValue(all,test):
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
      self.log.update({name: (old-new)/old*100})

class patches:

  def __init__(i,train,test,trainDF,testDF,rfTrain,tree=None,tunings=None,config=False):
    i.train=train
    i.trainDF = trainDF
    i.rftrain = rfTrain
    i.test=test
    i.testDF=testDF
    i.config=config
    i.tree=tree
    i.change =[]
    i.tunings = tunings#if tunings else tuner(i.rftrain)

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
    if len(t.kids)==0:
      return t
    for kid in t.kids:
      if i.config:
        if kid.val[0]==testInst[kid.f].values[0]:
          return i.find(testInst,kid)
      else:
        try:
          if kid.val[0]<=testInst[kid.f].values[0]<kid.val[1]:
            return i.find(testInst,kid)
          elif kid.val[1]==testInst[kid.f].values[0]==i.trainDF.describe()[kid.f]['max']:
            return i.find(testInst,kid)
        except: set_trace()
    return t

  @staticmethod
  def howfar(me, other):
    common = [a for a in me.branch if a not in other.branch]
    return len(me.branch)-len(common)

  def patchIt(i,testInst, config=False):
    # 1. Find where t falls
    C = changes() # Record changes
    testInst = pd.DataFrame(testInst).transpose()
    current = i.find(testInst, i.tree)
    node = current
    while node.lvl > -1:
      node = node.up  # Move to tree root

    leaves = flatten([i.leaves(_k) for _k in node.kids])
    try:
      if i.config:
        best = sorted([l for l in leaves if l.score<current.score], key=lambda F: i.howfar(current,F))[0]
      else:
        best = sorted([l for l in leaves if l.score<=0.01*current.score], key=lambda F: i.howfar(current,F))[0]
    except:
      return testInst.values.tolist()[0]

    def new(old, range):
      rad = abs(min(range[1]-old, old-range[1]))
      # return randn(old, rad) if rad else old
      # return uniform(old-rad,rad+old)
      return uniform(range[0],range[1])

    for ii in best.branch:
      before = testInst[ii[0]]
      if not ii in current.branch:
        then = testInst[ii[0]].values[0]
        now = ii[1] if i.config else new(testInst[ii[0]].values[0], ii[1])
        # print(current.branch,best.branch)
        testInst[ii[0]] = now
        C.save(name=ii[0], old=then, new=now)

    testInst[testInst.columns[-1]] = None
    i.change.append(C.log)
    return testInst.values.tolist()[0]


  def main(i, config=False, justDeltas=False):
    newRows = [i.patchIt(i.testDF.iloc[n], config) for n in xrange(i.testDF.shape[0]) if i.testDF.iloc[n][-1]>0 or i.testDF.iloc[n][-1]==True]
    newRows = pd.DataFrame(newRows, columns=i.testDF.columns)

    before, after = rforest(i.rftrain, newRows, tunings=i.tunings, bin = not i.config, regress=i.config)
    newRows[newRows.columns[-1]] = after
    gain = (1-sum(after)/sum(i.testDF[i.testDF.columns[-1]]))*100 if i.config else (1-sum(after)/len(after))*100

    if not justDeltas:
      return gain
    else:
      return i.testDF.columns[:-1], i.change

def xtree(train, test, rftrain=None, config=False,tunings=None, justDeltas=False):
  "XTREE"
  if config:
    # set_trace()
    data = csv2DF(train[1], toBin=False)
    shuffle(data)
    train_DF, test_DF=data[:int(len(data)/2)], data[int(len(data)/2):].reset_index(drop=True)
    tree = pyC45.dtree2(train_DF)
    patch = patches(train=train, test=test, trainDF=train_DF, testDF=test_DF, tree=tree, tunings=tunings, config=True)
    return patch.main(justDeltas=justDeltas)[1]
    # set_trace()


  else:
    train_DF = csv2DF(train, toBin=True)
    if not rftrain: rftrain=train
    test_DF = csv2DF(test)
    tree = pyC45.dtree(train_DF)
    # set_trace()
    patch = patches(train=train, test=test, trainDF=train_DF, testDF=test_DF, rfTrain=rftrain, tunings=tunings, tree=tree)
    return patch.main(justDeltas=justDeltas)

if __name__ == '__main__':
  E = []
  for name in ['ant']:#, 'ivy', 'jedit', 'lucene', 'poi']:
    print("##", name)
    train, test = explore(dir='../Data/Jureczko/', name=name)
    aft = [name]
    for _ in xrange(10):
      aft.append(xtree(train, test))
    E.append(aft)
  rdivDemo(E)
