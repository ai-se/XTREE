#! /Users/rkrsn/miniconda/bin/python
from __future__ import print_function
from __future__ import division
from os import environ
from os import getcwd
from pdb import set_trace
from random import uniform as rand
from random import randint as randi
import sys

# Update PYTHONPATH
HOME = environ['HOME']
axe = HOME + '/git/axe/axe/'  # AXE
pystat = HOME + '/git/pystat/'  # PySTAT
cwd = getcwd()  # Current Directory
sys.path.extend([axe, pystat, '../'])

from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from Planners.XTREE.lib.weights import weights as W

from Prediction import *
# from Planners.XTREE.lib.settingsWhere import o
from cliffsDelta import *
from hist import *
from smote import *
import Planners.XTREE.lib.makeAmodel as mam
from methods1 import *
import numpy as np
import pandas as pd
from counts import *
# import sk


class o:

  def __init__(i, **d):
    i.has().update(**d)

  def has(i):
    return i.__dict__

  def update(i, **d):
    i.has().update(d)
    return i

  def __repr__(i):
    show = [':%s %s' % (k, i.has()[k])
            for k in sorted(i.has().keys())
            if k[0] is not "_"]
    txt = ' '.join(show)
    if len(txt) > 60:
      show = map(lambda x: '\t' + x + '\n', show)
    return '{' + ' '.join(show) + '}'


def settings(**d):
  return o(
      name="WHAT",
      what="WHAT - A Contrast Set Planner",
      author="Rahul Krishna",
      copyleft="(c) 2014, MIT license, http://goo.gl/3UYBp",
      seed=1,
      f=None,
  ).update(**d)

opt = settings()


class vertex():

  def __init__(self, ID, rows):
    self._id = ID
    self.rows = rows
    self.represent = None

  def score(self):
    return np.mean([r.cells[-2] for r in self.rows])

  def representative(self, method='mean'):
    if method == 'mean':
      return [float(np.mean([k.cells[indx] for k in self.rows]))
              for indx in xrange(len(self.rows[0].cells) - 2)]
    elif method == 'median':
      return [float(np.median([k.cells[indx] for k in self.rows]))
              for indx in xrange(len(self.rows[0].cells) - 2)]
    elif method == 'best':
      return sorted(self.rows, key=lambda F: F.cells[-2])[0].cells[:-2]
    elif method == 'any':
      return any(self.rows).cells[:-2]


class treatments():

  def __init__(
          self,
          train,
          test,
          bin=False,
          far=True,
          method='best',
          train_df=None,
          test_df=None,
          fSelect=True,
          Prune=True,
          infoPrune=0.25,
          extent=0.75):
    self.test, self.train = test, train
    self.extent = extent
    self.fSelect = fSelect
    self.Prune = Prune
    self.method = method
    self.infoPrune = infoPrune
    self.far = far
    self.bin = bin
    self.new_Tab = []
    self.train_df = train_df if train_df \
        else createTbl(self.train, isBin=False, bugThres=1)

    self.test_df = test_df if test_df \
        else createTbl(self.test, isBin=False, bugThres=1)

  def clusterer(self):
    IDs = list(set([f.cells[-1] for f in self.train_df._rows]))
    clusters = []
    for _id in list(set(IDs)):

      clusters.append(vertex(ID=_id, rows=[f for f in self.train_df._rows
                                           if f.cells[-1] == _id]))
    return clusters

  def knn(self, one, two):
    pdistVect = []
#    set_trace()
    for ind, n in enumerate(two):
      pdistVect.append([ind,
                        euclidean(one.representative(method=self.method),
                                  n.representative(method=self.method))])
    indices = sorted(pdistVect, key=lambda F: F[1], reverse=self.far)
    return [two[n[0]] for n in indices]

  def getHyperplanes(self):
    hyperPlanes = []
    ClusterRows = self.clusterer()
    while ClusterRows:
      one = ClusterRows.pop()
      try:
        two = self.knn(one, ClusterRows)[1]
      except IndexError:
        two = one
      hyperPlanes.append([one, two])
    return hyperPlanes

  def projection(self, node_one, node_two, three):
    if node_one.score() < node_two.score():
      one, two = node_one, node_two
    else:
      one, two = node_two, node_one
    plane = [
        b - a for a,
        b in zip(
            one.representative(
                method=self.method),
            two.representative(
                method=self.method))]
    norm = np.linalg.norm(plane)
    unitVect = [p / norm for p in plane]
    proj = np.dot(three, unitVect)
    return proj

  def fWeight(self, criterion='Variance'):
    lbs = W(use=criterion).weights(self.train_df)
    sortedLbs = sorted(
        [l / max(lbs[0]) if max(lbs[0]) else 0 for l in lbs[0]], reverse=True)
    indx = int(self.infoPrune * len(sortedLbs)) - 1 if self.Prune else -1
    cutoff = sortedLbs[indx]
    L = [l / max(lbs[0]) if max(lbs[0]) else 0 for l in lbs[0]]
    return [0 if l < cutoff else l for l in L] if self.Prune else L

  def mutate(self, me, others):

    def new(my, good, extent, f=None):
      if my == good:
        return my
      elif f:
        return good if rand() < extent * f else my
      else:
        return good if rand() < extent else my

    def one234(pop, f=lambda x: id(x)):
      seen = []

      def oneOther():
        x = any(pop)
        while f(x) in seen:
          x = any(pop)
        seen.append(f(x))
        return x
      return oneOther()
    two = one234(others.rows)
    if self.bin:
      if self.fSelect:
        return [new(my, good, self.extent, f=f) for f, my, good in zip(
                opt.f, me[:-2], others.representative(method=self.method))]
      else:
        return [new(my, good, self.extent) for f, my, good in zip(
                opt.f, me[:-2], others.representative(method=self.method))]

    else:
      if self.fSelect:
        return [my + self.extent * f * (good - my) for f, my, good in zip(
            opt.f, me[:-2], others.representative(method=self.method))]
      else:
        return [my + self.extent * (good - my) for f, my, good in zip(
            opt.f, me[:-2], others.representative(method=self.method))]

  def main(self):
    hyperPlanes = self.getHyperplanes()
    opt.f = self.fWeight()
    aa = []
    for rows in self.test_df._rows:
      aa.append(rows.cells[:-2])
      newRow = rows
#       if rows.cells[-2] > 0:
      vertices = sorted(
          hyperPlanes,
          key=lambda F: self.projection(
              F[0],
              F[1],
              rows.cells[
                  :-2]),
          reverse=True)[0]
      [good, bad] = sorted(vertices, key=lambda F: F.score())
      newRow.cells[:-2] = self.mutate(rows.cells, good)
      self.new_Tab.append(newRow)
#     for gg, ff in zip(self.train_df._rows, self.test_df._rows):
#       print([b - a for b, a in zip(gg.cells[:-2], ff.cells[:-2])])
    # scatterPlot(train=self.train_df, test=aa, delta=self.new_Tab).pcaProj()

    return clone(
        self.test_df, rows=[r.cells for r in self.new_Tab], discrete=True)


def testPlanner2():
  dir = '../Data'
  one, two = explore(dir)
  fWeight = treatments(one[0], two[0]).fWeight(criterion='Variance')
  set_trace()

if __name__ == '__main__':
  testPlanner2()
