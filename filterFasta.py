#!/usr/bin/env python3

# script to filter a fasta file, removeing any sequence inside a blast search
import sys

if (len(sys.argv) != 4):
    print("Usage: {} <blast_file> <fasta_file> <output_file>".format(sys.argv[0]))
    sys.exit(1)

blast_file = sys.argv[1]
fasta_file = sys.argv[2]
out_file   = sys.argv[3]

print("reading blast file: {}".format(blast_file))
match_ids = {}
with open (blast_file, "rt") as fh:
    for line in fh:
        elem = line.rstrip().split("\t")
        match_ids[ elem[0] ] = 1 # query_id is the first element, hit_id is the second

print("filtering fasta file: {}".format(fasta_file))
out = open(out_file, "wt")
with open (fasta_file, "rt") as fh:
    print_line = False
    for line in fh:
        if line.startswith(">"):
            seq_id = line.rstrip().replace(">", "")
            if seq_id in match_ids: # check if the sequence is in the blast search
                print_line = False
            else:
                print_line = True

        if print_line:
            out.write(line)

out.close()
print("done")