import json

def convert_to_jsonl(input_file, output_file):
    with open(input_file, 'r') as file:
        sentences = file.readlines()

    with open(output_file, 'w') as file:
        for sentence in sentences:
            stripped_sentence = sentence.strip()
            if stripped_sentence:  # Skip empty lines
                json_line = {
                    "instruction": "",
                    "input": "",
                    "output": stripped_sentence
                }
                json.dump(json_line, file)
                file.write('\n')

# Provide the input and output file paths
input_file_path = "ch1to5.txt"
output_file_path = "output.jsonl"

# Call the conversion function
convert_to_jsonl(input_file_path, output_file_path)

