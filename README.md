# aws-jmespath-utils

## Installation

```bash
pip3 install aws_jmespath_utils
```

## Usage

```python
import jmespath
from aws_jmespath_utils import jmespath_options

result = jmespath.search(
    'filter_tags(`["=ab*"]`, @)',
    {
        "a":"b",
        "Tags": [{"Key": "Name", "Value": "jmespath-utils"}]    
    },
    options=jmespath_options
)

print(result)
```
