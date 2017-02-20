from __future__ import division

import os
import sys

import pandas as pd
from sklearn.ensemble import RandomForestClassifier

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


def rforest(source, target):
    clf = RandomForestClassifier(n_estimators=100, random_state=1)
    try:
        source = SMOTE(source)
    except ValueError:
        pass
    features = source.columns[:-1]
    klass = source[source.columns[-1]]
    set_trace()
    clf.fit(source[features], klass)
    preds = clf.predict(target[target.columns[:-1]])
    distr = clf.predict_proba(target[target.columns[:-1]])
    return preds, distr[:, 1]


def _test_model():
    pass


if __name__ == '__main__':
    _test_model()
