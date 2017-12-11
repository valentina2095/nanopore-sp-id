#! /usr/bin/env python3

# http://biopython.org/DIST/docs/tutorial/Tutorial.html#htoc88

from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
from Bio import SeqIO
import argparse
import sys

parser = argparse.ArgumentParser(description='blast fasta or fastq reads\
                                against the NCBI nucleotide database.',
                                formatter_class=(argparse
                                .ArgumentDefaultsHelpFormatter))
parser.add_argument('input', type=str, help='input file, fasta and fastq\
                    formats are accepted.')
parser.add_argument('-o', '--output', default='blast_record.xml', type=str,
                    help='desired output file name.')
parser.add_argument('-e', '--expect', default=10, type=int, help='expect value\
                    cutoff.')
#parser.add_argument('--blasthelp',)

args = parser.parse_args()
# print(args)

if args.blasthelp:
    help(NCBIWWW.qblast)

# Define var filetype
# https://stackoverflow.com/users/7802200/arya-mccarthy
# def is_fasta(filename):
#     with open(filename, "r") as handle:
#         fasta = SeqIO.parse(handle, "fasta")
#         return any(fasta)  # False when `fasta` is empty, i.e. wasn't a FASTA file
#
# is_fasta(my_file)
# # False

read_file = open(args.input, 'r')
reads = SeqIO.parse(read_file, filetype)

out_handle = open(args.output, 'a')

#for query in reads:
    # result_handle = NCBIWWW.qblast('blastn', 'nt', query.seq, megablast=True, format_type='Text', expect=args.expect) # query can be a GI number, fasta file, sequence, SeqRecord
    # saving the result handle
#    out_handle.write(result_handle.read())
#    result_handle.close()

# parse output
# result_handle = open('my_blast.xml','r')
# blast_records = NCBIXML.parse(result_handle)
# for blast_record in blast_records:
