import jmespath
from jmespath import functions
import fnmatch
from typing import List, Dict, Union
import logging
from os import environ as env_vars

logging.basicConfig(level=env_vars.get('AWS_JMESPATH_UTILS_LOG_LEVEL', logging.INFO))



def get_tags_of_data(data: Dict) -> List:
    tag_pair_list = data.get("Tags", False)
    if not tag_pair_list:
        return False
    rv = []    
    for tag_pair in tag_pair_list:
        a_tag_key = tag_pair.get('Key')
        a_tag_value = tag_pair.get('Value')
        rv.append((a_tag_key,a_tag_value))
    if not rv:
        return False    
    return rv
    
def is_accepted(expression: str, data: Dict) -> bool:
    MATCH_ANY_EXPRESSIONS=("=", "*=","=*","*=*")
    _is_any_expression = expression in MATCH_ANY_EXPRESSIONS
    if _is_any_expression:
        logging.debug(f"Expression('{expression}') matches ANY, returning True...")
        return True 
    if expression=="" or expression is None:
        logging.debug(f"Expression is empty. Try to use '[] | filter_tags(`[\"*=*\"]`, @)' to get started.")
        return False 
   
    try:
        expr_key, expr_value = expression.split('=')
    except ValueError as e:
        logging.info(f"Failed to parse expression: {expression}, check documentation. Exiting...")
        exit(1)
    
    tags_list = get_tags_of_data(data)
    if not tags_list:
        # resource does not have tags
        return False    
    
    _accepted = False
    
    for tag_pair in tags_list:
        # look for any matching tag pair
        a_tag_key,a_tag_value=tag_pair
        _expr_key_match = False
        _expr_value_match = False
            
        # if it's empty string or *, we skip that part of expression
        _skip_key_matching = expr_key == '' or expr_key == '*'
        _skip_value_matching = expr_value == '' or expr_value == '*'
        
        
        
        if not _skip_key_matching:
            _expr_key_match = fnmatch.fnmatch(a_tag_key, expr_key)
        if not _skip_value_matching:
            _expr_value_match = fnmatch.fnmatch(a_tag_value, expr_value)
        
        # if we do not skip both, we should use 'and' operation 
        compare_both = (not _skip_key_matching) and (not _skip_value_matching)
        
        if compare_both:
            if _expr_key_match and _expr_value_match:
                _accepted = True
                logging.debug(f"Accepted data:\n\t{a_tag_key=} {expr_key=} {_skip_key_matching=}\n\t{a_tag_value=} {expr_value=} {_skip_value_matching=}")
                break
        else: 
            if _expr_key_match or _expr_value_match:
                _accepted = True
                logging.debug(f"Accepted data:\n\t{a_tag_key=} {expr_key=} {_skip_key_matching=}\n\t{a_tag_value=} {expr_value=} {_skip_value_matching=}")
                break
    return _accepted
