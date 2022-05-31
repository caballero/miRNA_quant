#!/usr/bin/env python3

# Script to deduplicate a fasta file based on sequence similarity
# it assume sequences are in fasta format and one line per sequence (i.e. miRNAs)

import gzip

if (len(sys.argv) != 3):
    print("Usage: {} <fasta_input> <fasta_output>".format(sys.argv[0]))
    sys.exit(1)

in_file  = sys.argv[1]
out_file = sys.argv[2]
prefix   = ">seq_"

seqs = {}
print("Reading sequences from {}".format(in_file))
if (in_file.endswith(".gz")):
    fi = gzip.open(in_file, 'rt')
else:
    fi = open(in_file, 'r')

for line in fi:
    if (line[0] == '>'):
        continue
    seq = line.strip()
    if (seq in seqs):
        seqs[seq] += 1
    else:
        seqs[seq] = 1

fi.close()

print("writing output to {}".format(out_file))
if (out_file.endswith(".gz")):
    fo = gzip.open(out_file, 'wt')
else:
    fo = open(out_file, 'w')

nseq = 0
for seq in seqs:
    nseq += 1
    cnt = seqs[seq]
    fo.write(prefix + str(nseq) + ' count=' + str(cnt) + '\n')
    fo.write(seq + '\n')

fo.close()