#!/bin/bash
directories_set1=(
  "./task2/jsonoutputs/pensvmA"  # Directory 1 of set 1
  "./task2/jsonoutputs/pensvmB"    # Directory 2 of set 1
  "./task2/jsonoutputs/pensvmC"    # Directory 3 of set 1
)

directories_set2=(
  "./prompts/pensvnA"    # Directory 1 of set 2
  "./prompts/pensvnB"    # Directory 2 of set 2
  "./prompts/pensvnC"    # Directory 3 of set 2
)
outputset=("quizTypeA" "quizTypeB" "quizTypeC")
for((i=0; i<3; i++)); do
    question="${directories_set1[$i]}"
    echo "${question}"
    prompt="${directories_set2[$i]}"
    output="${outputset[$i]}"
    for file1 in "${question}"/*; do
        echo "${question}"
        echo "${prompt}"
        echo "${file1}"
        for file2 in "${prompt}"/*; do
            echo "proccessing ${file1} and ${file2}"
            python3 ./src/jsonpython.py --question_input_path="$file1" --prompt_input_path="$file2" --output_folder="$output" &
        done
    done
done
