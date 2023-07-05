import lmql
import json
from pathlib import Path
import argparse
from functools import partial
import os

def query(c):
    '''takes in a dict that includes lmql prompt and the ground truth answer, 
    returns list of dictionaries that include prompt, ground truth, and model output'''
    print("sending output")
    output = lmql.run_sync(c["code"], output_writer=lmql.stream("RESPONSE"))
    print("output returned as: " + output[0].variables['ANSWER'].strip())
    # TODO: better way to do this?
    return {"code":c["code"]}, {"answer":c["answer"]}, {"model_output":output[0].variables['ANSWER'].strip()}

def get_outputs(codes):
    '''passes lmql code to query, returns a list of dictionaries of all of the model's results'''
    results = []
    for c in codes:
        results.append(query(c))
    return results


# getting json name
parser = argparse.ArgumentParser()
parser.add_argument('second_argument')

# opening json file
file_path = Path.cwd()/parser.parse_args().second_argument
with file_path.open(mode='r',encoding="utf-8") as f:
        data = json.load(f)


# creating output base filename
info_list = parser.parse_args().second_argument.split(".")
print(info_list)
json_name = ".".join([info_list[0].split("/")[2], "fr", info_list[1], info_list[2], info_list[0].split("/")[1]])

# creating output filepaths
output_response_file = "results-free-resp/" +  json_name + ".raw.json"

if not os.path.exists(output_response_file) or os.path.getsize(file_path) == 0: 
    # getting model output
    model_output = get_outputs(data["codes"]) 

    # exporting model output
    with open(output_response_file, "w") as outfile:
        outfile.write(json.dumps(model_output))
