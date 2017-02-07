from __future__ import print_function, division
__author__ = 'rkrsn'
from Planners.CD import *
from Planners.xtree import xtree
from tools.sk import rdivDemo
from tools.misc import explore, say
from tools.stats import ABCD
from tools.tune.dEvol import tuner
from tools.oracle import *
# Timing
from time import time
from logo import logo

# Parallelism
from functools import partial
from multiprocessing import Pool


def RF(indx):

  train,test = explore(dir='Data/Jureczko/')

  # print("Data,\t Pd,\t Pf,\t Pd,\t Pf")
  # print("\t,Naive,\t\t,Tuned,\t,\t")
  tr,te = train[indx],test[indx]
  print(tr[0].split('/')[-2])
  E0, E1 = [],[]
  Pd=[tr[0].split('/')[-2]]
  Pf=[tr[0].split('/')[-2]]
  G =[tr[0].split('/')[-2]]
  tunings = tuner(tr)
  actual, preds = rforest(tr, te, tunings=None, smoteit=False)
  abcd = ABCD(before=actual, after=preds)
  F = np.array([k.stats()[-2] for k in abcd()])
  Pd0 = np.array([k.stats()[0] for k in abcd()])
  Pf0 = np.array([k.stats()[1] for k in abcd()])
  init = tr[0].split('/')[-2]+'\t, %0.2f,\t %0.2f,\t'%(Pd0[1], 1-Pf0[1])
  # init1 = tr[0].split('/')[-2]+'\t, %0.2f,\t'%(F[1])

  # Tune+SMOTE
  smote= True
  actual, preds = rforest(tr, te, tunings=tunings, smoteit=True)
  abcd = ABCD(before=actual, after=preds)
  F = np.array([k.stats()[-2] for k in abcd()])
  Pd0 = np.array([k.stats()[0] for k in abcd()])
  Pf0 = np.array([k.stats()[1] for k in abcd()])
  say(init + '%0.2f,\t %0.2f\n' % (Pd0[1], 1 - Pf0[1]))
  # say(init1+'%0.2f\n'%(F[1]))
  return init+'%0.2f,\t %0.2f\n'%(Pd0[1], 1-Pf0[1])

def SVM(indx):
  train,test = explore(dir='Data/Jureczko/')
  # set_trace()
  print("Data, Pd, Pf")
  print("# %s"%(te[0].split('/')[-2]))
  for tr,te in zip(train,test):
    E0, E1 = [],[]
    # for tr in train:
    Pd=[tr[0].split('/')[-2]]
    Pf=[tr[0].split('/')[-2]]
    G =[tr[0].split('/')[-2]]
    # for _ in xrange(1):
    tunings = None #tuner(tr)
    smote= True
    # tunings = tuner(tr)
    # set_trace()
    actual, preds = rforest(tr, te, tunings=tunings, smoteit=smote)
    abcd = ABCD(before=actual, after=preds)
    F = np.array([k.stats()[-2] for k in abcd()])
    Pd0 = np.array([k.stats()[0] for k in abcd()])
    Pf0 = np.array([k.stats()[1] for k in abcd()])
    # set_trace()
    G.append(F[0])
    say(tr[0].split('/')[-2] + ', %0.2f, %0.2f\n' % (Pd0[1], 1 - Pf0[1]))

  set_trace()

def parallel():
  collect=[]
  train,test = explore(dir='Data/Jureczko/')
  n_proc = len(train)
  set_trace()
  p=Pool(processes=n_proc)
  collect.append(p.map(RF, range(n_proc)))
  for cc in collect: print(cc)
  set_trace()

def serial():
  RF(2)
  
if __name__=='__main__':
  # serial()
  parallel()
