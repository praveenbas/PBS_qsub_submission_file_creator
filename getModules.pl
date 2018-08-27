#!/usr/bin/perl -w
use strict;

#if($unloadmod)
#{

#foreach my $unLoadModules (loadModules($ARGV[0],"unload",$ARGV[1])){
#	print FH "module unload $unLoadModules\n";
#}
#}

#if($modulelist)
#{

open FH, ">$ARGV[3]" or die "cannot open file $ARGV[3]:$!";        
foreach my $toLoadModules (loadModules($ARGV[0], "load",$ARGV[1])){
	 print FH "module $ARGV[2] $toLoadModules\n";

}

close(FH);
#}







#### function to load necessary modules.
#### returns list of arrays to be loaded.
sub loadModules {
        my @loadlist= split(",",$_[0]);
        my $load_unload=$_[1];
        my $verprint=$_[2];
        my @cmd=`module -p avail 2>&1 | grep -v \"ERROR\"`;
        shift(@cmd);
        my %modules;
        foreach (@cmd)
        {

                my $soft=(split("/",$_))[1];
                if(!exists $modules{$soft})
                {

                        $modules{$soft}=$_;
                }


        }

        my @soft_mod=keys %modules;

        #print "######Avialable modules ##### \n@soft_mod\n########\n";

        my %modules_new;


        foreach my $softwares (@loadlist)
        {

                my @grepped=grep {/$softwares/ } @cmd;
                my $grepped_len=@grepped;
                if($verprint eq "TRUE"){
                        print "######Avialable modules ##### \n@soft_mod\n########\n";
                        print "$grepped[0]\n";
                        print "$softwares => $grepped_len\n";
                }
                if($grepped_len == 1)
                {
                        $grepped[0]=~s/[\(,\)]//g;
                        $modules_new{$softwares} =$grepped[0];
                        #system("module load $grepped[0]");
                }else{

                        system("module -p avail 2>&1 | grep \"$softwares\"");
                        print "Muliple version of module ::$softwares ::exists :::\n Please choose one :: ";
                        my $input=<STDIN>;
                        chomp($input);
                        $input=~s/[\(,\)]//g;
                        $modules_new{$softwares}=$input;
                        print "Using :: $input :::  to $load_unload the module $softwares\n";
                        #system("module load $input");
                }

        }
        my @return_mod= values %modules_new;
        return(@return_mod);

}


