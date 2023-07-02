import json
import os
import argparse
from evaluate import load
import copy
parser = argparse.ArgumentParser()
parser.add_argument('--file_name', default = 'task2update/quizstyle/PENSVMA/CAPITVLVM XXV.json')
parser.add_argument("--output_folder", default = "results")
parser.add_argument("--model", default = "/data/imoradi/hugging13B")


args = parser.parse_args()
file_path = args.file_name
output_folder = args.output_folder
model = args.model
with open(file_path, 'r') as file:
    data = json.load(file)




questions = []
answers = []
evalsentenceslist = []
evalsentences = []
correct = 0

for x in range(len(data)):
    questions.append(data[x]["question"])
    answers.append(data[x]["answer"])
    evalsentenceslist.append(data[x]["evalsentences"])
    for z in range(4):
        evalsentences.append(evalsentenceslist[x][z])
 





perplexity = load("perplexity", module_type="metric")
results = perplexity.compute(predictions=evalsentences, model_id=model, device="cpu")

perplexities = results["perplexities"]

intperplexities = copy.deepcopy(perplexities)
intevalsentences = copy.deepcopy(evalsentences)
retlist = []
intlist = []
outerdictionary = {}
innerdictionary = {}
for x in range(len(questions)):
    for z in range(4):
        innerdictionary["evalsentence"] = intevalsentences[z]
        innerdictionary["perplexity"] = intperplexities[z]
        intlist.append(innerdictionary)
        innerdictionary = {}
    del intevalsentences[:4]
    del intperplexities[:4]
    outerdictionary["question"] = questions[x]
    outerdictionary["answer"] = answers[x]
    outerdictionary["evalsentences"] = intlist
    retlist.append(outerdictionary)
    outerdictionary = {}
    intlist = []
    

evallist = []
for x in range(len(questions)):
    evallist = perplexities[:4]
    print("evallist=", evallist)
    print("evalsentences[:4]=", evalsentences[:4])
    del perplexities[:4]
    min_index = evallist.index(min(evallist))
    if evalsentences[min_index] == answers[x]:
        correct += 1
    del evalsentences[:4]



file_name = os.path.basename(args.file_name)
dir_path = os.path.dirname(args.file_name)

# Extract the last folder name from the directory path
folder1 = os.path.basename(dir_path)
# Now you can use both the file name and folder1 in your output file name
output_file_name = os.path.join(output_folder, file_name[:-5] + "." + folder1 + "." + model.split("/")[-1] +  ".json")
accuracy = correct/len(questions)
print("accuracy =", accuracy )

# Ensure the output_folder exists
os.makedirs(output_folder, exist_ok=True)
with open(output_file_name, "w") as outfile:
    json.dump(accuracy, outfile)

output_file_name1 = os.path.join(output_folder, file_name[:-5] + "." + folder1 + "." + model.split("/")[-1] + ".raw" + ".json")

with open(output_file_name1, "w") as outfile:
    json.dump(retlist, outfile)
