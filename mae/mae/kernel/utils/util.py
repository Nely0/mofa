import json
from typing import Union

from crewai_tools import tool
import yaml

from mae.utils.files.read import read_yaml


def make_crewai_tool(func):
    tool.name = func.__name__
    return tool(func)

def load_agent_config(yaml_file:str):
    params = read_yaml(yaml_file)
    if 'AGENT' in params:
        config = {}
        for key in params.keys():
            if params.get(key,None) is not None:
                config.update(params.get(key,None))
        config = {k.lower(): v for k, v in config.items()}
    else:
        config = params
    return config


def load_dora_inputs_and_task(dora_event):
    task_inputs = json.loads(dora_event["value"][0].as_py())
    dora_result = json.loads(dora_event["value"][0].as_py())
    if isinstance(task_inputs, dict):
        task = task_inputs.get('task', None)
    else:
        task = task_inputs
    return task_inputs,dora_result,task

def create_agent_output(step_name:str,output_data:Union[str,dict],dataflow_status:bool=False):
    if isinstance(output_data,dict):
        output_data = json.dumps(output_data)
    return json.dumps({'step_name':step_name,'node_results':output_data,'dataflow_status':dataflow_status})