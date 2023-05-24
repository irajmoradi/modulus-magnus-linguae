import json
with open('jsonstuff.json', 'r') as f:
    data = json.load(f)
#print(data)
questions = []
answer  = []
for x in range(len(data['questions'])):
    
    questions.append(data['questions'][x]["question"])

    answer.append(data['questions'][x]["answer"])

for x in range(len(questions)):
    print(questions[x], answer[x])

promptss = ["answer this latin", "latin am i right?"]

for x in range(len(questions)):
    for prompts in promptss:
        string = (prompts + " " + questions[x] + " " + "[ANSWER] ") 
        newstring = 'argmax"' + string + '" from "openai/text-ada-001"'
        #create json file for code
        finalname = str(x) + prompts + ".lmql"
        f = open(finalname, "w")
        f.write(newstring)
