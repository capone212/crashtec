'''
Created on 24.02.2013

@author: capone
'''
import collections

l3 = [100, 200]
l2 = [10, 11, l3]
l = [1, 2, 3, l2]

def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el

for x in flatten(l):
    print x
