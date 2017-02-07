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
from collections import Counter

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
      d = new/old if new>old else -new/old #*100
      d = d if np.isfinite(d) else 0# (new-old)/new*100
      self.log.update({name: d})

class patches:

  def __init__(i,train,test,trainDF,testDF,rfTrain,tree=None,tunings=None,config=False):
    i.train    = train
    i.trainDF  = trainDF
    i.rftrain  = rfTrain
    i.test     = test
    i.testDF   = testDF
    i.config   = config
    i.tree     = tree
    i.change   = []
    i.tunings  = tunings#if tunings else tuner(i.rftrain)

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


  def patchIt(i,testInst, config=False):
    testInst = pd.DataFrame(testInst).transpose()
    node = i.find(testInst, i.tree)
    return 1 if (np.median(node.t["$<bug"]) > 0 and testInst["$<bug"].values[0] > 0) or (np.median(node.t["$<bug"]) == testInst["$<bug"].values[0]) else 0
    
  def disc(i):
    def ent(x):
      C = Counter(x)
      N = len(x)
      return sum([-C[n]/N*np.log(C[n]/N) for n in C.keys()])

    leaves = flatten([i.leaves(_k) for _k in i.tree.kids])
    values = [l.t["$<bug"].values.tolist() for l in leaves]
    entrop = np.array([ent(val) for val in values])
    max_l = np.max([len(l) for l in values])
    wt = np.array([(len(l)-1)/(max_l-1) for l in values] )
    return np.mean(wt*entrop)
    
  def stability(i, config=False, justDeltas=False):
    newRows = [i.patchIt(i.testDF.iloc[n], config) for n in xrange(i.testDF.shape[0])]
    return sum(newRows)/len(newRows)




def xtree(train, test, rftrain=None, config=False,tunings=None, justDeltas=False):
  
  "XTREE"
  train_DF = csv2DF(train, toBin=True)
  if not rftrain: rftrain=train
  test_DF = csv2DF(test)
  train_val = csv2DF(train[:-1], toBin=True)
  test_val  = csv2DF([train[-1]], toBin=True)
  tree = pyC45.dtree(train_DF)
  tree_val = pyC45.dtree(train_val)
  patch0 = patches(train=train, test=test, trainDF=train_DF, testDF=test_DF, rfTrain=rftrain, tunings=tunings, tree=tree)
  patch1 = patches(train=train, test=test, trainDF=train_val, testDF=test_val, rfTrain=rftrain, tunings=tunings, tree=tree_val)
  stab = np.min(patch0.stability(justDeltas=justDeltas), patch1.stability(justDeltas=justDeltas))
  disc = patch0.disc()

  return stab, disc