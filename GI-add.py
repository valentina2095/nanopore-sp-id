#! /usr/bin/env python3

import os
import os.path
import sys
from Bio import Entrez
from Bio import SeqIO

fnas = sys.argv[1:]

Entrez.email = 'vsanche1@eafit.edu.co'

search_phrase = 'Rodentia[organism:exp]'

handle = Entrez.esearch(db='nuccore', term=search_phrase, retmax=500,
         rettype='gbwithparts', retmode='text', idtype='GI')
gi_result = Entrez.read(handle, validate = False)
gi = list(gi_result['IdList'])
handle.close()
print('Done with GI')

handle2 = Entrez.esearch(db='nuccore', term=search_phrase, retmax=500,
         rettype='gbwithparts', retmode='text', idtype='acc')
acc_result = Entrez.read(handle2, validate = False)
acc = list(acc_result['IdList'])
handle.close()
print('Done with accession numbers,', 'NM_001357748.1' in acc)

# from: NM_001357748.1 Mus musculus coatomer protein complex
# to:   gi|1274096202|ref|NM_001357748.1| Mus musculus coatomer protein complex
for fna in fnas:
    try:
        ind = acc.index(fna[:-4])
        with open(fna, 'rU') as handle:
            seq = SeqIO.read(handle, 'fasta')
            print('bien\n')
        with open(fna, 'w') as out:
            out.write('>gi|'+gi[ind]+'|ref|'+seq.id+'|'+seq.description[len(seq.id):]+'\n'+seq.id)

    except ValueError:
        print('ERROR: This search does not include the acc. number', fna[:-4])
