#!/usr/bin/python

import json
import os
import argparse
import codecs
#nested for loops
#promptfilepath = 
#questionfilepath =
#outputfolder = 
#model = 
#have model be string
#load prompt and json info from the filenames and store them in the following variables
#jsondata = 
#prompt = 


def findquestions(pensum, jsondata):
    for keyval in jsondata['exercises']:
        if pensum  == keyval["name"]:
            return keyval["questions"]
            
            

def getquestions(questionslist):
    """
    Returns a list of questions and a list of answers from json data in the format of {"questions":[{"answer": "something", "question": "hi?"}, ... ]})
    Parameters:
    jsondata (dictionary)

    Returns:
    Questions, answers (lists)
    >>> getquestions({"questions":[{"answer": "red", "question": "Firetruck?"}, {"answer": "blue", "question": "ocean"} ]})
    (['Firetruck?', 'ocean'], ['red', 'blue'])
    """
    questions = []
    answers = []
    for x in range(len(questionslist)):
        queststr = questionslist[x]["q"].encode('utf-8')
        queststr.replace("#", "~")
        questions.append(queststr)
        answers.append(' '.join(questionslist[x]["a"]))
    return questions, answers
    #promptss = ["answer this lat:in", "latin am i right?"]

def constructprompts(questions, prompt):
    """
    Returns list of strings each question with the given prompt strategy
    Parameters:
    questions (list): the questions being asked
    prompt (str): the template for the prompts to be sent to lmql

    Returns:
    retlist (list): list of questions + prompts for lmql
    >>> constructprompts(["firetruck?", "Ocean?"], "What color?")
    ['What color? firetruck?', 'What color? Ocean?']
    """
    retlist = []
    for question in questions:
        retstring = prompt + " " + question
        new_string = ''.join(retstring.split('\n'))
        retlist.append(new_string)
    return retlist

def constructcodes(questprompts, model, answers):
    """
    returns list of strings of lmql code asking the questtions + prompts to a given model
    
    Parameters:
    questprompts (list of strs): What is being asked of LLM
    model (str): the model being used in lmql

    Returns:
    list of strs: list of code to be passed into lmql
    >>> constructcodes(['What color? firetruck?', 'What color? Ocean?'], "openai/text-ada-001")
    ["argmax 'What color? firetruck? [ANSWER]' from 'openai/text-ada-001'", "argmax 'What color? Ocean? [ANSWER]' from 'openai/text-ada-001'"]
    """
    codes = []
    answerstring = "[ '" + answers[0] + "',"
    for a in range(1, len(answers) - 1):
        answerstring = answerstring + " '" + answers[a] + "',"
    answerstring = answerstring + " '" + answers[-1] + "']"
    answerstringprint = answerstring.replace("'", "")


    for questprompt in questprompts:
        code = "argmax '" + questprompt + " Choose from this set of possible answers" + answerstringprint + " [ANSWER]' from '" + model + "' where ANSWER in " + answerstring  
        codes.append(code)
    return codes

def constructdictionary(codes, answers):
    """
    Returns dictionary where a code is paired with the answer for the question in the code

    Parameters:
    codes (list): list of code for lmql
    answers (list): list of answers
    
    Returns:
    dict: dictionary based on template in github repo

    >>> constructdictionary(["code1", "code2"], ["answer1", "answer2"])
    {'codes': [{'code': 'code1', 'answer': 'answer1'}, {'code': 'code2', 'answer': 'answer2'}]}
    """
    outerdict = {}
    outerdict["codes"] = []
    for index in range(len(codes)):
        innerdict = {}
        innerdict["code"] = codes[index]
        innerdict["answer"] = answers[index]
        outerdict["codes"].append(innerdict)
    return outerdict

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--question_input_path',required=True)
    parser.add_argument('--prompt_input_path',required=True)
    parser.add_argument('--output_folder', default = 'lmql_code_outputs')
    parser.add_argument('--model', default = 'openai/text-ada-001')
    parser.add_argument('--pensum',required=True)
    args = parser.parse_args()
    question_input_path = args.question_input_path
    prompt_input_path = args.prompt_input_path
    output_folder = args.output_folder
    model = str(args.model)
    pensum = str(args.pensum)
    with open(question_input_path, 'r') as f:
        jsondata = json.load(f)

    with open(prompt_input_path, 'r') as f:
        prompt = f.read()
    try:
        os.makedirs(args.output_folder)
    except FileExistsError:
        pass
    questionslist = findquestions(pensum, jsondata)
    questions, answers = getquestions(questionslist)
    questprompts = constructprompts(questions, prompt)
    codes = constructcodes(questprompts, model, answers)
    dictionary = constructdictionary(codes, answers)
    output_path_base = os.path.join(args.output_folder, ("capitvlvm_" + str(jsondata["id"]+1)))
    output_path = output_path_base + '.' + os.path.basename(args.prompt_input_path)[:-4]+ '.' + model.split('/')[-1] + ".json"
    with open(output_path, "w") as outfile:
        json.dump(dictionary, outfile)
    
if __name__ == "__main__":
    main() 
