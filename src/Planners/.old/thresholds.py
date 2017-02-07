"""
CK Thresholds
"""
from __future__ import print_function, division
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import f_classif, f_regression
import sys
import texttable
sys.path.append('..')
from tools.oracle import *
from pdb import set_trace



def VARL(coef,inter,p0=0.05):
  return (np.log(p0/(1-p0))-inter)/coef

def thresholds():
  for name in ['ant', 'ivy', 'jedit', 'lucene', 'poi']:
    print("##", name)
    train, test = explore(dir='../Data/Jureczko/', name=name)
    data_DF=csv2DF(train, toBin=True)
    metrics=[str[1:] for str in data_DF[data_DF.columns[:-1]]]
    ubr = LogisticRegression()
    X = data_DF[data_DF.columns[:-1]].values
    y = data_DF[data_DF.columns[-1]].values
    ubr.fit(X,y)
    inter, coef, pVal = ubr.intercept_[0], ubr.coef_[0], f_classif(X,y)[1]

    table= texttable.Texttable()
    table.set_cols_align(["l","l","l"])
    table.set_cols_valign(["m","m","m"])
    table.set_cols_dtype(['t', 't', 't'])
    table_rows=[["Metric", "Threshold", "P-Value"]]

    for i in xrange(len(metrics)):
      if VARL(coef[i], inter, p0=0.05)>0 and pVal[i]<0.05:
        thresh="%0.2f"%VARL(coef[i], inter, p0=0.1)
        table_rows.append([metrics[i], thresh, "%0.3f"%pVal[i]])

    table.add_rows(table_rows)
    print(table.draw())

  # === DEBUG ===
  set_trace()
  return None

if __name__=="__main__":
  thresholds()
  pass
