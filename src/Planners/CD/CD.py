"""
XTREE
"""
from __future__ import print_function, division
import sys
sys.path.append('..')
from tools.sk import *
from tools.oracle import *
from tools.where import where
from random import choice
from scipy.spatial.distance import euclidean as edist
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
    return np.argsort(lbs)[::-1]

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



class node:
  """
  A data structure to hold all the rows in a cluster.
  Also return an exemplar: the centroid.
  """

  def __init__(i, rows, what='centroid'):
    i.rows = []
    for r in rows:
      i.rows.append(r)
    i.sample = i.exemplar(what)

  def exemplar(i, what='choice'):
    if what == 'choice':
      return choice(i.rows)
    if what == 'centroid':
      return np.median(np.array(i.rows), axis=0)
    elif what == 'mean':
      return np.mean(np.array(i.rows), axis=0)


class changes():
  """
  Record changes.
  """
  def __init__(i):
    i.log = {}

  def save(i, name=None, old=None, new=None):
    if not old == new:
      i.log.update({name: (old, new)})

class CD:

  def __init__(i,train,test,trainDF,testDF,fsel=True,clst=None):
    i.train=train
    i.trainDF = trainDF
    i.test=test
    i.testDF=testDF
    i.clstr=clst
    i.change =[]
    i.fsel=fsel
    if fsel:
      i.lbs = fWeight(trainDF)

  def closest(i, arr):
    """
    :param arr: np array (len=No. Indep var + No. Depen var)
    :return: float
    """
    return sorted(i.clstr, key= lambda x: edist(arr[:-1], x.sample[:-1]))

  def patchIt(i,testInst):
    testInst = testInst.values
    C = changes()
    close = i.closest(testInst)[0]
    better = [b for b in i.clstr if b.sample[-1]<testInst[-1]]
    better = sorted(i.closest(close.sample), key=lambda x: x.sample[-1])[1]
    newInst = testInst + (better.sample-close.sample)
    # set_trace()
    if i.fsel:
      old = testInst
      indx = i.lbs[:int(len(i.lbs)*0.33)]
      for n in indx:
        C.save(name=i.testDF.columns.values[n], old=testInst[n], new=newInst[n])
        testInst[n] = newInst[n]
      i.change.append(C.log)
      return testInst
    else:
      for name, then, now in zip(i.testDF.columns[:-1].values,
          testInst, newInst): C.save(name=name, old=then, new=now)
      i.change.append(C.log)
      return newInst

  def main(i, reps=10, justDeltas=False):
    newRows = [i.patchIt(i.testDF.iloc[n]) for n in xrange(i.testDF.shape[0]) if i.testDF.iloc[n][-1]>0]
    newRows = pd.DataFrame(newRows, columns=i.testDF.columns)
    before, after = rforest(i.train, newRows)
    gain = (1-sum(after)/len(after))*100
    # set_trace()
    # set_trace()
    if not justDeltas:
      return gain
    else:
      return i.testDF.columns[:-1].values, i.change


class HOW:

  def __init__(i,train,test,trainDF,testDF,fsel=False,clst=None):
    i.train=train
    i.trainDF = trainDF
    i.test=test
    i.testDF=testDF
    i.clstr = clst
    i.pairs=[]
    i.change =[]
    if fsel:
      i.fsel=fsel
      i.lbs = fWeight(trainDF)
    for n in xrange(len(clst)):
      one = clst[0]
      close = i.closest(one)[1]
      i.pairs.append((one, close))

  def closest(i, arr):
    """
    :param arr: np array (len=No. Indep var + No. Depen var)
    :return: float
    """
    return sorted(i.clstr, key= lambda x: edist(arr.sample[:-1], x.sample[:-1]))

  def patchIt(i,testInst):
    testInst = testInst.values
    C = changes()
    def proj(one, two, test):
      a = edist(one, test)
      b = edist(two, test)
      c = edist(one, two)
      return (a**2-b**2+c**2)/(2*c)
    better = sorted(i.pairs, key= lambda x: proj(x[0].sample, x[1].sample, testInst), reverse=True)[0]
    (toMe, notToMe) = (better[0], better[1]) if better[0].sample[-1]<=better[1].sample[-1] else (better[1], better[0])
    newInst = testInst + 0.5*(toMe.sample-testInst)
    # set_trace()
    if i.fsel:
      old=testInst
      indx = i.lbs[:int(len(i.lbs)*0.33)]
      for n in indx:
        C.save(name=i.testDF.columns.values[n], old=testInst[n], new=newInst[n])
        testInst[n] = newInst[n]
      i.change.append(C.log)
      return testInst
    else:
      return newInst


  def main(i, reps=10, justDeltas=False):
    newRows = [i.patchIt(i.testDF.iloc[n]) for n in xrange(i.testDF.shape[0]) if i.testDF.iloc[n][-1]>0]
    newRows = pd.DataFrame(newRows, columns=i.testDF.columns)
    before, after = rforest(i.train, newRows)
    gain = (1-sum(after)/len(after))*100
    # set_trace()
    # set_trace()
    if not justDeltas:
      return gain
    else:
      return i.testDF.columns[:-1].values, i.change

def method1(train, test, justDeltas=False):
  "CD"
  train_DF = csv2DF(train, toBin=False)
  test_DF = csv2DF(test)
  clstr = [node(x) for x in where(data=train_DF)]
  # set_trace()
  return CD(train=train, test=test, trainDF=train_DF, testDF=test_DF, clst=clstr, fsel=False).main(justDeltas=justDeltas)

def method2(train, test, justDeltas=False):
  "CD+FS"
  train_DF = csv2DF(train, toBin=False)
  test_DF = csv2DF(test)
  clstr = [node(x) for x in where(data=train_DF)]
  # set_trace()
  return CD(train=train, test=test, trainDF=train_DF, testDF=test_DF, clst=clstr, fsel=True).main(justDeltas=justDeltas)

def method3(train, test, justDeltas=False):
  "HOW"
  train_DF = csv2DF(train, toBin=False)
  test_DF = csv2DF(test)
  clstr = [node(x, what='centroid') for x in where(data=train_DF)]
  # set_trace()
  return HOW(train=train, test=test, trainDF=train_DF, testDF=test_DF, clst=clstr, fsel=True).main(justDeltas=justDeltas)

if __name__ == '__main__':
  E = []
  for name in ['ant']:#, 'ivy', 'jedit', 'lucene', 'poi']:
    print("##", name)
    train, test = explore(dir='../Data/Jureczko/', name=name)
    aft = [name]
    for _ in xrange(10):
      aft.append(method3(train, test))
    E.append(aft)
  rdivDemo(E)
