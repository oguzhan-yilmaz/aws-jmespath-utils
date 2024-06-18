from .filter_tags import AwsJmespathUtilsCustomFunctions
import jmespath

jmespath_options = jmespath.Options(custom_functions=AwsJmespathUtilsCustomFunctions())
