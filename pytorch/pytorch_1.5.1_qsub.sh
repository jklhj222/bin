#!/bin/bash

JOB=$1
HERE=`pwd`
USER=`whoami`


echo "This script is for running a single Pytorch-1.5.1 job"
echo "To run a series of Pytorch jobs, you have to use"
echo "pytorch_1.5.1_qsub.sh JOB-name"
echo "where script JOB describes how to run these"
echo "jobs in sequence"
echo "All input files have to be in this directory"
echo ""


QUE=1cpu
MEM=4gb
NCPUS=1

if [ -e "$JOB".torch ]
then
 /bin/rm "$JOB".torch
fi


echo "How manyf CPUs do you want to run your job? "
echo "1cpu, 2cpu, 4cpu [default $QUE] "
read QUE
echo "How much memory want to use?"
echo "unit in kb, mb, gb [default $MEM]"
read MEM

if [ "$QUE" = 1cpu ]
then
  NCPUS=1
fi
if [ "$QUE" = 2cpu ]
then
  NCPUS=2
fi
if [ "$QUE" = 4cpu ]
then
  NCPUS=4
fi

cat << END_OF_CAT > "$JOB".torch
#!/bin/bash
#PBS -e localhost:$HERE/err
#PBS -o localhost:$HERE/out
#PBS -l nodes=1:ppn=$NCPUS:gpus=1
#PBS -l mem=$MEM
#PBS -l walltime=120:00:00

cd $HERE

workon pytorch1.5.1 

echo "Your Pytorch job starts at  \`date\` "

/home/hugh/.virtualenvs/pytorch1.5.1/bin/python3 train.py > $JOB.out 2> $JOB.err

wait


echo "Your Octopus job completed at  \`date\` "

END_OF_CAT


chmod +x "$JOB".torch

qsub ./"$JOB".torch


