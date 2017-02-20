"""
Truncate csv file to remove unwanted columns.
  
Warning: DO NOT USE IF YOU ARE NOT SURE WHY THIS MUST BE RUN. CONTACT AUTHOR.
"""
import os, sys
from pdb import set_trace

import pandas as pd
from glob2 import glob


def change_class_to_bool(fname):
    old = pd.read_csv(fname)
    old.loc[old[old.columns[-1]] > 0, old.columns[-1]] = True
    old.loc[old[old.columns[-1]] <= 0, old.columns[-1]] = False
    old[old.columns[3:]].to_csv(fname, index=False)


if __name__ == "__main__":
    res = glob("./**/*.csv")
    for fname in res:
        change_class_to_bool(os.path.abspath(fname))
    set_trace()
