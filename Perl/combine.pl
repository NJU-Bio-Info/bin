#!/usr/bin/perl

use 5.010;
use strict;
use warnings;
use diagnostics;
use autodie;
use utf8;

#this script can be used to combine several files;
#the format of use:
#	combine.pl [files] [dest.files]

my $out = pop @ARGV;

open my $out_fh, '>>', $out;
while (<>){
	print { $out_fh } $_;
}

close $out_fh;
