from __future__ import print_function
from scipy.io.arff import loadarff
from os import walk
from pdb import set_trace
import csv
import re

def do():
  for (a,b,c) in walk('./'):
    if not '.svn' in a:
      if not a =='./':
        for file in c:
          if 'arff' in file:
            print(a+'/'+file)
            arff = loadarff(a+'/'+file)
            tags = [aa for aa in arff[1]]
            header = ['$'+h for h in tags[:-1]]
            header.append('$>'+tags[-1])
            # set_trace()
            name = []
            with open(a+'/'+re.sub('.arff|[ ]','',file)+'.csv', 'w+') as csvfile:
              writer = csv.writer(csvfile, delimiter=',', quotechar='|')
              writer.writerow(header)
              for body in arff[0].tolist():
                writer.writerow(body)
          # else:
          #   print('arff' in file)
          #   # set_trace()

if __name__ == '__main__':
  do()