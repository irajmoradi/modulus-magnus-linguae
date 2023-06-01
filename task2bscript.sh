
#!/bin/bash
directories_set1=(
  "PENSVM A" 
  "PENSVM B"  
  "PENSVM C"
)

directories_set2=(
  "./prompts/pensvnA"    
  "./prompts/pensvnB"   
  "./prompts/pensvnC"    
)
outputset=("quizTypeA" "quizTypeB" "quizTypeC")
for((i=0; i<3; i++)); do
    pensum="${directories_set1[$i]}"
    echo "${question}"
    prompt="${directories_set2[$i]}"
    output="${outputset[$i]}"
    for file1 in "task2/chapterinfo/"CH*; do
        echo "${question}"
        echo "${prompt}"
        echo "${file1}"
        for file2 in "${prompt}"/*; do
            echo "proccessing ${file1} and ${file2}"
            python3 ./src/jsonpython.py --question_input_path="$file1" --prompt_input_path="$file2" --output_folder="$output" --pensum="$pensum"&
        done
    done
done
