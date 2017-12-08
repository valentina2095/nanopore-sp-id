#! /usr/bin/env python3

#import os
import sys
import pickle
from Bio import Entrez
import argparse

parser = argparse.ArgumentParser(description='download GI or accession numbers\
                                 from GenBank.')
parser.add_argument('email', metavar='name@example.com', type=str, help='email\
                    for NCBI Entrez tools')
parser.add_argument('-s', metavar='ORGANISM', type=str, help='search phrase\
                    . e.g. Rodentia[organism:exp]')
parser.add_argument('-t', metavar='ID TYPE', type=str, help='ACC for accession\
                    numbers or GI for GI numbers. Defaults to ACC.')

args = parser.parse_args()

Entrez.email = args.email
organism = args.org

typeid = args.t if args.t else 'ACC'


total = []

rmax = 10000
i = 0
while True:
    handle = Entrez.esearch(db='nuccore', term=search_phrase, retstart=i*rmax,
                           retmax=rmax, rettype='gbwithparts', retmode='text',
                           idtype=typeid)

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
