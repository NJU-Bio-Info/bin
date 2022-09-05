#!/usr/bin/python3

import argparse
import textwrap

parser = argparse.ArgumentParser(prog = "getFeature.py",
				 description = textwrap.dedent('''\
						 This is a python tool for you to extract gene features in bed file format from bed13 file.

						 About how to convert GTF annotation file into bed13 file:
						 - https://www.jianshu.com/p/de2455a8f507
						 About the structure of transcripts:
						 - https://www.jianshu.com/p/f97935ce7255
						 '''),
				 formatter_class = argparse.RawDescriptionHelpFormatter,
				 epilog = "Owner: skm@smail.nju.edu.cn, Nanjing University."
				 )

parser.add_argument('--bed13', '-b', required = True, help = "the bed13 file.")
parser.add_argument('--prefix', '-p', required = True, help = "the prefix of the file to store the result.")
parser.add_argument('--feature', '-f', required = True, choices = ['exon', 'intron', '5utr', '3utr', 'start_codon', 'stop_codon', 'cds'], help = "the feature type you want to extract.")
parser.add_argument('--keep', '-k', action = 'store_true', help = "whether to keep non-main chr, default is not.") 
parser.add_argument('--version', '-v', action = 'version', version='%(prog)s 1.0.0')

args = parser.parse_args()

#input
bed = args.bed13
prefix = args.prefix
feature = args.feature


#load bed13 file
with open(bed, 'r') as input_file:
	tx_dict = {}
	chrs_keep = ['chrM', 'chrX', 'chrY']
	for i in range(22):
		chrs_keep.append('chr' + str(i+1))
	for line in input_file.readlines():
		line = line.strip()
		fields = line.split("\t")
#		chr = fields[0]
#		start = fields[1]
#		end = fields[2]
#		name = fields[3]
#		strand = fields[5]
#		cds_start = fields[6]
#		cds_end = fields[7]
#		num = fields[9]
#		exon_size = fields[10]
#		exon_start = fields[11]

		name = fields.pop(3)
		del fields[3]
		del fields[6]
		if args.keep:
			tx_dict[name] = fields
		else:
			if fields[0] in chrs_keep:
				tx_dict[name] = fields
#		chr, start, end, strand, cds_start, cds_end, num, exon_size, exon_start
#function to extract feature
#exon
def get_exon(dict, dest):
	file = dest + '.exon.bed'
	with open(file, 'w') as exon:
		for tx,feat in dict.items():
			for i in range(int(feat[6])):
				curr_exon_start = int(feat[1]) + int(feat[8].split(",")[i])
				curr_exon_end = curr_exon_start + int(feat[7].split(",")[i])
				curr_line = [feat[0], str(curr_exon_start), str(curr_exon_end), tx + "_" + str(i+1), '0', feat[3]]
				exon.write("\t".join(curr_line) + "\n")
#intron
def get_intron(dict, dest):
	file = dest + '.intron.bed'
	with open(file, 'w') as intron:
		for tx,feat in dict.items():
			if int(feat[6]) != 1:
				for i in range(int(feat[6]) - 1):
					curr_exon_start = int(feat[1]) + int(feat[8].split(",")[i])
					curr_exon_end = curr_exon_start + int(feat[7].split(",")[i])
					next_exon_start = int(feat[1]) + int(feat[8].split(",")[i+1])
					curr_line = [feat[0], str(curr_exon_end), str(next_exon_start), tx + "_" + str(i+1), '0', feat[3]]
					intron.write("\t".join(curr_line) + "\n")


#cds
def get_cds(dict, dest):
	file = dest + '.cds.bed'
	with open (file, 'w') as cds:
		for tx,feat in dict.items():
			if feat[4] != feat[5]:
				index = 0
				for i in range(int(feat[6])):
					curr_exon_start = int(feat[1]) + int(feat[8].split(",")[i])
					curr_exon_end = curr_exon_start + int(feat[7].split(",")[i])
					bool_1 = curr_exon_start < int(feat[4]) and curr_exon_end > int(feat[4])
					bool_2 = curr_exon_start >= int(feat[4]) and curr_exon_end <= int(feat[5])
					bool_3 = curr_exon_start <= int(feat[5]) and curr_exon_end > int(feat[5])
					bool_4 = curr_exon_start <= int(feat[4]) and curr_exon_end >= int(feat[5])
					if bool_1:
						index += 1
						curr_line = [feat[0], str(feat[4]), str(curr_exon_end), tx + "_" + str(index), '0', feat[3]]
						cds.write("\t".join(curr_line) + "\n")
					elif bool_2:
						index += 1
						curr_line = [feat[0], str(curr_exon_start), str(curr_exon_end), tx + "_" + str(index), '0', feat[3]]
						cds.write("\t".join(curr_line) + "\n")
					elif bool_3:
						index += 1
						curr_line = [feat[0], str(curr_exon_start), str(feat[5]), tx + "_" + str(index), '0', feat[3]]
						cds.write("\t".join(curr_line) + "\n")
					elif bool_4:
						index += 1
						curr_line = [feat[0], str(feat[4]), str(feat[5]), tx + "_" + str(index), '0', feat[3]]
						cds.write("\t".join(curr_line) + "\n")

#start_codon
def get_start_codon(dict, dest):
	file = dest + '.startcodon.bed'
	with open(file, 'w') as startcodon:
		for tx,feat in dict.items():
			if feat[4] != feat[5]:
				if feat[3] == "+":
					curr_line = [feat[0], feat[4], str(int(feat[4]) + 3), tx, '0', feat[3]]
				else:
					curr_line = [feat[0], str(int(feat[5]) - 3), feat[5], tx, '0', feat[3]]
				startcodon.write("\t".join(curr_line) + "\n")
#stop_codon
def get_stop_codon(dict, dest):
	file = dest + '.stopcodon.bed'
	with open(file, 'w') as stopcodon:
		for tx,feat in dict.items():
			if feat[4] != feat[5]:
				if feat[3] == "+":
					curr_line = [feat[0], str(int(feat[5]) - 3), feat[5], tx, '0', feat[3]]
				else:
					curr_line = [feat[0], feat[4], str(int(feat[4]) + 3), tx, '0', feat[3]]
				stopcodon.write("\t".join(curr_line) + "\n")


#5-utr:
def get_five_utr(dict, dest):
	file = dest + '.5utr.bed'
	with open(file, 'w') as fiveutr:
		for tx,feat in dict.items():
			if feat[4] != feat[5]:
				if feat[3] == "+":
					for i in range(int(feat[6])):
						curr_exon_start = int(feat[1]) + int(feat[8].split(",")[i])
						curr_exon_end = curr_exon_start + int(feat[7].split(",")[i])
						bool_1 = curr_exon_start < int(feat[4]) and curr_exon_end <= int(feat[4])
						bool_2 = curr_exon_start < int(feat[4]) and curr_exon_end > int(feat[4])
						if bool_1:
							curr_line = [feat[0], str(curr_exon_start), str(curr_exon_end), tx + '_' + str(i+1), '0', feat[3]]
							fiveutr.write("\t".join(curr_line) + "\n")
						elif bool_2:
							curr_line = [feat[0], str(curr_exon_start), feat[4], tx + '_' + str(i+1), '0', feat[3]]
							fiveutr.write("\t".join(curr_line) + "\n")
				else:
					index = 0
					for i in range(int(feat[6])):
						curr_exon_start = int(feat[1]) + int(feat[8].split(",")[i])
						curr_exon_end = curr_exon_start + int(feat[7].split(",")[i])
						bool_1 = curr_exon_start > int(feat[5]) and curr_exon_end > int(feat[5])
						bool_2 = curr_exon_start <= int(feat[5]) and curr_exon_end > int(feat[5])
						if bool_1:
							index += 1
							curr_line = [feat[0], str(curr_exon_start), str(curr_exon_end), tx + '_' + str(index), '0', feat[3]]
							fiveutr.write("\t".join(curr_line) + "\n")
						elif bool_2:
							index += 1
							curr_line = [feat[0], feat[5], str(curr_exon_end), tx + '_' + str(index), '0', feat[3]]
							fiveutr.write("\t".join(curr_line) + "\n")
#3-utr
def get_three_utr(dict, dest):
	file = dest + '.3utr.bed'
	with open(file, 'w') as threeutr:
		for tx,feat in dict.items():
			if feat[4] != feat[5]:
				if feat[3] == "+":
					index = 0
					for i in range(int(feat[6])):
						curr_exon_start = int(feat[1]) + int(feat[8].split(",")[i])
						curr_exon_end = curr_exon_start + int(feat[7].split(",")[i])
						bool_1 = curr_exon_start > int(feat[5]) and curr_exon_end > int(feat[5])
						bool_2 = curr_exon_start <= int(feat[5]) and curr_exon_end > int(feat[5])
						if bool_1:
							index += 1
							curr_line = [feat[0], str(curr_exon_start), str(curr_exon_end), tx + '_' + str(index), '0', feat[3]]
							threeutr.write("\t".join(curr_line) + "\n")
						elif bool_2:
							index += 1
							curr_line = [feat[0], feat[5], str(curr_exon_end), tx + '_' + str(index), '0', feat[3]]
							threeutr.write("\t".join(curr_line) + "\n")
				else:
					for i in range(int(feat[6])):
						curr_exon_start = int(feat[1]) + int(feat[8].split(",")[i])
						curr_exon_end = curr_exon_start + int(feat[7].split(",")[i])
						bool_1 = curr_exon_start < int(feat[4]) and curr_exon_end <= int(feat[4])
						bool_2 = curr_exon_start < int(feat[4]) and curr_exon_end > int(feat[4])
						if bool_1:
							curr_line = [feat[0], str(curr_exon_start), str(curr_exon_end), tx + '_' + str(i+1), '0', feat[3]]
							threeutr.write("\t".join(curr_line) + "\n")
						elif bool_2:
							curr_line = [feat[0], str(curr_exon_start), feat[4], tx + '_' + str(i+1), '0', feat[3]]
							threeutr.write("\t".join(curr_line) + "\n")


if __name__ == '__main__':
	print ("Processing...")
	if feature == "exon":
		get_exon(dict = tx_dict, dest = prefix)
	elif feature == "intron":
		get_intron(dict = tx_dict, dest = prefix)
	elif feature == "cds":
		get_cds(dict = tx_dict, dest = prefix)
	elif feature == "start_codon":
		get_start_codon(dict = tx_dict, dest = prefix)
	elif feature == "stop_codon":
		get_stop_codon(dict = tx_dict, dest = prefix)
	elif feature == "5utr":
		get_five_utr(dict = tx_dict, dest = prefix)
	elif feature == "3utr":
		get_three_utr(dict = tx_dict, dest = prefix)
	print ("Finished...")
