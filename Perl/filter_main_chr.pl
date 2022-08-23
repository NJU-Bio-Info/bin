#!/usr/bin/perl

use v5.10;
use warnings;
use strict;
use utf8;
use autodie;

sub usage{
print STDERR <<HELP
Usage:
	filter_main_chr.pl input_chr_file output_main_chr_file
Parameter:
	input_chr_file		the input file containing multiple chrs.
	output_main_chr_file	the output file only contain main chrs (chr1-chr22, chrM, chrX, chrY).
Version:
	v 1.0.0
Owner:
	Kun-ming Shui, skm\@smail.nju.edu.cn
HELP
}

unless (@ARGV == 2 && $ARGV[0] eq "--help" && $ARGV[0] eq "-h"){&usage; exit(-1);}

open my $chr, '<', "$ARGV[0]";
open my $main, '>', "$ARGV[1]";

while (<$chr>){
	if (m/\bchr\d{1,2}\b/ || m/\bchr[MXY]\b/){
		print $main $_;
	}
}

close $chr;
close $main;
