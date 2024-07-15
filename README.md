# aws-jmespath-utils

## Installation

```bash
pip3 install aws_jmespath_utils
```

## Examples

Check out the example code:

- [examples/01_filter_tags_basic.py](./examples/01_filter_tags_basic.py)
- [examples/02_filter_tags_exclude.py](./examples/02_filter_tags_exclude.py)

## Usage

**Find resources with 'Name' tag set**

```python
jmespath.search(  # it's important that your expression array must be inside `` backticks
    '[] | filter_tags(`["Name=*"]`, @)', data_list, options=jmespath_options
)
```

**Find tag values starting with 123**

```python
jmespath.search(  # it's important that your expression array must be inside `` backticks
    '[].filter_tags(`["=123*"]`, @)', data_list, options=jmespath_options
)
```

**Find Many tag values**

```python
jmespath.search(  # it's important that your expression array must be inside `` backticks
    '[].filter_tags(`["=123*", "=jmespath*"]`, @)', data_list, options=jmespath_options
)
```

**Exclude Tags**

```python
jmespath.search(  # it's important that your expression array must be inside `` backticks
    '[].exclude_tags(`["map-migrated=*"]`, @)', data_list, options=jmespath_options
)
```

**Setting log levels**

```bash
# set log level as you wish
export AWS_JMESPATH_UTILS_LOG_LEVEL="DEBUG"   
export AWS_JMESPATH_UTILS_LOG_LEVEL="INFO"  # default   
```



## Complete Usage Example

```python
import jmespath
from aws_jmespath_utils import jmespath_options
import json
data_list = [    
    {"a": "a", "Tags": [{"Key": "Name", "Value": "jmespath-utils"}, ]},
    {"b": "b", "Tags": [{"Key": "Nam", "Value": "jmespath-utils-nam"}]},
    {"c": "c", "Tags": [{"Key": "map-migrated", "Value": "234"}]}
]

print(
    json.dumps(
        jmespath.search('[] | filter_tags(`["Name=*"]`, @)', data_list, options=jmespath_options),
        indent=2
    )
)

print(
    json.dumps(
        jmespath.search('[] | exclude_tags(`["Nam*="]`, @)', data_list, options=jmespath_options),
        indent=2
    )
)

```