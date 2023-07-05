import os
import asyncio
import lmql
import json
from pathlib import Path
import argparse
import aiometer
from functools import partial

async def query(c):
    '''takes in a dict that includes lmql prompt and the true answer,
    returns 1 if the model is correctand 0 if wrong'''
    print("sending output")
    output = (await lmql.run(c["code"], output_writer=lmql.stream("RESPONSE")))
    print(output)
    return {"code":c["code"]}, {"answer":c["answer"]}, {"model_output":output[0].variables['ANSWER'].strip()}

async def run(codes):
    results = await aiometer.run_all([partial(query,c) for c in codes], max_per_second=.2, max_at_once=5)
    return results

def get_outputs(codes):
    '''calculates accuracy based on outputs from query

    TODO: update these 
    >>> calc_accuracy([{'code': ('argmax "Q: Fill in the missing words: Italia ~ Europa est; Graecia ~ in Europa est. '
    ...                 'Answer Choices: (A) in quoque (B) ne non (C) ubi (D) non sed '
    ...                 'A: [ANSWER]" from "openai/text-davinci-003" where ANSWER in ["A", "B","C", "D"]'),'answer': 'A'}, {'code': ('argmax' 
    ...                 '"Q: Fill in the missing words: ~ est Arabia? In Asia est Arabia. '
    ...                 'Answer Choices: (A) in quoque (B) ne non (C) ubi (D) non sed '
    ...                 'A: [ANSWER]" from "openai/text-davinci-003" where ANSWER in ["A", "B","C", "D"]'),'answer':'C'}])
    0.5
    >>> calc_accuracy([{'code': ('argmax "Q: Fill in the tilde: Italia in Europa ~. '
    ...                 'Answer Choices: (A) est (B) sunt '
    ...                 'A: [ANSWER]" from "openai/text-davinci-003" where ANSWER in ["A", "B"]'),'answer': 'A'}, {'code': ('argmax'
    ...                 '"Q: Fill in the tilde: Italia et Gallia in Europa ~. '
    ...                 'Answer Choices: (A) est (B) sunt '
    ...                 'A: [ANSWER]" from "openai/text-davinci-003" where ANSWER in ["A", "B"]'),'answer':'B'}])
    1.0
    '''
    # using query to prompt model with questions in parallel 
    loop = asyncio.get_event_loop()
    outputs = loop.run_until_complete(run(codes))

    return outputs

def calculate_accuracy(model_output):
    '''takes in list that contains the model output, questions, and answers, returns accuracy score'''
    scores = []
    for question in model_output:
        if question[1]["answer"] == question[2]["model_output"]:
            scores.append(1)
        else:
            scores.append(0)
    
    return sum(scores) / len(scores)

def main():
    # opening json file
    parser = argparse.ArgumentParser()
    parser.add_argument('second_argument')
    file_path = Path.cwd()/parser.parse_args().second_argument
    with file_path.open(mode='r',encoding="utf-8") as f:
         data = json.load(f)

    
    # creating output filenames
    info_list = parser.parse_args().second_argument.split(".")
    model = "davinci"
    if info_list[4] == "davinci:ft-personal:ch5txt-only-2023-06-15-04-29-57":
        model = "davinci-finetuned-ch5txt-only"
    elif info_list[4] == "davinci:ft-personal:ch5txt-replacements-2023-06-15-01-18-46":
        model = "davinci-finetuned-ch5txt-replacements"
    elif info_list[4] == "davinci:ft-personal:ch5txt-prompt-replacements-2023-06-17-19-29-25":
        model = "davinci-finetuned-ch5txt-qareplacements"
    json_name = ".".join([info_list[0].split("/")[2], info_list[5], info_list[1], model, info_list[0].split("/")[1], info_list[2], info_list[3]])

    output_accuracy_file = "x/" + json_name + ".json"
    output_response_file = "x/" +  json_name + ".raw.json"

    #if not os.path.exists(output_accuracy_file) or os.path.getsize(file_path) == 0:
    #model_output = get_outputs(data["codes"]) TODO: FIX
    #print(model_output)
    model_output = [({'code': 'argmax \'ANSWER KEY:[āte, am ant ī ōs at īte, it am iunt, iunt ō īs īs, ē ās ēte, īs, ā ā it, ent, ēte ite ās ite, ās unt unt ō am unt ō ās ā unt] Q: lius et Aemilia in vīll~ habit~ cum liber~ et serv~. A: ā ant īs īs Q: minus mult~ serv~ et mult~ ancill~ habet. A: ōs ōs ās ās Q: milia in peristȳl~ est cum Mārc~ et Quīnt~ et Iūli~. A: ō ō ō ā Q: Aemilia: "Mārce et Quīnte! Voc~ Iūliam!" A: [ANSWER]\' from \'openai/davinci\' where ANSWER in [\'ā\', \'ōs\', \'ō\', \'ās\', \'am\', \'āte\', \'am\', \'it\', \'iunt\', \'ē\', \'īs\', \'ā\', \'ent\', \'ēte\', \'ās\']'}, {'answer': 'āte'}, {'model_output': 'īs'}), ({'code': 'argmax \'ANSWER KEY:[āte, am ant ī ōs at īte, it am iunt, iunt ō īs īs, ē ās ēte, īs, ā ā it, ent, ēte ite ās ite, ās unt unt ō am unt ō ās ā unt] Q: lius et Aemilia in vīll~ habit~ cum liber~ et serv~. A: ā ant īs īs Q: minus mult~ serv~ et mult~ ancill~ habet. A: ōs ōs ās ās Q: milia in peristȳl~ est cum Mārc~ et Quīnt~ et Iūli~. A: ō ō ō ā Q: Puerī Iūli~ voc~ : "Iūlia! Ven~!" et Iūlia puer~ voc~ : "Mārce et Quīnte! Ven~ " A: [ANSWER]\' from \'openai/davinci\' where ANSWER in [\'ā\', \'ōs\', \'ō\', \'ās\', \'am\', \'āte\', \'am\', \'it\', \'iunt\', \'ē\', \'īs\', \'ā\', \'ent\', \'ēte\', \'ās\']'}, {'answer': 'am ant ī ōs at īte'}, {'model_output': 'īs'})]
    with open(output_accuracy_file, "w") as outfile:
       outfile.write(str(calculate_accuracy(model_output)))
    with open(output_response_file, "w") as outfile:
        outfile.write(json.dumps(model_output))

if __name__ == "__main__":
    main()
