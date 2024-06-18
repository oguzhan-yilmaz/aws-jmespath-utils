import jmespath
from jmespath import functions
import fnmatch

def get_tags_of_data(data:dict):
    # TODO: change my data to real aws Tags=[{Key:Value},...] and do this part again. I'm missing something
    tags_list = data.get("Tags", False)
    if not tags_list:
        return False
    rv = []    
    for tag_pair in tags_list:
        a_tag_key = tag_pair.get('Key')
        a_tag_value = tag_pair.get('Value')
        rv.append((a_tag_key,a_tag_value))
    if not rv:
        return False    
    return rv
    
def is_accepted(expression, data: dict) -> bool:
    MATCH_ANY_EXPRESSIONS=("=", "*=","=*","*=*")
    _is_any_expression = expression in MATCH_ANY_EXPRESSIONS
    if _is_any_expression:
        return True 
    
    _accepted = False
    expr_key, expr_value = expression.split('=')

    tags_list = get_tags_of_data(data)
    if not tags_list:
        # resource does not have tags
        # it should be accepted if only it's not strict ??
        pass
    
    
    for tag_pair in tags_list:
        a_tag_key,a_tag_value=tag_pair
        # print(f"doing tag: {a_tag_key} : {a_tag_value}")
        _expr_key_match = False
        _expr_value_match = False
            
        if expr_key != '' and expr_key != '*':
            _expr_key_match = fnmatch.fnmatch(a_tag_key, expr_key)
        if expr_value != '' and expr_value != '*':
            _expr_value_match = fnmatch.fnmatch(a_tag_value, expr_value)
        
        if _expr_key_match or _expr_value_match:
            _accepted = True
            break
    return _accepted

class AwsJmespathUtilsCustomFunctions(functions.Functions):
    @functions.signature({'types': ["array"]}, {'types': ["array", "object"]})
    def _func_filter_tags(self, expression_list, data):

        # print(f"{type(expression_list)}: expression_list is:", expression_list)
        # print(f"{type(data)}: data is:",data)
        # print("-----------")
        
        return_value = None

        if type(data)==list:
            # print("data type is list")
            # apply for each element on the list
            return_value = []
            accepted_indices_map = {
                str(i): False
                for i, _d in enumerate(data)
            }
            
            for expression in expression_list:
                # print(f"processing expr: {expression}")
                for i, elmt in enumerate(data):
                    # print(f"doing {i} = {elmt}")
                    accepted_indices_map[str(i)] = accepted_indices_map[str(i)] or is_accepted(expression, elmt)

            for i, elmt in enumerate(data):
                if accepted_indices_map[str(i)]:
                    # return_value.append(elmt)
                    return_value.append(elmt.get('Tags'))
            return return_value
        
        if type(data)==dict:
            # print("data type is dict")
            # apply for the current dict only
            for expression in expression_list:
                # print(f"processing expr: {expression}")
                if is_accepted(expression, data):
                    return_value = data
            return return_value     
        return f"!{data}!"



def test():
    _jmespath_options = jmespath.Options(custom_functions=AwsJmespathUtilsCustomFunctions())
    from pprint import pprint
    import json
    data = None
    with open('tests/data/ec2_describe_instances.json', 'r') as file:
        data = json.load(file)

    pprint(
        jmespath.search(
            # '[] | filter_tags(`["="]`, @)',
            'DescribeInstances[*].Reservations[*].Instances[].filter_tags(`["=hum*","=ca*","Te*="]`, @)',
            data,
            options=_jmespath_options)
    )

    # TODO: ifilter_tags code.
    # Note: exclude pattern with fnmatch: 'filter_tags(`["[!Da.]*="]`, @)',


if __name__ == '__main__':
    test()