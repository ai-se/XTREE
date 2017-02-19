from __future__ import print_function, division

import os
import sys
from pdb import set_trace

from glob2 import glob

# Update path
root = os.path.join(os.getcwd().split('src')[0], 'src')
if root not in sys.path:
    sys.path.append(root)


def get_train_test(dataname="Jureczko"):
    """
    Get training and testing datasets
    :param dataname: 
    :return: 
    """
    train, test = [], []
    projects = glob(os.path.join(dataname, "*"))
    for f_name in projects:
        train.append(glob(os.path.join(f_name, "*"))[:-1])
        test.append(glob(os.path.join(f_name, "*"))[-1])
    yield train, test


if __name__ == "__main__":
    train, test = get_train_test()
    set_trace()
