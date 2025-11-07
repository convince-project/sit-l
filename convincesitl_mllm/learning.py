#SIT-AW  Copyright (C) CEA 2025  Razane Azrou
import convincesitl_mllm.prompts.description_prompt as prompt
import convincesitl_mllm.prompts.prompt_mapping as map
from convincesitaw_mllm import send_identification_request_to_VLM
from pathlib import Path
import re
import tyro

def new_anomaly_description(messages,inference):

    messages.append({"role":"user",
                     "content":prompt.USER_PROMPT3})
    anomaly_description = inference.inference_with_api(messages)

    return anomaly_description

def update_sys_prompt_file(anomaly_description:str,use_case_id:int):
    
    #search recursively for the file path
    prompt_file = next(Path(".").rglob(f"sys_prompts_UC{use_case_id}.py")) 
    #read its content
    prompts = prompt_file.read_text(encoding="utf-8")
    # Extract and modify the string inside `SYSTEM_PROMPT = """ ... """`
    pattern = r'(SYSTEM_PROMPT\s*=\s*""")(.*?)(?=""")'
    match = re.search(pattern, prompts, re.DOTALL)
    if not match:
        raise ValueError("Couldn't find SYSTEM_PROMPT string")
    sys_prompt = match.group(2)

    #the targets of where the list lives and that are mandatory
    target_up = "Here a list of situation descriptions:"
    target_down = "Here are some examples of the correct situation:"
    # get section position
    start_point = sys_prompt.find(target_up)
    if start_point ==-1:
        raise ValueError("Here a list of situation descriptions:, was not found in system prompt")
    start_index = start_point + len(target_up)
    end_index = sys_prompt.find(target_down)
    if end_index ==-1:
        raise ValueError("Here are some examples of the correct situation:, was not found in system prompt")
    section = sys_prompt[start_index:end_index]
    #get the last class to add another one after it 
    last_defined_class = re.findall(r"^\s*\d+\.\s.*$", section, re.MULTILINE)[-1]
    if not last_defined_class:
        raise ValueError("Nothing list found in system prompt")
    last_num = int(last_defined_class[0])

    new_class = f"\n{last_num+1}. {anomaly_description}\n\n"

    new_section = section.rstrip() + new_class

    new_sys_prompt = sys_prompt[:start_index]+new_section+sys_prompt[end_index:]
    new_text = prompts[:match.start(2)] + new_sys_prompt + prompts[match.end(2):]
    #rewrite the file 
    prompt_file.write_text(new_text, encoding="utf-8")



def main(use_case_id:int,anomaly_case_path:str):

    ## need to add the fact that it is launch if unkown
    sys_prompt = map.sys_prompts[use_case_id]
    messages,inference,reply= send_identification_request_to_VLM.main(use_case_id,anomaly_case_path,sys_prompt)
    if 'unknown' or 'Unknown' in reply: #this is something to be changed in the future to avoid relying on str
        anomaly_description = new_anomaly_description(messages,inference)
        print(f'new anomaly description : {anomaly_description}')
        update_sys_prompt_file(anomaly_description,use_case_id)


def cli():
    tyro.cli(main)
