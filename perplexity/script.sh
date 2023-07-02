#!/bin/bash

# Set the output folder
OUTPUT_FOLDER="results"

# Iterate over all .json files in perplexing/{manyfolders}
for FILE in $(find perplexing -name "*.json"); do
    echo "Processing file: $FILE"
    python3 evalperplex.py --file_name $FILE --output_folder $OUTPUT_FOLDER --model "/data/imoradi/finetuned_models/13Bjuly2nd1"
done

