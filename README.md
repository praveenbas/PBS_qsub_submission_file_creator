# PBS_qsub_submission_file_creator

The command-line interface
===========================

.. code-block:: bash
usage: qsub_submit.py 
                      [-h] [--verbosity] [--call CALL] [--vmem VMEM] [--hrt HRT]

                      [--parallel PARALLEL] [--outerror OUTERROR]
                      
                      [--name NAME] [--qsub_n QSUB_N] [--jhold JHOLD]
                      
                      [--nodes NODES] [--moduleLoad MODULELOAD]
                      
                      [--moduleUnLoad MODULEUNLOAD] [--qsubfile QSUBFILE]
                      
                      [--logfile LOGFILE] [--addpathto ADDPATHTO]
                      
 
  optional arguments:

    -h, --help            show this help message and exit
  
    --verbosity           Increase output verbosity
  
   --call CALL, -c CALL  Program or command to execute a task in double quotes
  
    --vmem VMEM           Virtural memeory requred to run the job [ Type: str ]
                        [default : 2G]
                        
   --hrt HRT             Time to run the job [ Type: str ] [default : 1:00:00]
  
  --parallel PARALLEL, -p PARALLEL
                        Number of parallel cores required [ Type: int ]
                        [default : 1]
                        
  --outerror OUTERROR, -o OUTERROR
                        File to print the output/ error messages [ Type: str ]
                        [default: command in call option]
                        
    --name NAME, -n NAME  Job name / qsub script name [ Type: str ] [default:
                        command in call option]
    --qsub_n QSUB_N       Create a qsub file and wont submit the job [ Type:
                        bool ] [default : False]
                        
    --jhold JHOLD         Job_id/job_name to hold this job from running [ Type:
                        str ] [default : null]
                        
    --nodes NODES         Number of nodes to be used [ Type: int ] [default : 1]
  
    --moduleLoad MODULELOAD, -ml MODULELOAD
                        Comma seperated list of moudles to be loaded [ Type:
                        str ] [default: null]
                        
    --moduleUnLoad MODULEUNLOAD, -mun MODULEUNLOAD
                        Unload modules (comma seperated list) [ Type: str ]
                        [default : null]
                        
    --qsubfile QSUBFILE   Qsub file name [ Type: str ] [default : -n option]
  
    --logfile LOGFILE     Log file name [ Type: str ] [default : -n,-o option]
    --addpathto ADDPATHTO File extension to add absoulte path to (comma sep list
                          of extensions) [ Type: str ] [default : null]                      
