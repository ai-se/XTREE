from __future__ import print_function, division

__author__ = 'rkrsn'
from Planners.xtree import xtree
from Planners.xtree2 import xtree as xtree2
from tools.sk import rdivDemo
from tools.oracle import *
# Timing
import numpy as np


class temporal:
    def __init__(self):
        pass

    def deltas(self):
        from collections import Counter
        counts = {}

        def save2plot(header, counts, labels, N):
            for h in header: say(h + ' ')
            print('')
            for l in labels:
                say(l[1:] + ' ')
                for k in counts.keys():
                    print("%0.2f " % (counts[k][l] * 100 / N), end="")
                print('')

        for name in ['ant', 'ivy', 'jedit', 'lucene', 'poi']:
            print("##", name)
            e = []
            train, test = explore(dir='Data/Jureczko/', name=name)
            for planners in [xtree]:  # , method1, method2, method3]:
                # aft = [planners.__doc__]
                for _ in xrange(10):
                    keys = []
                    everything, changes = planners(train, test, justDeltas=True)
                    for ch in changes: keys.extend(ch.keys())
                    counts.update({planners.__doc__: Counter(keys)})
            header = ['Features'] + counts.keys()
            save2plot(header, counts, everything, N=len(changes))

    def deltas0(self):
        from collections import Counter
        counts = {}

        def save2plot(header, counts, labels, numCh, N):
            #   for h in header: say(h+' ')
            print('')
            for id, l in enumerate(labels):
                # say(l[1:]+' ')
                #   for k in counts.keys():
                # print(counts[k])
                try:
                    if numCh[l] / N > 0.2:
                        # print(numCh[l]/N)
                        say(l[1:] + " %d %0.2f %0.2f %0.2f" % (
                            id + 1, np.median(counts[l]), np.percentile(counts[l], 25), np.percentile(counts[l], 75)))
                    else:
                        say(l[1:] + " %d 0 0 0" % (id + 1))

                except:
                    # set_trace()
                    say(l[1:] + " %d 0 0 0" % (id + 1))
                # set_trace()
                print('')
                # set_trace()

        for name in ['ant', 'ivy', 'jedit', 'lucene', 'poi']:
            print("##", name)
            e = []
            train, test = explore(dir='Data/Jureczko/', name=name)
            for planners in [xtree]:
                # keys=[]
                everything, changes = planners(train, test, justDeltas=True)
                keys = everything.values.tolist()
                # set_trace()
                for k in keys: counts.update({k: []})
                f_chCount = []
                for _ in xrange(5):
                    everything, changes = planners(train, test, justDeltas=True)
                    for c in changes:
                        for key in c.keys():
                            f_chCount.append(key)
                            counts[key].append(c[key])

            # set_trace()
            header = ['Features'] + counts.keys()
            save2plot(header, counts, everything, numCh=Counter(f_chCount), N=len(changes) * 5)

    def improve(self):
        for name in ['ant', 'lucene', 'poi', 'ivy', 'jedit']:
            print("##", name)
            e = []
            train, test = explore(dir='Data/Jureczko/', name=name)
            for planners in [xtree]:  # , method1, method2, method3]:
                aft = [planners.__doc__]
                for _ in xrange(10):
                    aft.append(planners(train, test, justDeltas=False))
                    # set_trace()
                e.append(aft)
            try:
                rdivDemo(e, isLatex=False, globalMinMax=True, high=100, low=0)
            except:
                set_trace()


def validate_xtree():
    e = {
        "Stab": [],
        "Cons": [],
        "Disc": []
    }
    for name in ['ant', 'ivy', 'jedit', 'lucene', 'poi']:
        print("##", name)
        train, test = explore(dir='Data/Jureczko/', name=name)
        stab = [name]
        disc = [name]
        for _ in xrange(10):
            aft = xtree2(train, test)
            stab.append(aft[0])
            disc.append(aft[1])
        e["Stab"].append(stab)
        e["Disc"].append(disc)
    rdivDemo(e["Stab"])
    rdivDemo(e["Disc"])


if __name__ == '__main__':
    temporal().improve()
