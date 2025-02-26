import collections.abc
from functions import get_research_help

# Provide backward compatibility for the package (To mitigate import error with Mappings)
if not hasattr(collections, 'Mapping'):
    collections.Mapping = collections.abc.Mapping
if not hasattr(collections, 'MutableMapping'):
    collections.MutableMapping = collections.abc.MutableMapping
if not hasattr(collections, 'Callable'):
    collections.Callable = collections.abc.Callable


# get_research_help('Napoleonic Wars', 3, "claude-3-haiku-20240307")
# get_research_help('Oil Crisis 1970s', 4, "claude-3-haiku-20240307")
# get_research_help('History of Nuclear Weapon', 2, "claude-3-haiku-20240307")
get_research_help('Russian-Japanese war in 1905', 2, "claude-3-haiku-20240307")