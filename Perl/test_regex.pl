#!/usr/bin/perl

use v5.24;
use warnings;
use strict;
use utf8;

#This Perl tool can be use to test regular expression.
#Iuput: regex.
#Input: keyboard target string.
#Example: test_regex.pl regex

while (<STDIN>){
	chomp;
	if (/$ARGV[0]/p){
		print "Matched:\n\t|${^PREMATCH}<${^MATCH}>${^POSTMATCH}|\n";
	}else{
		print "Unable to match:\n\t|$_|\n";
	}
}
