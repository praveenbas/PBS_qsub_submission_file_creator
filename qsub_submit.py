#!/usr/bin/env python
# -*- coding: utf-8 -*-
## gg
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--verbosity", help="Increase output verbosity",action="store_true")
parser.add_argument("--call", "-c", type=str, required=True,help="Program or command to execute a task in double quotes")
parser.add_argument("--vmem",  type=str,default="2G",help="Virtural memeory requred to run the job [ Type: %(type)s ] [default : %(default)s]")
parser.add_argument("--hrt", type=str,default="01:00:00",help="Time to run the job [ Type: %(type)s ] [default : 1:00:00]")
parser.add_argument("--parallel","-p" ,default=1,type=int,help="Number  of parallel cores required  [ Type: %(type)s ] [default : 1]")
parser.add_argument("--outerror", "-o", type=str,help="File to print the output/ error messages [ Type: %(type)s ] [default: command in call option]")
parser.add_argument("--name", "-n", type=str,help="Job name / qsub script name [ Type: %(type)s ] [default: command in call option]")
parser.add_argument("--qsub_n", type=bool,default=False,help="Create a qsub file and wont submit the job [ Type: %(type)s ]  [default : %(default)s]")
parser.add_argument("--jhold", type=str,help="Job_id/job_name to hold this job from running [ Type: %(type)s ]  [default : null] ")
parser.add_argument("--nodes", type=int,default=1,help="Number of nodes to be used  [ Type: %(type)s ] [default : %(default)s]")
parser.add_argument("--moduleLoad","-ml", type=str,help="Comma seperated list of moudles to be loaded  [ Type: %(type)s ] [default: null]")
parser.add_argument("--moduleUnLoad","-mun",type=str,help="Unload modules (comma seperated list) [ Type: %(type)s ]  [default : null]")
parser.add_argument("--qsubfile", type=str,help="Qsub file name [ Type: %(type)s ]  [default : -n option] ")
parser.add_argument("--logfile", type=str,help="Log file name [ Type: %(type)s ]  [default : -n,-o option] ")
parser.add_argument("--addpathto", type=str,help="File extension to add absoulte path to (comma sep list of extensions) [ Type: %(type)s ]  [default : null]")

args=parser.parse_args()

# -wl	OPTIONAL	Check qsub waiting list, submit job only if que is free [default : False]	Use [T,1,y]
# -t	OPTIONAL	Specify the upper limit for task array job		[default : null]	Example :: ~/script/array_task_example/cat.sh

#print(args.qsub_n)

#if not args.name:
#    name=args.call.split(" ")[0]

### if arg.name exist assign to name else take it from the calls.
name=args.name if args.name else args.call.split(" ")[0].replace(".","") + ".sh"
jobname = name
logerror=args.outerror if args.outerror else jobname+"-o"
Qsubfile=args.qsubfile if args.qsubfile else jobname
vmem=args.vmem
lhrt=args.hrt
parallel=args.parallel
call=args.call


shfile=open(Qsubfile,'w')
shfile.write("#!/bin/sh\n")
shfile.write("#  Reserve 8 CPUs for this job\n")

#if parallel > 1:
shfile.write("#PBS -l nodes=%d:ppn=%d:cfc\n" % (args.nodes,parallel))

shfile.write( "#PBS -q cfc\n")
shfile.write("#  Request 8G of RAM\n")
shfile.write("#PBS -l vmem=%s\n" % vmem)
shfile.write( "#  The name shown in the qstat output and in the output file(s). The  default is to use the script name\n")
shfile.write("#PBS -N %s\n" % jobname)
shfile.write("#  The path used for the standard output stream of the job\n")
shfile.write("#PBS -o %s\n" % logerror)
shfile.write("# Merge stdout and stderr. The job will create only one output file which contains both the real output and the error messages\n")
shfile.write("#PBS -j oe\n")
shfile.write("#  Use /bin/bash to execute this script\n")
shfile.write("#PBS -S /bin/bash\n")
shfile.write("#  Run job from current working directoryi : by default \n")
#print FH '#PBS -cwd'. "\n")
shfile.write( "# all environment variables in the qsub command’s environment are to be exported to the batch job \n")
shfile.write("#PBS -V \n")
shfile.write("#  Send email when the job begins, ends, aborts, or is suspended\n")
shfile.write("#PBS -m bea\n")
shfile.write( "#PBS -M praveen.baskaran@uni-tuebingen.de\n")
shfile.write("#PBS -l walltime=%s\n" % lhrt)
#print FH "#PBS -q cfc\n";

if args.jhold:
    jhold=args.jhold.replace(",",":")
    shfile.write("#PBS -W depend:afterok:%s\n" % jhold)
    
#if($task_array){
#        print FH "#PBS -t 1-$task_array\n"
#}


shfile.write("\n#Loading necessary modules .. \n")
shfile.write("module load qbic/anaconda/2.1.0 \n")

#### load and unload neccessary modules
if  args.moduleLoad:
    # this is done with Germoules perl function adatpted from Qsub-submit.pl script
    # following call writes the modules that needs to be loaded in jobname _moduleload.tx file 
    os.system("Getmoules.pl %s %s %s %s" % (args.moduleLoad,"True","load",jobname+"_moduleload.txt") )
    
    # open module load file and write to qsub file
    mload=open(jobname+"_moduleload.txt","r")
    mload_lines=mload.readlines()
    mload.close()
    
    for mloadf in mload_lines:
        shfile.write(mloadf)


if  args.moduleUnLoad:
    # same as before for modules unload
    os.system("Getmoules.pl %s %s %s %s" % (args.moduleUnLoad,"True","unload",jobname+"_moduleunload.txt") )
    munload=open(jobname+"_moduleunload.txt","r")
    munload_lines=munload.readlines()
    munload.close()

    for munloadf in munload_lines:
        shfile.write(munloadf)


def addpaths(call,extension):
    """ return call with absolute path for text matching the file extension """
    path=os.getcwd()
    arrayed=call.split(" ")
    ext_array=extension.split(",")
    for t in arrayed:
        for exe in ext_array:
            if t.endswith('.'+exe):
                call=call.replace(t, path +"/" + t)
    
    return(call)

if args.addpathto:
    call = addpaths(call=call,extension=args.addpathto)
 
 
shfile.write("echo \"******************Starting analysis :::: $(date) ********\"\n\n")   
shfile.write(call)
shfile.write("\n\necho \"******************Analysis ended:::: $(date) ********\" ")  
shfile.close()




def qsubSystemCommand(call):
    """ Check if the os.system runs successfully"""
    sys_return_code=os.system(call)
    if sys_return_code != 0:
        exit(sys_return_code)   


if args.qsub_n == False:
    qsubSystemCommand(call= "qsub " + Qsubfile )
else:
    print("Submisson file :: %s :::created, But not submitted" % Qsubfile)
