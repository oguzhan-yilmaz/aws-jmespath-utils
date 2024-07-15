from .common import (
    get_tags_of_data,
    is_accepted
)
import jmespath 
from jmespath import functions
from typing import List, Dict, Union
import logging
from os import environ as env_vars

logging.basicConfig(level=env_vars.get('AWS_JMESPATH_UTILS_LOG_LEVEL', logging.INFO))


class FilterTagsCustomFunction(functions.Functions):
    @functions.signature({'types': ["array"]}, {'types': ["array", "object"]})
    def _func_exclude_tags(self, expression_list: List, data: Union[Dict, List[Dict]]):

        
        result_list = None
        # logging.debug(f"_func_filter_tags data type is: {type(data)}")

        if type(data)==list:
            # print("data type is list")
            # apply for each element on the list
            result_list = []
            denied_indices_map = {
                str(i): False
                for i, _d in enumerate(data)
            }
            
            for expression in expression_list:
                for i, elmt in enumerate(data):
                    # find which elements are accepted by index
                    if denied_indices_map[str(i)] is False:
                        denied_indices_map[str(i)] = is_accepted(expression, elmt)

            for i, elmt in enumerate(data):
                if not denied_indices_map[str(i)]:
                    result_list.append(elmt)
            if result_list:  # result_list might be empty []
                return result_list 
            else:
                return None
            
        if type(data)==dict:
            # apply for the current dict only
            for expression in expression_list:
                if is_accepted(expression, data) and data:
                    return None    
            return data 
        raise Exception(f"Unimplemented data type: {type(data)} :: {data}")


    
    
    @functions.signature({'types': ["array"]}, {'types': ["array", "object"]})
    def _func_filter_tags(self, expression_list: List, data: Union[Dict, List[Dict]]):

        # print(f"{type(expression_list)}: expression_list is:", expression_list)
        # print(f"{type(data)}: data is:",data)
        # print("-----------")
        
        result_list = None
        # logging.debug(f"_func_filter_tags data type is: {type(data)}")

        if type(data)==list:
            # print("data type is list")
            # apply for each element on the list
            result_list = []
            accepted_indices_map = {
                str(i): False
                for i, _d in enumerate(data)
            }
            
            for expression in expression_list:
                for i, elmt in enumerate(data):
                    # find which elements are accepted by index
                    if accepted_indices_map[str(i)] is False:
                        accepted_indices_map[str(i)] = is_accepted(expression, elmt)

            for i, elmt in enumerate(data):
                if accepted_indices_map[str(i)]:
                    result_list.append(elmt)
            if result_list:  # result_list might be empty []
                return result_list 
            else:
                return None
            
        if type(data)==dict:
            # apply for the current dict only
            for expression in expression_list:
                if is_accepted(expression, data) and data:
                    return data     
            return None
        raise Exception(f"Unimplemented data type: {type(data)} :: {data}")



def test():
    _jmespath_options = jmespath.Options(custom_functions=FilterTagsCustomFunction())
    from pprint import pprint
    import json
    data = None
    with open('tests/data/ec2_describe_instances.json', 'r') as file:
        data = json.load(file)
        
    # 'DescribeInstances[*].Reservations[*].Instances[].filter_tags(`["=CHAT*"]`, @)[].exclude_tags(`["="]`, @)',
    # 'DescribeInstances[*].Reservations[*].Instances[].exclude_tags(`["Name=*"]`, @)[].Tags',
    # 'DescribeInstances[*].Reservations[*].Instances[].filter_tags(`["=can*"]`, @)',

    print('Filter test')
    print(
        json.dumps(
            jmespath.search(
            'DescribeInstances[*].Reservations[*].Instances[].filter_tags(`["=can*"]`, @)[].Tags',
            data,
            options=_jmespath_options),
            indent=2
        )
    )
    print('Exclude test')
    print(
        json.dumps(
            jmespath.search(
            'DescribeInstances[*].Reservations[*].Instances[].exclude_tags(`["=can*"]`, @)[].Tags',
            data,
            options=_jmespath_options),
            indent=2
        )
    )

if __name__ == '__main__':
    test()