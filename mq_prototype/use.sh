#/bin/bash


# params
PYTHON_PATH=/usr/bin/python3
SCRIPT_PATH=consumer.py
INPUT_FILE=status
OUTPUT_FILE=pid

BASH_REDIRECT_FOLDER=syslog
PYTHON_LOG_FOLDER=log2

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