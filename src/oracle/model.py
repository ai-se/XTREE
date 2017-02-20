from __future__ import division

import os
import sys
from pdb import set_trace
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from Utils.FileUtil import list2dataframe
from sklearn.metrics import roc_curve, roc_auc_score
from smote import SMOTE

root = os.path.join(os.getcwd().split('src')[0], 'src')
if root not in sys.path:
    sys.path.append(root)


def getTunings(fname):
    raw = pd.read_csv(root + '/old/tunings.csv').transpose().values.tolist()
    formatd = pd.DataFrame(raw[1:], columns=raw[0])
    try:
        return formatd[fname].values.tolist()
    except KeyError:
        return None


def rforest(train, target):
    clf = RandomForestClassifier(n_estimators=100, random_state=1)
    source = list2dataframe(train)
    features = source.columns[:-1]
    klass = source[source.columns[-1]]
    clf.fit(source[features], klass)
    preds = clf.predict(target[target.columns[:-1]])
    distr = clf.predict_proba(target[target.columns[:-1]])[:, 1]

    # Find a threshold for cutoff
    try:
        pseudo_train = list2dataframe(train[:-1])
        pseudo_test = list2dataframe(train[-1])
        thresh = 0.5
        klass0 = pseudo_train[pseudo_train.columns[-1]]
        clf.fit(pseudo_train[features], klass0)
        distribution = clf.predict_proba(pseudo_test[pseudo_test.columns[:-1]])
        fpr, tpr, thresholds = roc_curve(pseudo_test[pseudo_test.columns[-1]], distribution[:, 1])
        cutoff = 0.66
        for a, b, c in zip(fpr, tpr, thresholds):
            if b > cutoff and a < 1-cutoff:
                thresh = c
        # Apply cutoff
        preds = [1 if val < thresh else 0 for val in distr]
    except ValueError:
        pass

    return preds, distr


def _test_model():
    pass


if __name__ == '__main__':
    _test_model()
