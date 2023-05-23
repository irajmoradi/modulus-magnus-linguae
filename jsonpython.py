import json
with open('jsonstuff.json', 'r') as f:
    data = json.load(f)
#print(data)
questions = []
answer  = []
for x in range(len(data['questions'])):
    
    questions.append(data['questions'][x]["text"])

    answer.append(data['questions'][x]["answer"])

for x in range(len(questions)):
    print(questions[x], answer[x])

promptss = ["answer this latin", "latin am i right?"]

for x in range(len(questions)):
    for prompts in promptss:
        print(prompts + " " + questions[x] + " " +  answer[x])
