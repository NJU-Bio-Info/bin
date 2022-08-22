#!/usr/bin/perl

use 5.010;
use strict;
use warnings;
use autodie;
use utf8;

#this script can be used to combine several files;
#the format of use:
#	combine.pl [files] [dest.files]
if (! defined $ARGV[0] || $ARGV[0] eq "--help" || $ARGV[0] eq "-h"){
	die "The usage of this script:\n\t$0 [input files] [dest files]\n";
}


my $out = pop @ARGV;

open my $out_fh, '>', $out;
while (<>){
	print { $out_fh } $_;
}

close $out_fh;
