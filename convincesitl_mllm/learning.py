#SIT-AW  Copyright (C) CEA 2025  Razane Azrou
import convincesitl_mllm.prompts.description_prompt as prompt
import convincesitl_mllm.prompts.prompt_mapping as map
from convincesitaw_mllm import inference_with_hosted_VLM,inference_with_local_model
from pathlib import Path
import re
import tyro

def new_anomaly_description(messages,inference,local_model:bool,model=None,processor=None):

    messages.append({"role":"user",
                     "content":prompt.USER_PROMPT3})
    if local_model:
        if not model:
            raise Exception("No local model received")
        if not processor:
            raise Exception("No model processor received")
        
        anomaly_description = inference.inference_with_local_model(model,processor,messages)

    else:
        anomaly_description = inference.inference_with_api(messages)

    return anomaly_description

def update_sys_prompt_file(anomaly_description:str,use_case_id:int):
    
    #search recursively for the file path
    prompt_file = next(Path(".").rglob(f"prompts_UC{use_case_id}.py")) 
    #read its content
    prompts = prompt_file.read_text(encoding="utf-8")
    # Extract and modify the string inside `SYSTEM_PROMPT = """ ... """`
    pattern = r'(SYSTEM_PROMPT\s*=\s*""")(.*?)(?=""")'
    match = re.search(pattern, prompts, re.DOTALL)
    if not match:
        raise ValueError("Couldn't find SYSTEM_PROMPT string")
    sys_prompt = match.group(2)

    #the targets of where the list lives and that are mandatory
    target_up = "**[ACTIONS]**"
    target_down = "**[OUTPUT FORMAT]**"
    # get section position
    start_point = sys_prompt.find(target_up)
    if start_point ==-1:
        raise ValueError("**[ACTIONS]**, was not found in system prompt")
    start_index = start_point + len(target_up)
    end_index = sys_prompt.find(target_down)
    if end_index ==-1:
        raise ValueError("**[OUTPUT FORMAT]**:, was not found in system prompt")
    section = sys_prompt[start_index:end_index]
    #get the last class to add another one after it 
    last_defined_class = re.findall(r"^\s*\d+\.\s.*$", section, re.MULTILINE)[-1]
    if not last_defined_class:
        raise ValueError("No list found in system prompt")
    last_num = int(last_defined_class[0])

    new_class = f"\n{last_num+1}. {anomaly_description}\n\n"

    new_section = section.rstrip() + new_class

    new_sys_prompt = sys_prompt[:start_index]+new_section+sys_prompt[end_index:]
    new_text = prompts[:match.start(2)] + new_sys_prompt + prompts[match.end(2):]
    #rewrite the file 
    prompt_file.write_text(new_text, encoding="utf-8")


def main(use_case_id:int,anomaly_case_path:str,local_model:bool=False):

    ## need to add the fact that it is launch if unkown
    sys_prompt = map.prompts[use_case_id].SYSTEM_PROMPT
    model = None
    processor = None
    if local_model:
        messages,inference,reply,model,processor= inference_with_local_model.main(use_case_id,anomaly_case_path,sys_prompt)
    else:
        messages,inference,reply= inference_with_hosted_VLM.main(use_case_id,anomaly_case_path,sys_prompt)

    if 'unknown' or 'Unknown' in reply: #this is something to be changed in the future to avoid relying on str
        anomaly_description = new_anomaly_description(messages,inference,local_model=local_model,model=model,processor=processor)
        print(f'new anomaly description : {anomaly_description}')
        update_sys_prompt_file(anomaly_description,use_case_id)


def cli():
    tyro.cli(main)
