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
    :param dataname: Source of data
    :return: 
    """
    source, target = [], []
    projects = [p for p in glob(os.path.join(root, "Data", dataname, "*")) if os.path.isdir(p)]
    for f_name in projects:
        data = glob(os.path.join(f_name, "*.csv"))
        source.append(data[:-1])
        target.append(data[-1])
    return source, target


if __name__ == "__main__":
    train, test = get_train_test()
    set_trace()
