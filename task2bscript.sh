#!/bin/bash

directories_set1=(
  "PENSVMA" 
  "PENSVMB"  
  "PENSVMC"
)

directories_set2=(
  "./prompts/pensvnA"    
  "./prompts/pensvnB"   
  "./prompts/pensvnC"    
)
model_set=(
  "openai/text-ada-001"
  "openai/text-curie-001"
  "openai/text-babbage-001"
  "openai/text-davinci-001"
  "openai/text-davinci-002"
  "openai/text-davinci-003"
)
for((z=0; z<6; z++)); do
    model="${model_set[$z]}"
    outputset=("quizTypeA" "quizTypeB" "quizTypeC")
    for((i=0; i<3; i++)); do
        pensum="${directories_set1[$i]}"
        prompt="${directories_set2[$i]}"
        output="${outputset[$i]}"
        for file1 in "task2update/quizstyle/${pensum}/"*; do
            for file2 in "${prompt}"/*; do
                echo "proccessing ${file1} and ${file2} and ${model}"
                #folder2=$(basename "$folder1")
                python3 ./src/jsonpython.py --question_input_path="$file1" --prompt_input_path="$file2" --output_folder="outputs/${pensum}/" --multichoice="Y" --model="$model" 
            done
        done
       
    done 

    for folder1 in "task2update/quizstyle/"E*; do
        for folder2 in "prompts/"*; do
            for file3 in "${folder1}/"*; do 
                for file4 in "${folder2}/"*; do 
                    echo "processing ${file4} and ${file3} and ${model}"
                    base_folder=$(basename "$folder1")
                    python3 ./src/jsonpython.py --question_input_path="$file3" --prompt_input_path="$file4" --output_folder="outputs/${base_folder}/" --multichoice="Y" --model="$model"
                 done
            done
        done
    done
done


