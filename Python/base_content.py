#!/share/apps/anaconda3/envs/python3/bin/python3

import argparse
import numpy as np
import pandas as pd
import textwrap

parser = argparse.ArgumentParser(prog = "base_content.py",
		formatter_class = argparse.RawDescriptionHelpFormatter,
		description = textwrap.dedent('''\
				This script can calculate base content from a input fasta file.
				---------------------------------------------------------------
				The output of this mini program:
				[1] output_basenum.csv	the base number for each sequence in fasta.
				[2] output_basepro.csv	the base proportion for each sequence in fasta.
				[3] output_full_basenum.csv	the base number for the whole sequence in fasta.
				[4] output_full_basepro.csv	the base proportion for the whole sequence in fasta.
				
				The final output format is R user friendly.
				'''),
		epilog = "Author: Kun-ming Shui, skm@smail.nju.edu.cn.")

parser.add_argument('--fasta', '-f', type = str, required = True, help = "The input fasta file. (required)")
parser.add_argument('--out', '-o', type = str, required = True, help = "The prefix of output file name. (required)")

args = parser.parse_args()

fasta = args.fasta
output = args.out
#read fasta file
with open(file = fasta, mode = 'r') as file:
	dir = {}
	for line in file:
		line = line.strip()
		if line.startswith(">"):
			seq_name = line[1:]
			dir[seq_name] = ''
		else:
			dir[seq_name] += line

#calculate base content for each sequence
base_num = {}
base_pro = {}
full_seq = ''
for name,seq in dir.items():
	A_num = seq.count('A') + seq.count('a')
	T_num = seq.count('T') + seq.count('t')
	C_num = seq.count('C') + seq.count('c')
	G_num = seq.count('G') + seq.count('g')

	base_num[name] = {'A': A_num, 'T': T_num, 'C': C_num, 'G': G_num}
	base_pro[name] = {'A': np.round(A_num/len(seq),3), 'T': np.round(T_num/len(seq),3), 'C': np.round(C_num/len(seq),3), 'G': np.round(G_num/len(seq),3)}

	full_seq += seq

#base_num
file = output + '_basenum.' + 'csv'
pd.DataFrame.from_dict(base_num).T.to_csv(file)

#base_pro
file = output + '_basepro.' + 'csv'
pd.DataFrame.from_dict(base_pro).T.to_csv(file)

A_num = full_seq.count('A') + full_seq.count('a')
T_num = full_seq.count('T') + full_seq.count('t')
C_num = full_seq.count('C') + full_seq.count('c')
G_num = full_seq.count('G') + full_seq.count('g')

#full sequence
full_seq_num = {'A': A_num, 'T': T_num, 'C': C_num, 'G': G_num}
file = output + '_full_basenum.' + 'csv'
pd.DataFrame.from_dict(full_seq_num, orient = 'index').T.to_csv(file)

full_seq_pro = {'A': np.round(A_num/len(full_seq),3), 'T': np.round(T_num/len(full_seq),3), 'C': np.round(C_num/len(full_seq),3), 'G': np.round(G_num/len(full_seq),3)}
file = output + '_full_basepro.' + 'csv'
pd.DataFrame.from_dict(full_seq_pro, orient = 'index').T.to_csv(file)
