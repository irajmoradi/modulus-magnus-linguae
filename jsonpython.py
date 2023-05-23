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

