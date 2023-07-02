#!/usr/bin/python
import os, json

chapters = os.listdir('chapterinfo')

for chap in chapters:
    content = os.path.join('chapterinfo', chap)
    with open(content, 'r') as f:
        content = json.load(f)

        for exercise in content['exercises']:
            questions = exercise['questions']
            quiztype = os.path.join('quizstyle', exercise['name'].replace(" ", ""))

            if not os.path.exists(quiztype):
                os.makedirs(quiztype)

            quizpath = os.path.join(quiztype, content['name'] + '.json')
            with open(quizpath, 'w') as quizzes:
                json.dump(questions, quizzes, indent=4)
