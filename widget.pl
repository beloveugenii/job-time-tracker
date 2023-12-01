#!/usr/bin/perl

## It's a simple script, which creates Jtt widget using termux-widget.
## So…you must install it :-)
## v0.1.0
## v0.1.1 Add checking of existing .shortcuts dir
## v0.2.0 Rewritten on pure Perl

use strict;
#use utf8;
#use open qw / :std :utf8 /;
use FindBin qw / $Bin /;

my $path = "$ENV{HOME}/.shortcuts";

unless ( -d "$path" ) {
    mkdir "$ENV{HOME}/.shortcuts", 0700 and print "Dir '.shortcuts' created\n";
}

mkdir "$path/icons" unless -d _;

print "Enter widget name: ";
chomp ( my $widget_name = <STDIN> );

open ( my $fh, ">", "$path/$widget_name" );
print $fh "#!/bin/bash\nperl $Bin/jtt\n";
close $fh;

symlink "$Bin/jtt.png", "$path/icons/$widget_name.png";
