import re, json, os, codecs

file_path = 'quizzes.json'

with open(file_path, 'r') as file:
    js_function = file.read()

# Extracting each json for each chapter
pattern = r'JSON\.parse\((["\'])(.*?)\1\)}'

matches = re.findall(pattern, js_function, re.DOTALL)

json_objects = []

# Iterates through each json for each chapter
for match in matches:
        unescaped_str = codecs.decode(match[1], 'unicode_escape')
        json_obj = json.loads(unescaped_str)
        json_objects.append(json_obj)

directory = "chapterinfo"
if not os.path.exists(directory):
    os.makedirs(directory)

# Sort the chapters
sort_ch = sorted(json_objects, key = lambda x:int(x['id']))

# Creates a json file for each chapter
for chapter in sort_ch:
    # Naming as Chapter ID + 1 because ID starts at 0 (i.e. first chapter has id 0, second chapter has id 1, etc.)
    filename = f"CH_{str(chapter['id'] + 1).zfill(2)}.json"
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w') as f:
        json.dump(chapter, f, indent = 4)

