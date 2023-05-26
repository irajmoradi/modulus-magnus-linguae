import json

#nested for loops

with open('prompts.json', 'r') as f:
    data = json.load(f)
promptss = data
#print(data)
allquestions = []
questions = []
allanswers = []
answer  = []
for file_name in ["jsona.json", "jsonb.json", "jsonc.json"]:
    with open(file_name, 'r') as f:
        data = json.load(f)
    questions = []
    answer = []
    for x in range(len(data['questions'])):
        questions.append(data['questions'][x]["question"])
        answer.append(data['questions'][x]["answer"])
    allanswers.append(answer)
    allquestions.append(questions)
print(allquestions)

#promptss = ["answer this latin", "latin am i right?"]
outerdict = {}
outerdict["stuff"] = []


z = 0
index = ["Quiz A", "Quiz B", "Quiz C"]
for parts in range(3):
    letter = index[z]
    z += 1
    for x in range(len(allquestions[parts])):
        innerdict = {}
        innerdict["question"] = allquestions[parts][x]
        innerdict["answer"] = allanswers[parts][x]
        innerdict["prompt"] = []
        innerdict["code"] = []
        for prompts in promptss[letter]:
            stringg = (prompts + " " + allquestions[parts][x]) 
            string = (prompts + " " + allquestions[parts][x] + " " + "[ANSWER] ") 
            newstring = 'argmax"' + string + '" from "openai/text-ada-001"'
        #create json file for code
            innerdict["prompt"].append(stringg)
            innerdict["question"] = allquestions[parts][x]
            innerdict["code"].append(newstring)
        #finalname = str(x) + prompts + ".txt"
        #f = open(finalname, "w")
        #f.write(newstring)
        outerdict["stuff"].append(innerdict)  
with open("sample.json", "w") as outfile:
    json.dump(outerdict, outfile)
    
