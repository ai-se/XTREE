from __future__ import division

import sys
from pdb import set_trace

sys.dont_write_bytecode = True


class Abcd:
    def __init__(i, db="all", rx="all"):
        i.db = db;
        i.rx = rx;
        i.yes = i.no = 0
        i.known = {};
        i.a = {};
        i.b = {};
        i.c = {};
        i.d = {}

    def __call__(i, actual=None, predicted=None):
        return i.keep(actual, predicted)

    def tell(i, actual, predict):
        i.knowns(actual)
        i.knowns(predict)
        if actual == predict:
            i.yes += 1
        else:
            i.no += 1
        for x in i.known:
            if actual == x:
                if predict == actual:
                    i.d[x] += 1
                else:
                    i.b[x] += 1
            else:
                if predict == x:
                    i.c[x] += 1
                else:
                    i.a[x] += 1

    def knowns(i, x):
        if not x in i.known:
            i.known[x] = i.a[x] = i.b[x] = i.c[x] = i.d[x] = 0.0
        i.known[x] += 1
        if (i.known[x] == 1):
            i.a[x] = i.yes + i.no


    def ask(i):
        def p(y):
            return int(100 * y + 0.5)

        def n(y):
            return int(y)

        pd = pf = pn = prec = g = f = acc = 0
        for x in i.known:
            if x == 1: # Only for defects (x=0 -> no defects)
                a = i.a[x];
                b = i.b[x];
                c = i.c[x];
                d = i.d[x]
                if (b + d): pd = d / (b + d)
                if (a + c): pf = c / (a + c)
                if (a + c): pn = (b + d) / (a + c)
                if (c + d): prec = d / (c + d)
                if (1 - pf + pd): g = 2 * (1 - pf) * pd / (1 - pf + pd)
                if (prec + pd): f = 2 * prec * pd / (prec + pd)
                if (i.yes + i.no): acc = i.yes / (i.yes + i.no)
                return p(pd), p(pf), p(prec)


def _Abcd(before=None, after=None):
    abcd = Abcd(db='Actual', rx='Predicted')
    train = before
    test = after
    for actual, predicted in zip(train, test):
        abcd.tell(actual, predicted)

    return abcd.ask()


if __name__ == "__main__":
    _Abcd()
