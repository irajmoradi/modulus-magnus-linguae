import json
import os
import random
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--file_name', default = 'task2update/quizstyle/PENSVMA/CAPITVLVM XXV.json')
parser.add_argument("--output_folder", default = "cats")

args = parser.parse_args()
file_path = args.file_name

with open(file_path, 'r') as file:
    data = json.load(file)

questions = []
answers = []
newquestions = []
newanswers = []
for x in range(len(data)):
    queststr = data[x]["q"]
    queststr = queststr.lstrip('0123456789')
    queststr = queststr.replace("#", "~")
    questions.append(queststr)
    answers.append(data[x]["a"])


def lcg(seed, evalendings, answer):
    retlist = []
    a = 7
    c = 1
    evalendings = list(evalendings)
    m = len(evalendings)
    counter = 0
    while len(retlist) != 3:
        counter += 1
        newseed = (a * seed + c) % m
        print("newseed=", newseed)
        if evalendings[newseed] in retlist:
            pass
        else:
            if evalendings[newseed] != answer:
                retlist.append(evalendings[newseed])
        seed = newseed
        if counter > 100:
            a = a + 1
    return retlist, seed

for z in range(len(questions)):
    if questions[z].count("~") == 1:
        newquestions.append(questions[z])
        newanswers.append(answers[z][0])
    else:
        hat = range(len(answers[z]))
        for x in hat: 
            if questions[z].count("~") == 1:
                newanswers.append(answers[z][0])
                newquestions.append(questions[z]) 
            else:
                firstindex = questions[z].find("~")
                questint = questions[z][:firstindex] + "#" + questions[z][firstindex + 1:]
                if questint.count("~") > 0:
                    for count in range(questint.count("~")):
                        count = count + 1
   #                     print("count)=", (count))
    #                    print("answers[z]=", answers[z])
     #                   print("questint=", questint)
                        questint = questint[:questint.find("~")] + answers[z][count] + questint[questint.find("~") + 1:]
      #                  print("questint=", questint)
                    newquestions.append(questint.replace("#", "~"))
                    newanswers.append(answers[z][0])
                    questint = questions[z][:firstindex] + answers[z][0] + questions[z][firstindex + 1:]
                    questions[z] = questint
                    del answers[z][0]
                else:
                    newquestions.append(questint.replace("#", "~"))
                    newanswers.append(answers[z][x])
                    questint = questions[z][:firstindex] + answers[z][x] + questions[z][firstindex + 1:]

#print("newquestions=", newquestions)
#print("newanswers=", newanswers)




evalendings = set(newanswers)
print("len(evalendings)=", len(evalendings))
print("evalendings=", evalendings)
evalsentenceslist = []
answersentencelist = []
evalsentences = []
seed = 2
for x in range(len(newquestions)):
    evalsentences = []
    question = newquestions[x]
    answer = newanswers[x]
    answersentence = question.replace("~", answer)
    answersentencelist.append(answersentence)
    evalsentences.append(answersentence)
    #add rng for eval endings here
    rngevalendings, seed = lcg(seed, evalendings, answer) 
    print("rngevalendings=", rngevalendings)
    print("question=", question)
    for ending in rngevalendings:
        print("ending=", ending)
        if ending != answer:
            evalsentences.append(question.replace("~", ending))
    evalsentenceslist.append(evalsentences)
#    print("evalsentences=", evalsentences)


#print("evalsentences=", evalsentences)
#print("evalsentenceslist=", evalsentenceslist)
#print("answersentencelist=", answersentencelist)

retlist = []
for x in range(len(newquestions)):
    innerdict = {}
    innerdict["question"] = newquestions[x]
    innerdict["evalsentences"] = evalsentenceslist[x]
    innerdict["answer"] = answersentencelist[x]
    retlist.append(innerdict)
print("innerdict=", innerdict)


output_path_base = os.path.join(args.output_folder, os.path.basename(args.file_name))
output_path = output_path_base.replace(" ", "_")[:-5] +  ".json"

with open(output_path, "w") as outfile:
    json.dump(retlist, outfile)
