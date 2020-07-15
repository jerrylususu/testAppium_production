#/bin/bash


# params
OUTPUT_FILE=pool_pid

BASH_REDIRECT_FOLDER=syslog
PYTHON_LOG_FOLDER=pylog

echo "start killing!"

while read line; do
    readarray -d "|" -t arr <<< $line
    kill "${arr[0]}"
    res=$!
    echo "started on $line, pid is ${arr[0]}, killed $res"
done < $OUTPUT_FILE

echo "all runner killed!"
