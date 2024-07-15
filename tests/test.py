from pprint import pprint
import json
from aws_jmespath_utils import FilterTagsCustomFunction
import jmespath 

_jmespath_options = jmespath.Options(custom_functions=FilterTagsCustomFunction())

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