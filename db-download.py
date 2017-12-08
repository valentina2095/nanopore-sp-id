#! /usr/bin/env python3

import os
import os.path
import sys
from Bio import Entrez
from Bio import SeqIO
import datetime
import time
import glob
import argparse

parser = argparse.ArgumentParser(description='download specific database from\
                                GenBank.')
parser.add_argument('email', metavar='name@example.com', type=str, help='email\
                    for NCBI Entrez tools')
parser.add_argument('--org', metavar='ORGANISM', type=str, help='add organism\
                    scientific name, Genbank common name or Taxonomy ID. (e.g.\
                    Rodentia, 9989)')
parser.add_argument('--strain', type=str, help='add the\
                    strain to search for. (e.g. HUSEC2011)')
parser.add_argument('--start', type=int, help='starting point for esearch,\
                    Defaults to 0.')

args = parser.parse_args()

Entrez.email = args.email

organism = args.org
strain = args.strain
keywords = ''
search_phrase = ''

if ',' in keywords:
    keywords = keywords.split(',')

ncbi_terms = ['[organism:exp]', '[strain]', '[keyword]']
ncbi_values = [organism, strain, keywords]

for index, n in enumerate(ncbi_values):
    if index == 0 and n != '':
        search_phrase = '(' + n + ncbi_terms[index] + ')'
    else:
        if n != '' and index != len(ncbi_values)-1:
            search_phrase = search_phrase + ' AND (' + n + ncbi_terms[index] + \
            ')'
    if index == len(ncbi_values)-1 and n != '' and type(n) is not list:
        search_phrase = search_phrase + ' AND (' + n + ncbi_terms[index] + ')'
    if index == len(ncbi_values)-1 and n != '' and type(n) is list:
        for name in n:
            name = name.lstrip()
            search_phrase = search_phrase + ' AND (' + name + ncbi_terms[index]\
            + ')'


print('\n Here is the complete search line that will be used: \n', search_phrase)

unprocessed = []

rstart = args.start if args.start else 0
rmax = 2000
for i in range(5):
    handle = Entrez.esearch(db='nuccore', term=search_phrase,
    retstart = rstart+i*rmax, retmax=rmax, rettype='gbwithparts',
    retmode="text",idtype="acc")
    print('\nThe esearch is complete')

    result = Entrez.read(handle, validate=False)
    handle.close()
    acc_numbers = result['IdList']

    new_path = 'Genbank_Rodentia_casa/'
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    else:
        previous = os.listdir(new_path)

    start_day = datetime.date.today().weekday() # 0 is Monday, 6 is Sunday
    start_time = datetime.datetime.now().time()

    if ((start_day < 5 and start_time > datetime.time(hour=21)) or (start_day <
    5 and start_time < datetime.time(hour=5)) or start_day >= 5 or len(acc_numbers) <= 100 ):
        print('\nCalling Entrez...')

        auxiliar = 1
        for acc in acc_numbers:
            if ((datetime.date.today().weekday() < 5 and
                datetime.datetime.now().time() > datetime.time(hour=21)) or
                (datetime.date.today().weekday() < 5 and
                datetime.datetime.now().time() < datetime.time(hour=5)) or
                (datetime.date.today().weekday() == start_day + 1 and
                datetime.datetime.now().time() < datetime.time(hour=5)) or
                (datetime.date.today().weekday() >= 5) or len(acc_numbers) <=
                100) and (not acc in previous):

                print('Downloading file %s of %s   (%s' %(auxiliar,
                len(acc_numbers), 100*auxiliar/len(acc_numbers)) + '%)')

                try:
                    handle=Entrez.efetch(db='nuccore', rettype='gbwithparts',
                    retmode='text', id=acc)
                    FILENAME =  new_path + acc + '.fna'
                    local_file=open(FILENAME,'w')
                    SeqIO.write(SeqIO.parse(handle, 'genbank'), local_file,
                    "fasta")
                    handle.close()
                    local_file.close()
                    auxiliar += 1
                except:
                    unprocessed.append(acc)
            else:
                print('\nYou have too many files to download at the time. Try again later.')
                print('The last accession we were able to download was %s, corresponding to %s of nuccore'  %(acc, rstart+auxiliar))

print('unprocessed files:', unprocessed)
