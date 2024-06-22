""" NOTE:
pip3 install aws_jmespath_utils  
"""
import jmespath
from aws_jmespath_utils import jmespath_options
from os import environ as env_vars
from json import dumps 

data_list = [    
    {"a": "a", "Tags": [{"Key": "Name", "Value": "jmespath-utils"}, ]},
    {"b": "b", "Tags": [{"Key": "Name", "Value": "jmespath-utils-nam"}, {"Key": "map-migrated", "Value": "1234"}]},
    {"c": "c", "Tags": [{"Key": "Ebcd", "Value": "edfg"}, {"Key": "map-migrated", "Value": "6789"}]}
]


print("#"*20, f"data: {dumps(data_list,indent=2)}", "", "#"*20, "", sep="\n")

expression = '[] | filter_tags(`["Name="]`, @)' # it's important that your expression array must be inside `` backticks
search_name_tag=jmespath.search(expression, data_list, options=jmespath_options)
print("--*--"*10, f"Using jmespath expression: '{expression}'", dumps(search_name_tag, indent=2), "", sep='\n')


 
expression = '[].filter_tags(`["*=1234"]`, @)' # it's important that your expression array must be inside `` backticks
search_tag_value_1234=jmespath.search(expression, data_list, options=jmespath_options)
print("--*--"*10, f"Using jmespath expression: '{expression}'", dumps(search_tag_value_1234, indent=2), "", sep='\n')