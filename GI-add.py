#! /usr/bin/env python3

import os
import sys
import pickle
from Bio import SeqIO

files = sys.argv[1]

if os.path.exists('GI.pickle'):
    with open('GI.pickle', 'rb') as gi_file:
        gi = pickle.load(gi_file)
else:
    print('There is no GI.pickle in the current directory')
    sys.exit()

if os.path.exists('acc.pickle'):
    with open('acc.pickle', 'rb') as acc_file:
        acc = pickle.load(acc_file)
else:
    print('There is no acc.pickle in the current directory')
    sys.exit()

# from: >NM_001357748.1 Mus musculus coatomer protein complex
# to:   >gi|1274096202|ref|NM_001357748.1| Mus musculus coatomer protein complex
for fna in os.listdir(files):
    try:
        ind = acc.index(os.path.splitext(fna)[0])

        with open(files + '/' + fna, 'rU') as handle:
            record = SeqIO.read(handle, 'fasta')

            if not 'gi|' in record.id:
                # print(fna)
                with open(files + '/' + fna, 'w') as out:
                    out.write('>gi|'+gi[ind]+'|ref|'+record.id+'|'+record.description[len(record.id):]+'\n'+str(record.seq))

    except ValueError:
        print('ERROR: This search does not include the acc. number', fna)
