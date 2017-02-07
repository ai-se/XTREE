from __future__ import print_function
import pandas as pd
from os import walk
from pdb import set_trace
import csv
import re

def do():
  for (a,b,c) in walk('./'):
    if not '.svn' in a:
      if not a =='./':
        for file in c:
          if '.csv' in file:
            print(a+'/'+file)
            arff = pd.read_csv(a+'/'+file)
            # set_trace()
            tags = arff.columns.values
            first3 = ['?'+h for h in tags[0:3]]
            indep = ['$'+h for h in tags[3:-1]]
            header = first3+indep
            header.append('?>'+tags[-1])
            # set_trace()
            # name = []
            with open(a+'/'+file, 'w+') as csvfile:
              writer = csv.writer(csvfile, delimiter=',', quotechar='|')
              writer.writerow(header)
              for body in arff.values:
                writer.writerow(body)
          # else:
          #   print('arff' in file)
          #   # set_trace()

if __name__ == '__main__':
  do()