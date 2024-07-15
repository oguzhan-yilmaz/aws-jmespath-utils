from .filter_tags import FilterTagsCustomFunction
import jmespath

jmespath_options = jmespath.Options(custom_functions=FilterTagsCustomFunction())
