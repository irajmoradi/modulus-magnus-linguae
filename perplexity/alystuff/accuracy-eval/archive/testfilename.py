# oldfilename: CAPITVLVM_I.mc.style1.text-davinci-003.Exercise1.0shot
    # oldfilename: CAPITVLVM_I.mc.style1.text-davinci-003.Exercise1.0shot.0exclusion.json
    # origional : CAPITVLVM_V.zeroshot_style3.0shot.5exclusion.davinci:ft-personal:ch5txt-only-2023-06-15-04-29-57.mc.json
    # better: CAPITVLVM_V.style3.0shot.5exclusion.davinci:ft-personal:ch5txt-only-2023-06-15-04-29-57.mc
    # new: CAPITVLVM_V.mc.style3.model.PENSVMA.0shot.5exclusion
 #         CAPITVLVM_V.mc.style3.davinci-finetuned-ch5txt-only.PENSVMA.0shot.5exclusion

inputName = "pokemon/PENSVMA/CAPITVLVM_V.style_3.3shot.5exclusion.davinci:ft-personal:ch5txt-replacements-2023-06-15-01-18-46.mc.json"

info_list = inputName.split(".")

if info_list[4] == "davinci:ft-personal:ch5txt-only-2023-06-15-04-29-57":
    model = "davinci-finetuned-ch5txt-only"
elif info_list[4] == "davinci:ft-personal:ch5txt-replacements-2023-06-15-01-18-46":
    model = "davinci-finetuned-ch5txt-replacements"
json_name = ".".join([info_list[0].split("/")[2], info_list[5], info_list[1], model, info_list[0].split("/")[1], info_list[2], info_list[3]])

print(json_name)