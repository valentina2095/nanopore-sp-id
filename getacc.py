#! /usr/bin/env python3

import os
import sys
from Bio import Entrez

Entrez.email = 'vsanche1@eafit.edu.co'

search_phrase = 'Rodentia[organism:exp]'


handle = Entrez.esearch(db='nuccore', term=search_phrase, retstart=sys.argv[1], retmax=50000,
         rettype='gbwithparts', retmode='text', idtype='acc')
acc_result = Entrez.read(handle, validate = False)
acc = list(acc_result['IdList'])
handle.close()

if os.path.exists('acc.txt'):
    with open('acc.txt', 'r') as acc_old:
        prev = (acc_old.read()[2:-2].split("', '"))
        acc.extend(prev)

with open('acc.txt', 'a') as out:
    out.write(str(acc))

print('Done with acc')
