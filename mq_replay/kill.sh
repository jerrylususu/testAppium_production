#/bin/bash


# params
OUTPUT_FILE=pool_pid

echo "killing!"

while read line; do
    $PYTHON_PATH $SCRIPT_PATH $line >$BASH_REDIRECT_FOLDER/$line.out 2>$BASH_REDIRECT_FOLDER/$line.err &
    pid=$!
    echo "$pid|$line" >> $OUTPUT_FILE 

    echo "started on $line, pid is $pid"
done < $INPUT_FILE

echo "all started!"