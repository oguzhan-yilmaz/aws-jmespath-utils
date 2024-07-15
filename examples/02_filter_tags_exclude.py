""" NOTE:
pip3 install aws_jmespath_utils  
"""
import jmespath
from aws_jmespath_utils import jmespath_options
from os import environ as env_vars
from json import dumps 

data_list = [    
    {"a": "a", "Tags": [{"Key": "Name", "Value": "jmespath-utils"}, ]},
    {"b": "b", "Tags": [{"Key": "Namee", "Value": "jmespath-utils-nam"}, {"Key": "map-migrated", "Value": "789"}]},
    {"c": "c", "Tags": [{"Key": "Ebcd", "Value": "edfg"}, {"Key": "map-migrated", "Value": "234"}]}
]




expression = '[] | exclude_tags(`["Name="]`, @)[].Tags' # it's important that your expression array must be inside `` backticks
search_no_name_tag=jmespath.search(expression, data_list, options=jmespath_options)
print("--*--"*10, f"Using jmespath expression: '{expression}'", dumps(search_no_name_tag, indent=2), "", sep='\n')




expression = '[] | exclude_tags(`["Ebcd="]`, @)[].Tags' # it's important that your expression array must be inside `` backticks
search_no_tag_value_Ebc=jmespath.search(expression, data_list, options=jmespath_options)
print("--*--"*10, f"Using jmespath expression: '{expression}'", dumps(search_no_tag_value_Ebc, indent=2), "", sep='\n')





