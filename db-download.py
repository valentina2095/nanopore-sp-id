#! /usr/bin/env python3

import os
import os.path
import sys
from Bio import Entrez
from Bio import SeqIO
import datetime
import time
import glob

Entrez.email = 'vsanche1@eafit.edu.co'

organism = 'Rodentia'
strain = ''
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
            search_phrase = search_phrase + ' AND (' + n + ncbi_terms[index] + ')'
    if index == len(ncbi_values)-1 and n != '' and type(n) is not list:
        search_phrase = search_phrase + ' AND (' + n + ncbi_terms[index] + ')'
    if index == len(ncbi_values)-1 and n != '' and type(n) is list:
        for name in n:
            name = name.lstrip()
            search_phrase = search_phrase + ' AND (' + name + ncbi_terms[index] + ')'


print('\n Here is the complete search line that will be used: \n', search_phrase)

start_ret = 15000+2101
for i in range(1,5):
    handle = Entrez.esearch(db='nuccore', term=search_phrase, retstart = start_ret,retmax=10000-2101, rettype='gbwithparts', retmode="text",idtype="acc")
    print('\nThe esearch is complete')

    result = Entrez.read(handle, validate=False)
    handle.close()
    acc_numbers = result['IdList']

    #########################
    # Solo fasta por ahora
    new_path = 'Genbank_Rodentia_Files/'
    if not os.path.exists(new_path):
        os.makedirs(new_path)

    start_day = datetime.date.today().weekday() # 0 is Monday, 6 is Sunday
    start_time = datetime.datetime.now().time()

    if ((start_day < 5 and start_time > datetime.time(hour=21)) or (start_day < 5 and start_time < datetime.time(hour=5)) or start_day >= 5 or len(acc_numbers) <= 100 ):
        print('\nCalling Entrez...')

        auxiliar = 1
        for acc in acc_numbers:
            if ((datetime.date.today().weekday() < 5 and datetime.datetime.now().time() > datetime.time(hour=21)) or
                (datetime.date.today().weekday() < 5 and datetime.datetime.now().time() < datetime.time(hour=5)) or
                (datetime.date.today().weekday() == start_day + 1 and datetime.datetime.now().time() < datetime.time(hour=5)) or
                (datetime.date.today().weekday() >= 5) or len(acc_numbers) <= 100 ):

                print('\nDownloading file %s of %s   (%s' %(auxiliar, len(acc_numbers), 100*auxiliar/len(acc_numbers)) + '%)')

                handle=Entrez.efetch(db='nuccore', rettype='gbwithparts', retmode='text', id=acc)
                FILENAME =  new_path + acc + '.fna'
                local_file=open(FILENAME,'w')
                SeqIO.write(SeqIO.parse(handle, 'genbank'), local_file, "fasta")
                handle.close()
                local_file.close()
                auxiliar += 1
            else:
                print('\nYou have too many files to download at the time. Try again later.')
                print('The last accession we were able to download was %s, corresponding to %s of nuccore'  %s(acc, start_ret+auxiliar))
    start_ret += 10000
