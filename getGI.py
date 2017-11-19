#! /usr/bin/env python3

#import os
import sys
import pickle
from Bio import Entrez

Entrez.email = 'vsanche1@eafit.edu.co'

search_phrase = 'Rodentia[organism:exp]'
# search_phrase = input('Enter search phrase \n')

typeid = input('Enter ID type [ GI or acc ]: ')


total = []

rmax = 10000
i = 0
while True:
    handle = Entrez.esearch(db='nuccore', term=search_phrase, retstart=i*rmax, retmax=rmax, rettype='gbwithparts', retmode='text', idtype=typeid)

    result = Entrez.read(handle, validate = False)
    data = list(result['IdList'])
    handle.close()
    total.extend(data)
    i += 1

    if len(data) == 0:
        break

with open(typeid+'.pickle', 'wb') as out:
    pickle.dump(total, out, pickle.HIGHEST_PROTOCOL)

print('Done, it retrieved a total of', len(total), typeid)
