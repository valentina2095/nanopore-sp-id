#! /usr/bin/env python3

import os
import sys
from Bio import SeqIO

files = sys.argv[1]

if os.path.exists('GI.txt'):
    with open('GI.txt', 'r') as gi_file:
        gi = (gi_file.read()[2:-2].split("', '"))

if os.path.exists('acc.txt'):
    with open('acc.txt', 'r') as acc_file:
        acc = (acc_file.read()[2:-2].split("', '"))

# from: NM_001357748.1 Mus musculus coatomer protein complex
# to:   gi|1274096202|ref|NM_001357748.1| Mus musculus coatomer protein complex
for fna in os.listdir(files):
    try:
        if fna.endswith('.fna'):
            ind = acc.index(fna[:-4])
        if fna.endswith('.fasta'):
            ind = acc.index(fna[:-6])

        with open(files + '/' + fna, 'rU') as handle:
            seq = SeqIO.read(handle, 'fasta')

        with open(files + '/' + fna, 'w') as out:
            out.write('>gi|' + gi[ind] + '|ref|' + seq.id + '|' + \
            seq.description[len(seq.id):] + '\n' + seq.id + '\n')

    except ValueError:
        print('ERROR: This search does not include the acc. number', fna)
