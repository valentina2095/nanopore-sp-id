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
parser.add_argument('--gi', action='store_true', default=False,
                    help='whether to give \'gi\' identifier.')
parser.add_argument('-d', '--descriptions', default=500, type=int,
                    help='number of descriptions to show.')
parser.add_argument('-a', '--alignments', default=500, type=int,
                    help='number of alignments to show.')
parser.add_argument('-e', '--expect', default=10, type=int,
                    help='expect value cutoff.')
parser.add_argument('-f', '--filter', default=None, type=str,
                    help='turn on filtering.')
parser.add_argument('-q', '--query', type=str,
                    help='entrez query to limit Blast search.')
parser.add_argument('--hits', default=50, type=int,
                    help='number of hits to return.')
parser.add_argument('--megablast', action='store_true',
                    help='whether to use MEga BLAST algorithm.')
parser.add_argument('--blasthelp', action='store_true',
                    help='show blast options.')

args = parser.parse_args()
print(args)

if args.blasthelp:
    help(NCBIWWW.qblast)
    sys.exit()

# Define var filetype
# https://stackoverflow.com/users/7802200/arya-mccarthy
def is_type(filename, filetype):
    with open(filename, 'rU') as handle:
        read = SeqIO.parse(handle, filetype)
        return read#any(read)  # False when `read` is empty

# read_file = open(args.input, 'r')

print(is_type(args.input, 'fasta'))
print(is_type(args.input, 'fastq'))

# out_handle = open(args.output, 'a')

# #for query in reads:
#     # result_handle = NCBIWWW.qblast('blastn', 'nt', query.seq, megablast=True, format_type='Text', expect=args.expect) # query can be a GI number, fasta file, sequence, SeqRecord
#     # saving the result handle
# #    out_handle.write(result_handle.read())
# #    result_handle.close()

# # parse output
# # result_handle = open('my_blast.xml','r')
# # blast_records = NCBIXML.parse(result_handle)
# # for blast_record in blast_records:
