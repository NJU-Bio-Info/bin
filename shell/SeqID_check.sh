#!/bin/bash

#@Author: Kun-ming Shui, skm@smail.nju.edu.cn

#this script is used to check whether there is sequence name duplication in fastq file
#usage:

if [ $# -eq 0 ] || [ $1 == "--help" ] || [ $1 == "-h" ]
then
	echo "Usage:"
	echo -e "\tSeqID_check.sh <fastq>"
	exit 1
fi

if [[ $1 =~ gz$ ]]
then
	zcat $1 | awk 'FNR%4==1' > SeqID_check_readsID.txt
else
	cat $1 | awk 'FNR%4==1' > SeqID_check_readsID.txt
fi

cat readsID.txt | sort | uniq -c > SeqID_check_tmp.txt

num=`cat tmp.txt | awk '$1 != 1' | wc -l`

if [ $num eq 0 ]
then
	echo "There is no sequence name duplication."
else
	echo "Some sequence name duplication were found here!"
	echo "They will be written into SeqID_dup.txt file."
	cat tmp.txt | awk '$1 != 1' > SeqID_dup.txt
fi

rm SeqID_check_readsID.txt SeqID_check_tmp.txt
