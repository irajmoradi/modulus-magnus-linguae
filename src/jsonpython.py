#!/usr/bin/python

import json
import os
import argparse
#nested for loops

parser = argparse.ArgumentParser()
parser.add_argument('--question_input_path',required=True)
parser.add_argument('--prompt_input_path',required=True)
parser.add_argument('--output_folder', default = 'lmql_code_outputs')
parser.add_argument('--model', default = 'openai/text-ada-001')
args = parser.parse_args()
question_input_path = args.question_input_path
prompt_input_path = args.prompt_input_path
output_folder = args.output_folder
model = str(args.model)
print("model=", model)




with open(question_input_path, 'r') as f:
    jsondata = json.load(f)

with open(prompt_input_path, 'r') as f:
    prompt = f.read()

print("prompt=", prompt)
print("jsondata=", jsondata)
#Give this using argparse
#promptfilepath = 
#questionfilepath =
#outputfolder = 
#model = 
#have model be string
#load prompt and json info from the filenames and store them in the following variables
#jsondata = 
#prompt = 




def getquestions(jsondata):
    """
    Returns a list of questions and a list of answers from json data in the format of {"questions":[{"answer": "something", "question": "hi?"}, ... ]})
    >>> getquestions({"questions":[{"answer": "red", "question": "Firetruck?"}, {"answer": "blue", "question": "ocean"} ]})
    (['Firetruck?', 'ocean'], ['red', 'blue'])
    """
    questions = []
    answers = []
    for x in range(len(jsondata["questions"])):
        questions.append(jsondata['questions'][x]["question"])
        answers.append(jsondata['questions'][x]["answer"])
    return questions, answers
    #promptss = ["answer this lat:in", "latin am i right?"]

def constructprompts(questions, prompt):
    """
    Returns list of strings each question with the given prompt strategy
    >>> constructprompts(["firetruck?", "Ocean?"], "What color?")
    ['What color? firetruck?', 'What color? Ocean?']
    """
    retlist = []
    for question in questions:
        retstring = prompt + " " + question
        new_string = ''.join(retstring.split('\n'))
        retlist.append(new_string)
    return retlist

def constructcodes(questprompts, model):
    """
    returns list of strings of lmql code asking the questtions + prompts to a given model
    
    Parameters:
    questprompts (list of strs): What is being asked of LLM
    model (str): the model being used in lmql

    Returns:
    list of strs: list of code to be passed into lmql
    >>> constructcodes(['What color? firetruck?', 'What color? Ocean?'], "openai/text-ada-001")
    ['argmax "What color? firetruck? [ANSWER]" from "openai/text-ada-001"', 'argmax "What color? Ocean? [ANSWER]" from "openai/text-ada-001"']
    """
    codes = []
    for questprompt in questprompts:
        code = "argmax '" + questprompt + " [ANSWER]' from '" + model + "'" 
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


try:
    os.makedirs(args.output_folder)
except FileExistsError:
    pass

questions, answers = getquestions(jsondata)
questprompts = constructprompts(questions, prompt)
print("questprompts=", questprompts)
codes = constructcodes(questprompts, model)
print("codes=", codes)
dictionary = constructdictionary(codes, answers)
print("dictionary=", dictionary)
output_path_base = os.path.join(args.output_folder,os.path.basename(args.question_input_path))
output_path = output_path_base +  str(args.prompt_input_path).split('/')[-2] + os.path.basename(args.prompt_input_path)[:-3] + "json"
with open(output_path, "w") as outfile:
    json.dump(dictionary, outfile)
    
