# aws-jmespath-utils

## Installation

```bash
pip3 install aws_jmespath_utils
```
## Examples

Check out the example code:

- [examples/01_filter_tags_basic.py](./examples/01_filter_tags_basic.py)


## Usage

**Find resources with Name tag set**

```python
jmespath.search(  # it's important that your expression array must be inside `` backticks
    '[] | filter_tags(`["Name=*"]`, @)', data_list, options=jmespath_options
)
```

**Find Tag values starting with 123**
```python
jmespath.search(  # it's important that your expression array must be inside `` backticks
    '[].filter_tags(`["=123*"]`, @)', data_list, options=jmespath_options
)
```

**Setting log levels**

```bash
# set log level as you wish
export AWS_JMESPATH_UTILS_LOG_LEVEL="DEBUG"   
export AWS_JMESPATH_UTILS_LOG_LEVEL="WARNING"   
export AWS_JMESPATH_UTILS_LOG_LEVEL="INFO"  # default   
```


