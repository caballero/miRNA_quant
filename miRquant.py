#!/usr/bin/env python3

import sys

if len(sys.argv) != 4:
    print("Usage: %s <miRNA Fasta> <raw Fastq> <output table>" % sys.argv[0])
    sys.exit(1)

mir_fasta = sys.argv[1]
raw_fastq = sys.argv[2]
out_table = sys.argv[3]

mir_seqs = {}
mir_id = None
mir_cnt = 0
print ("Reading miRNA fasta file {}".format(mir_fasta))
with open(mir_fasta, 'r') as f:
    for line in f:
        line = line.rstrip()
        if line.startswith('>'):
            mir_id = line
        else:
            mir_seq = line
            if mir_seq in mir_seqs:
                mir_seqs[mir_seq] = mir_seqs[mir_seq] + ":" + mir_id
            else:
                mir_seqs[mir_seq] = mir_id
                mir_cnt += 1
print ("Read {} miRNAs".format(mir_cnt))

read_cnt = {}
read_line = 0
cnt = 0
print ("Reading raw fastq file {}".format(raw_fastq))
with open(raw_fastq, 'r') as f:
    for line in f:
        line = line.rstrip()
        read_line += 1
        if read_line == 2: # sequence line
            seq = line
            if seq in read_cnt:
                read_cnt[seq] += 1
            else:
                read_cnt[seq] = 1
                cnt += 1
        if read_line == 4: # reset line counter
            read_line = 0
print ("Read {} unique reads".format(cnt))

print ("Writing output table {}".format(out_table))
with open(out_table, 'w') as f:
    f.write("miRNA_id\tmiRNA_seq\tcount\t")
    for mir_seq in mir_seqs:
        mir_cnt = 0
        if mir_seq in read_cnt:
            mir_cnt = read_cnt[mir_seq]
            mir_id  = mir_seqs[mir_seq]
        f.write("{}\t{}\t{}\n".format(mir_id, mir_seq, mir_cnt))
