#/bin/bash


# params
PYTHON_PATH=/home/luzhirui/miniconda3/bin/python3.7
SCRIPT_PATH=docker_replay_mq_pool_runner.py
INPUT_FILE=pool_status
OUTPUT_FILE=pool_pid

BASH_REDIRECT_FOLDER=syslog
PYTHON_LOG_FOLDER=pylog

mkdir $BASH_REDIRECT_FOLDER
mkdir $PYTHON_LOG_FOLDER

# empty the ouput file
> $OUTPUT_FILE

echo "start!"

while read line; do
    $PYTHON_PATH $SCRIPT_PATH $line >$BASH_REDIRECT_FOLDER/$line.out 2>$BASH_REDIRECT_FOLDER/$line.err &
    pid=$!
    echo "$pid|$line" >> $OUTPUT_FILE 

    echo "started on $line, pid is $pid"
done < $INPUT_FILE

echo "all started!"