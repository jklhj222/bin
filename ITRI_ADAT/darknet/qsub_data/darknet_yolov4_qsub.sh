#!/bin/bash

JOB=$1
HERE=`pwd`
USER=`whoami`


echo "This script is for running a single darknet-yolov4 job"
echo "To run a series of darknet jobs, you have to use"
echo "darknet_v4_qsub.sh JOB-name"
echo "where script JOB describes how to run these"
echo "jobs in sequence"
echo "All input files have to be in this directory"
echo ""


QUE=1cpu
MEM=4gb
NCPUS=1

if [ -e "$JOB".darknet ]
then
 /bin/rm "$JOB".darknet
fi


echo "How manyf CPUs do you want to run your job? "
echo "1cpu, 2cpu, 4cpu [default $QUE] "
read QUE
echo "How much memory want to use?"
echo "unit in kb, mb, gb [default $MEM]"
read MEM
echo "GPU idx?"
read GPU_IDX

if [ `echo $GPU_IDX | wc | awk '{print $3}'` -lt 3 ]
then
  GPUS=1
else
  GPUS=2
fi

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

cat << END_OF_CAT > "$JOB".darknet
#!/bin/bash
#PBS -e localhost:$HERE/err
#PBS -o localhost:$HERE/out
#PBS -l nodes=1:ppn=$NCPUS:gpus=$GPUS
#PBS -l mem=$MEM
#PBS -l walltime=240:00:00

cd $HERE

echo "Your darknet job starts at  \`date\` "

/home/hugh/pkg/local/darknet_alexyab_20200825_new/darknet detector train cfg/task.data cfg/train.cfg -map  -dont_show -gpus $GPU_IDX > $JOB.out 2> $JOB.err

wait


echo "Your darknet job completed at  \`date\` "

END_OF_CAT


chmod +x "$JOB".darknet

qsub ./"$JOB".darknet


