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


#def findquestions(pensum, jsondata):
#    for keyval in jsondata['exercises']:
#        if pensum  == keyval["name"]:
#            return keyval["questions"]
            
            

def getquestions(questionslist):
    """
    Returns a list of questions and a list of answers from json data in the format of {"questions":[{"answer": "something", "question": "hi?"}, ... ]})
    Parameters:
    jsondata (dictionary)

    Returns:
    Questions, answers (lists)
    >>> getquestions([{"a": "red", "q": "Firetruck?"}, {"a": "blue", "q": "ocean"} ])
    (['Firetruck?', 'ocean'], ['red', 'blue'])
    >>> getquestions([{"a": ["red", "green"], "q": "Firetruck?"}, {"a": "blue", "q": "ocean"} ])
    (['Firetruck?', 'ocean'], ['red', 'blue'])
    """
    questions = []
    answers = []
    lmqlfixanswers = []
    for x in range(len(questionslist)):
        queststr = questionslist[x]["q"]
        queststr = queststr.lstrip('0123456789. ')

        queststr = queststr.replace("#", "~")
        questions.append(queststr)
        if type(questionslist[x]["a"]) == list:
            answers.append(' '.join(questionslist[x]["a"]))
            lmqlfixanswers.append(questionslist[x]["a"][0])
        else:
            answers.append(questionslist[x]["a"])
    return questions, answers, lmqlfixanswers
    #promptss = ["answer this lat:in", "latin am i right?"]

def shotexclusion(shot, exclusion, questions, answers):
    '''
    >>> shotexclusion(1, 2, ["a", "b", "c"], ["d", "e", "f"])
    (['a'], ['d'], ['c'], ['f'])
    '''
    examplequest = []
    exampleanswer = []
    if shot > 0:
        for x in range(shot):
            examplequest.append(questions[x][2:])
            exampleanswer.append(answers[x])
    if exclusion > 0:
        for x in range(exclusion):
            del questions[0]
            del answers[0]
    return examplequest, exampleanswer, questions, answers

def constructprompts(questions, prompt, examplequest, exampleanswer, multichoice, answers):
    """
    Returns list of strings each question with the given prompt strategy
    Parameters:
    questions (list): the questions being asked
    prompt (str): the template for the prompts to be sent to lmql

    Returns:
    retlist (list): list of questions + prompts for lmql
    >>> constructprompts(["Firetruck color?", "Ocean color?"], "What is the", ["Sky color?"], ["blue"])
    ['What is the Question: Sky color? Answer: blue  Question: Firetruck color?', 'What is the Question: Sky color? Answer: blue  Question: Ocean color?']
    """
    retlist = [] 
    # Add quotes around each answer individually.

    answerstring = ", ".join(f"'{answer}'" for answer in answers)
    # Surround entire string with brackets for the "where ANSWER in" clause.
    answerstring = "[" + answerstring + "]"
    examplestring = ""
    if len(examplequest) > 0:
        for x in range(len(examplequest)):
            examplestring = examplestring + "Q: " + examplequest[x] + " A: " + exampleanswer[x] + " "
    if multichoice == "Y":
        for question in questions:
            newstring = "ANSWER KEY:"  + answerstring.replace("'", "") 
            print(newstring)
            newstring = newstring + " " + examplestring
            retstring = newstring +   "Q: " + question.replace("'", "\\'")
            new_string = ''.join(retstring.split('\n'))
            print("new_string=", new_string)
            retlist.append(new_string)
    else:
        for question in questions:
            retstring = prompt.replace('<example>', examplestring) + " " + "Question: " + question.replace("'", "\\'")
            new_string = ''.join(retstring.split('\n'))
            retlist.append(new_string)
    return retlist

def constructcodes(questprompts, model, answers, multichoice, lmqlfixanswers):
    """
    returns list of strings of lmql code asking the questtions + prompts to a given model
    
    Parameters:
    questprompts (list of strs): What is being asked of LLM
    model (str): the model being used in lmql

    Returns:
    list of strs: list of code to be passed into lmql
    >>> constructcodes(['What color is the firetruck?', 'What color is the Ocean?'], "openai/text-ada-001", ['red', 'blue'], 'N')
    ["argmax 'What color is the firetruck? Answer: [ANSWER]' from 'openai/text-ada-001'", "argmax 'What color is the Ocean? Answer: [ANSWER]' from 'openai/text-ada-001'"]
    """
    codes = [] 
    # Add quotes around each answer individually.
    answerstring = ", ".join(f"'{answer}'" for answer in lmqlfixanswers)
    # Surround entire string with brackets for the "where ANSWER in" clause.
    answerstring = "[" + answerstring + "]"

    for questprompt in questprompts:
        if multichoice == "Y":
            code = "argmax '" + questprompt +" A: [ANSWER]' from '" + model + "' where ANSWER in " + answerstring  
        else:
            code = "argmax '" + questprompt +  " Answer: [ANSWER]' from '" + model  + "'"
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
  #  parser.add_argument('--prompt_input_path',required=True)
    parser.add_argument('--output_folder', default = 'lmql_code_outputs')
    parser.add_argument('--model', default = 'openai/text-ada-001')
    parser.add_argument('--multichoice', default = 'Y')
    parser.add_argument('--shot')
    parser.add_argument('--exclusion', default = 5)
    args = parser.parse_args()
    question_input_path = args.question_input_path
   # prompt_input_path = args.prompt_input_path
    shot = args.shot
    shot = int(shot)
    exclusion = int(args.exclusion)
    output_folder = args.output_folder
    model = str(args.model)
    multichoice = args.multichoice
    if multichoice == "Y":
        mc = ".mc"
    else:
        mc = ""
    with open(question_input_path, 'r') as f:
        jsondata = json.load(f)

    #with open(prompt_input_path, 'r') as f:
     #   prompt = f.read()
    prompt = ""
    try:
        os.makedirs(args.output_folder)
    except FileExistsError:
        pass
    questions, answers, lmqlfixanswers = getquestions(jsondata)
    examplequest, exampleanswer, questions, answers = shotexclusion(shot, exclusion, questions, answers)
    questprompts = constructprompts(questions, prompt, examplequest, exampleanswer, multichoice, answers)
    codes = constructcodes(questprompts, model, answers, multichoice, lmqlfixanswers)
    dictionary = constructdictionary(codes, answers)
    output_path_base = os.path.join(args.output_folder, os.path.basename(args.question_input_path).replace(" ", "_"))
    output_path = output_path_base[:-5] + '.' + "style_0" + '.' + str(shot) + "shot" + "." + str(exclusion) + "exclusion" + "."  + model.split('/')[-1] +  mc + ".json"

    with open(output_path, "w") as outfile:
        json.dump(dictionary, outfile)
    
if __name__ == "__main__":
    main() 
