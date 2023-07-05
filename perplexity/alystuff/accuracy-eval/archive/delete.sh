#!/bin/bash

# Specify the directory path
directory="results-capV"

# Loop through each file in the directory
for file in "$directory"/*; do
  # Check if the file is empty
  if [ -s "$file" ]; then
    echo "File $file is not empty."
  else
    echo "Deleting empty file: $file"
    rm "$file"
  fi
done