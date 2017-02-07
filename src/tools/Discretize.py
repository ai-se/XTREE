"""
An instance filter that discretizes a range of numeric attributes in the dataset into nominal attributes. Discretization is by Fayyad & Irani's MDL method (the default).

For more information, see:

Usama M. Fayyad, Keki B. Irani: Multi-interval discretization of continuous valued attributes for classification learning. In: Thirteenth International Joint Conference on Artificial Intelligence, 1022-1027, 1993.

Igor Kononenko: On Biases in Estimating Multi-Valued Attributes. In: 14th International Joint Conference on Articial Intelligence, 1034-1040, 1995.

Dougherty, James, Ron Kohavi, and Mehran Sahami. "Supervised and unsupervised discretization of continuous features." Machine learning: proceedings of the twelfth international conference. Vol. 12. 1995.
"""
from __future__ import division, print_function
import pandas as pd
from collections import Counter
from misc import *
import numpy as np
from pdb import set_trace
from sklearn.tree import DecisionTreeClassifier as CART



def fWeight(tbl):
    """
    Sort features based on entropy
    """
    clf = CART(criterion='entropy')
    features = tbl.columns[:-1]
    klass = tbl[tbl.columns[-1]]
    clf.fit(tbl[features], klass)
    lbs = clf.feature_importances_
    return [tbl.columns[i] for i in np.argsort(lbs)[::-1]]

def discretize(feature, klass, atleast=-1, discrete=False):

  """
  Recursive Minimal Entropy Discretization
  ````````````````````````````````````````
  Inputs:
    feature: A list or a numpy array of continuous attributes
    klass: A list, or a numpy array of discrete class labels.
    atleast: minimum splits.
  Outputs:
    splits: A list containing suggested spilt locations
  """
  def measure(x):
    def ent(x):
      C = Counter(x)
      N = len(x)
      return sum([-C[n]/N*np.log(C[n]/N) for n in C.keys()])
    def stdev(x):
      if np.isnan(np.var(x)**0.5):
        return 0
      return np.var(x)**0.5
    if not discrete: return ent(x)
    else: return stdev(x)

  # Sort features and klass
  feature, klass = sorted(feature), [k for (f,k) in sorted(zip(feature,klass))]
  splits = []
  gain = []
  lvl = 0
  def redo(feature, klass, lvl):
      if len(feature)>0:
        E = measure(klass)
        N = len(klass)
        T=[] # Record boundaries of splits
        for k in xrange(len(feature)):
          west, east = feature[:k], feature[k:]
          k_w, k_e = klass[:k], klass[k:]
          N_w, N_e = len(west), len(east)
          T+=[N_w/N*measure(k_w)+N_e/N*measure(k_e)]

        T_min = np.argmin(T)
        left, right = feature[:T_min], feature[T_min:]
        k_l, k_r = klass[:T_min], klass[T_min:]
        # set_trace()
        def stop(k,k_l,k_r):
          gain =  E-T[T_min]
          def count(lst): return len(Counter(lst).keys())
          delta = np.log2(float(3**count(k)-2)) - (
              count(k)*measure(k)-count(k_l)*measure(k_l)-count(k_r)*measure(k_r))
          # print(gain, (np.log2(N-1)+delta)/N)
          return gain<(np.log2(N-1)+delta)/N or T_min==0

        if stop(klass,k_l,k_r) and lvl>=atleast:
          if discrete:
            splits.append(T_min)
          else:
            splits.append(feature[T_min])

        else:
          _ = redo(feature=left, klass=k_l, lvl=lvl+1)
          _ = redo(feature=right, klass=k_r, lvl=lvl+1)

  # ------ main ------
  redo(feature,klass, lvl=0)
  # set_trace()
  return splits

def _test0():
  "A Test Function"
  test  = np.random.normal(0,10,1000).tolist()
  klass = [int(abs(i)) for i in np.random.normal(0,1,1000)]
  splits = discretize(feature=test, klass=klass)
  set_trace()

def _test1():
  tbl_loc = explore(name='ant')[0]
  tbl = csv2DF(tbl_loc)
  new = discreteTbl(tbl)
  set_trace()

def discreteTbl(tbl,B=0.33, Prune=True):
  """
  Discretize a table
  ``````````````````
  Columns 1 to N-1 represent the independent attributes, column N the dependent.

  Parameters:

  tbl   - A Pandas Data Frame
  B     - Cutoff for Pruning Columns (float between 0,1)
  Prune - Prune (True/False)

  Returns:
  Pandas Data Frame: Discretized table
  """
  dtable=[]
  fweight = fWeight(tbl)
  for i,name in enumerate(tbl.columns[:-1]):
    new=[]
    feature=tbl[name].values
    klass = tbl[tbl.columns[-1]].values
    splits = discretize(feature, klass)
    LO, HI = min(feature), max(feature)
    cutoffs = sorted(list(set(splits+[LO,HI])))
    def pairs(lst):
      while len(lst)>1:
        yield (lst.pop(0), lst[0])
    cutoffs = [t for t in pairs(sorted(list(set(splits+[LO,HI]))))]
    for f in feature:
      for n in cutoffs:
        if n[0]<=f<n[1]:
          new.append(n)
        elif f==n[1]==HI:
          new.append((n[0],HI))
    dtable.append(new)
  dtable.append(klass.tolist())
  dtable = pd.DataFrame(dtable).T
  dtable.columns = tbl.columns
  ranks = fWeight(tbl)
  if Prune:
    return dtable[ranks[:int(len(ranks)*B)]+[tbl.columns[-1]]]
  else:
    return dtable[ranks+[tbl.columns[-1]]]

if __name__=='__main__':
  _test0()
  pass