# Combined Pydantic Documentation

## Table of Contents

- [latest](#latest)
- [latest api aliases](#latest_api_aliases)
- [latest api annotated handlers](#latest_api_annotated_handlers)
- [latest api base model](#latest_api_base_model)
- [latest api config](#latest_api_config)
- [latest api dataclasses](#latest_api_dataclasses)
- [latest api errors](#latest_api_errors)
- [latest api experimental](#latest_api_experimental)
- [latest api fields](#latest_api_fields)
- [latest api functional serializers](#latest_api_functional_serializers)
- [latest api functional validators](#latest_api_functional_validators)
- [latest api json schema](#latest_api_json_schema)
- [latest api networks](#latest_api_networks)
- [latest api pydantic core](#latest_api_pydantic_core)
- [latest api pydantic core schema](#latest_api_pydantic_core_schema)
- [latest api pydantic extra types color](#latest_api_pydantic_extra_types_color)
- [latest api pydantic extra types coordinate](#latest_api_pydantic_extra_types_coordinate)
- [latest api pydantic extra types country](#latest_api_pydantic_extra_types_country)
- [latest api pydantic extra types currency code](#latest_api_pydantic_extra_types_currency_code)
- [latest api pydantic extra types isbn](#latest_api_pydantic_extra_types_isbn)
- [latest api pydantic extra types language code](#latest_api_pydantic_extra_types_language_code)
- [latest api pydantic extra types mac address](#latest_api_pydantic_extra_types_mac_address)
- [latest api pydantic extra types payment](#latest_api_pydantic_extra_types_payment)
- [latest api pydantic extra types pendulum dt](#latest_api_pydantic_extra_types_pendulum_dt)
- [latest api pydantic extra types phone numbers](#latest_api_pydantic_extra_types_phone_numbers)
- [latest api pydantic extra types routing numbers](#latest_api_pydantic_extra_types_routing_numbers)
- [latest api pydantic extra types script code](#latest_api_pydantic_extra_types_script_code)
- [latest api pydantic extra types semantic version](#latest_api_pydantic_extra_types_semantic_version)
- [latest api pydantic extra types timezone name](#latest_api_pydantic_extra_types_timezone_name)
- [latest api pydantic extra types ulid](#latest_api_pydantic_extra_types_ulid)
- [latest api pydantic settings](#latest_api_pydantic_settings)
- [latest api root model](#latest_api_root_model)
- [latest api standard library types](#latest_api_standard_library_types)
- [latest api type adapter](#latest_api_type_adapter)
- [latest api types](#latest_api_types)
- [latest api validate call](#latest_api_validate_call)
- [latest api version](#latest_api_version)
- [latest changelog](#latest_changelog)
- [latest concepts alias](#latest_concepts_alias)
- [latest concepts config](#latest_concepts_config)
- [latest concepts conversion table](#latest_concepts_conversion_table)
- [latest concepts dataclasses](#latest_concepts_dataclasses)
- [latest concepts experimental](#latest_concepts_experimental)
- [latest concepts fields](#latest_concepts_fields)
- [latest concepts forward annotations](#latest_concepts_forward_annotations)
- [latest concepts json](#latest_concepts_json)
- [latest concepts json schema](#latest_concepts_json_schema)
- [latest concepts models](#latest_concepts_models)
- [latest concepts performance](#latest_concepts_performance)
- [latest concepts pydantic settings](#latest_concepts_pydantic_settings)
- [latest concepts serialization](#latest_concepts_serialization)
- [latest concepts strict mode](#latest_concepts_strict_mode)
- [latest concepts type adapter](#latest_concepts_type_adapter)
- [latest concepts types](#latest_concepts_types)
- [latest concepts unions](#latest_concepts_unions)
- [latest concepts validation decorator](#latest_concepts_validation_decorator)
- [latest concepts validators](#latest_concepts_validators)
- [latest contributing](#latest_contributing)
- [latest errors errors](#latest_errors_errors)
- [latest errors usage errors](#latest_errors_usage_errors)
- [latest errors validation errors](#latest_errors_validation_errors)
- [latest examples custom validators](#latest_examples_custom_validators)
- [latest examples files](#latest_examples_files)
- [latest examples orms](#latest_examples_orms)
- [latest examples queues](#latest_examples_queues)
- [latest examples requests](#latest_examples_requests)
- [latest help with pydantic](#latest_help_with_pydantic)
- [latest install](#latest_install)
- [latest integrations aws lambda](#latest_integrations_aws_lambda)
- [latest integrations datamodel code generator](#latest_integrations_datamodel_code_generator)
- [latest integrations devtools](#latest_integrations_devtools)
- [latest integrations hypothesis](#latest_integrations_hypothesis)
- [latest integrations linting](#latest_integrations_linting)
- [latest integrations logfire](#latest_integrations_logfire)
- [latest integrations mypy](#latest_integrations_mypy)
- [latest integrations pycharm](#latest_integrations_pycharm)
- [latest integrations rich](#latest_integrations_rich)
- [latest integrations visual studio code](#latest_integrations_visual_studio_code)
- [latest internals architecture](#latest_internals_architecture)
- [latest internals resolving annotations](#latest_internals_resolving_annotations)
- [latest migration](#latest_migration)
- [latest pydantic people](#latest_pydantic_people)
- [latest version-policy](#latest_version-policy)
- [latest why](#latest_why)
- [pydantic docs combined](#pydantic_docs_combined)

---

<a id='latest'></a>

## latest

Pydantic 
dev


Welcome to Pydantic 
Type to start searching


  * Get Started  Get Started 
  * Concepts  Concepts 
  * API Documentation  API Documentation 
    * Pydantic  Pydantic 
    * Pydantic Core  Pydantic Core 
    * Pydantic Extra Types  Pydantic Extra Types 
  * Internals  Internals 
  * Examples  Examples 
  * Error Messages  Error Messages 
  * Integrations  Integrations 
    * Dev Tools  Dev Tools 
    * Production Tools  Production Tools 


Page contents 


Pydantic is the most widely used data validation library for Python.
Fast and extensible, Pydantic plays nicely with your linters/IDE/brain. Define how data should be in pure, canonical Python 3.8+; validate it with Pydantic.
Logfire integrates with many popular Python libraries including FastAPI, OpenAI and Pydantic itself, so you can use Logfire to monitor Pydantic validations and understand why some inputs fail validation:
Monitoring Pydantic with Logfire```
from datetime import datetime
import logfire
from pydantic import BaseModel
logfire.configure()

class Delivery(BaseModel):
  timestamp: datetime
  dimensions: tuple[int, int]

# this will record details of a successful validation to logfire
m = Delivery(timestamp='2020-01-02T03:04:05Z', dimensions=['10', '20'])
print(repr(m.timestamp))
#> datetime.datetime(2020, 1, 2, 3, 4, 5, tzinfo=TzInfo(UTC))
print(m.dimensions)
#> (10, 20)

```

Would give you a view like this in the Logfire platform:
This is just a toy example, but hopefully makes clear the potential value of instrumenting a more complex application.


To see Pydantic at work, let's start with a simple example, creating a custom class that inherits from `BaseModel`:
Validation Successful```
from datetime import datetime
from pydantic import BaseModel, PositiveInt

class User(BaseModel):

external_data = {
  'id': 123,
  'tastes': {
    'wine': 9,
  },
}
#> 123
"""
{
  'id': 123,
  'name': 'John Doe',
  'signup_ts': datetime.datetime(2019, 6, 1, 12, 22),
  'tastes': {'wine': 9, 'cheese': 7, 'cabbage': 1},
}
"""

```

If validation fails, Pydantic will raise an error with a breakdown of what was wrong:
Validation Error```
# continuing the above example...
from datetime import datetime
from pydantic import BaseModel, PositiveInt, ValidationError

class User(BaseModel):
  id: int
  name: str = 'John Doe'
  signup_ts: datetime | None
  tastes: dict[str, PositiveInt]

try:
except ValidationError as e:
  print(e.errors())
"""
  [
    {
      'type': 'int_parsing',
      'loc': ('id',),
      'msg': 'Input should be a valid integer, unable to parse string as an integer',
      'input': 'not an int',
    },
    {
      'type': 'missing',
      'loc': ('signup_ts',),
      'msg': 'Field required',
      'input': {'id': 'not an int', 'tastes': {}},
    },
  ]
  """

```

Hundreds of organisations and packages are using Pydantic. Some of the prominent companies and organizations around the world who are using Pydantic include:
Was this page helpful? 
Thanks for your feedback! 
Thanks for your feedback! 
Back to top 

---

<a id='latest_api_aliases'></a>

## latest api aliases

Pydantic 
dev


Aliases 
Type to start searching


  * Get Started  Get Started 
  * Concepts  Concepts 
  * API Documentation  API Documentation 
    * Pydantic  Pydantic 
    * Pydantic Core  Pydantic Core 
    * Pydantic Extra Types  Pydantic Extra Types 
  * Internals  Internals 
  * Examples  Examples 
  * Error Messages  Error Messages 
  * Integrations  Integrations 
    * Dev Tools  Dev Tools 
    * Production Tools  Production Tools 


Page contents 


# Aliases
Support for alias configurations.
```

```

Usage Documentation
A data class used by `validation_alias` as a convenience to create aliases.
Attributes:
Name | Type | Description  
---|---|---  
Source code in `pydantic/aliases.py`
```

```
| ```
def __init__(self, first_arg: str, *args: str | int) -> None:
  self.path = [first_arg] + list(args)

```
  
---|---  
```

```

Converts arguments to a list of string or integer aliases.
Returns:
Type | Description  
---|---  
Source code in `pydantic/aliases.py`
```

```
| ```
def convert_to_aliases(self) -> list[str | int]:
"""Converts arguments to a list of string or integer aliases.
  Returns:
    The list of aliases.
  """
  return self.path

```
  
---|---  
```

```

Searches a dictionary for the path specified by the alias.
Returns:
Type | Description  
---|---  
Source code in `pydantic/aliases.py`
```

```
| ```
def search_dict_for_path(self, d: dict) -> Any:
"""Searches a dictionary for the path specified by the alias.
  Returns:
    The value at the specified path, or `PydanticUndefined` if the path is not found.
  """
  v = d
  for k in self.path:
    if isinstance(v, str):
      # disallow indexing into a str, like for AliasPath('x', 0) and x='abc'
      return PydanticUndefined
    try:
      v = v[k]
    except (KeyError, IndexError, TypeError):
      return PydanticUndefined
  return v

```
  
---|---  
```
AliasChoices(
)

```

Usage Documentation
A data class used by `validation_alias` as a convenience to create aliases.
Attributes:
Name | Type | Description  
---|---|---  
Source code in `pydantic/aliases.py`
```

```
| ```
def __init__(self, first_choice: str | AliasPath, *choices: str | AliasPath) -> None:
  self.choices = [first_choice] + list(choices)

```
  
---|---  
```

```

Converts arguments to a list of lists containing string or integer aliases.
Returns:
Type | Description  
---|---  
Source code in `pydantic/aliases.py`
```

```
| ```
def convert_to_aliases(self) -> list[list[str | int]]:
"""Converts arguments to a list of lists containing string or integer aliases.
  Returns:
    The list of aliases.
  """
  aliases: list[list[str | int]] = []
  for c in self.choices:
    if isinstance(c, AliasPath):
      aliases.append(c.convert_to_aliases())
    else:
      aliases.append([c])
  return aliases

```
  
---|---  
```
AliasGenerator(
  validation_alias: (
    | None
  ) = None,
)

```

Usage Documentation
A data class used by `alias_generator` as a convenience to create various aliases.
Attributes:
Name | Type | Description  
---|---|---  
```
generate_aliases(
]

```

Generate `alias`, `validation_alias`, and `serialization_alias` for a field.
Returns:
Type | Description  
---|---  
Source code in `pydantic/aliases.py`
```
```
| ```
def generate_aliases(self, field_name: str) -> tuple[str | None, str | AliasPath | AliasChoices | None, str | None]:
"""Generate `alias`, `validation_alias`, and `serialization_alias` for a field.
  Returns:
    A tuple of three aliases - validation, alias, and serialization.
  """
  alias = self._generate_alias('alias', (str,), field_name)
  validation_alias = self._generate_alias('validation_alias', (str, AliasChoices, AliasPath), field_name)
  serialization_alias = self._generate_alias('serialization_alias', (str,), field_name)
  return alias, validation_alias, serialization_alias # type: ignore

```
  
---|---  
Was this page helpful? 
Thanks for your feedback! 
Thanks for your feedback! 
Back to top 

---

<a id='latest_api_annotated_handlers'></a>

## latest api annotated handlers

Pydantic 
dev


Annotated Handlers 
Type to start searching


  * Get Started  Get Started 
  * Concepts  Concepts 
  * API Documentation  API Documentation 
    * Pydantic  Pydantic 
    * Pydantic Core  Pydantic Core 
    * Pydantic Extra Types  Pydantic Extra Types 
  * Internals  Internals 
  * Examples  Examples 
  * Error Messages  Error Messages 
  * Integrations  Integrations 
    * Dev Tools  Dev Tools 
    * Production Tools  Production Tools 


Page contents 


# Annotated Handlers
Type annotations to use with `__get_pydantic_core_schema__` and `__get_pydantic_json_schema__`.
Handler to call into the next JSON schema generation function.
Attributes:
Name | Type | Description  
---|---|---  
```
resolve_ref_schema(

```

Get the real schema for a `{"$ref": ...}` schema. If the schema given is not a `$ref` schema, it will be returned as is. This means you don't have to check before calling this function.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
Raises:
Type | Description  
---|---  
Returns:
Name | Type | Description  
---|---|---  
Source code in `pydantic/annotated_handlers.py`
```

```
| ```
def resolve_ref_schema(self, maybe_ref_json_schema: JsonSchemaValue, /) -> JsonSchemaValue:
"""Get the real schema for a `{"$ref": ...}` schema.
  If the schema given is not a `$ref` schema, it will be returned as is.
  This means you don't have to check before calling this function.
  Args:
    maybe_ref_json_schema: A JsonSchemaValue which may be a `$ref` schema.
  Raises:
    LookupError: If the ref is not found.
  Returns:
    JsonSchemaValue: A JsonSchemaValue that has no `$ref`.
  """
  raise NotImplementedError

```
  
---|---  
Handler to call into the next CoreSchema schema generation function.
```

```

Get the name of the closest field to this validator.
```

```

Generate a schema unrelated to the current context. Use this function if e.g. you are handling schema generation for a sequence and want to generate a schema for its items. Otherwise, you may end up doing something like applying a `min_length` constraint that was intended for the sequence itself to its items!
Parameters:
Name | Type | Description | Default  
---|---|---|---  
Returns:
Name | Type | Description  
---|---|---  
`CoreSchema` |  `CoreSchema` |  The `pydantic-core` CoreSchema generated.  
Source code in `pydantic/annotated_handlers.py`
```

```
| ```
def generate_schema(self, source_type: Any, /) -> core_schema.CoreSchema:
"""Generate a schema unrelated to the current context.
  Use this function if e.g. you are handling schema generation for a sequence
  and want to generate a schema for its items.
  Otherwise, you may end up doing something like applying a `min_length` constraint
  that was intended for the sequence itself to its items!
  Args:
    source_type: The input type.
  Returns:
    CoreSchema: The `pydantic-core` CoreSchema generated.
  """
  raise NotImplementedError

```
  
---|---  
```
resolve_ref_schema(
  maybe_ref_schema: CoreSchema,
) -> CoreSchema

```

Get the real schema for a `definition-ref` schema. If the schema given is not a `definition-ref` schema, it will be returned as is. This means you don't have to check before calling this function.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`maybe_ref_schema` |  `CoreSchema` |  A `CoreSchema`, `ref`-based or not. |  _required_  
Raises:
Type | Description  
---|---  
Returns:
Type | Description  
---|---  
`CoreSchema` |  A concrete `CoreSchema`.  
Source code in `pydantic/annotated_handlers.py`
```

```
| ```
def resolve_ref_schema(self, maybe_ref_schema: core_schema.CoreSchema, /) -> core_schema.CoreSchema:
"""Get the real schema for a `definition-ref` schema.
  If the schema given is not a `definition-ref` schema, it will be returned as is.
  This means you don't have to check before calling this function.
  Args:
    maybe_ref_schema: A `CoreSchema`, `ref`-based or not.
  Raises:
    LookupError: If the `ref` is not found.
  Returns:
    A concrete `CoreSchema`.
  """
  raise NotImplementedError

```
  
---|---  
Was this page helpful? 
Thanks for your feedback! 
Thanks for your feedback! 
Back to top 

---

<a id='latest_api_base_model'></a>

## latest api base model

Pydantic 
dev


BaseModel 
Initializing search 


  * Get Started  Get Started 
  * Concepts  Concepts 
  * API Documentation  API Documentation 
    * Pydantic  Pydantic 
    * Pydantic Core  Pydantic Core 
    * Pydantic Extra Types  Pydantic Extra Types 
  * Internals  Internals 
  * Examples  Examples 
  * Error Messages  Error Messages 
  * Integrations  Integrations 
    * Dev Tools  Dev Tools 
    * Production Tools  Production Tools 


Page contents 


# BaseModel
Pydantic models are simply classes which inherit from `BaseModel` and define fields as annotated attributes.
Usage Documentation
A base class for creating Pydantic models.
Attributes:
Name | Type | Description  
---|---|---  
`__pydantic_decorators__` |  `DecoratorInfos` |  Metadata containing the decorators defined on the model. This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1.  
`__pydantic_generic_metadata__` |  `PydanticGenericMetadata` |  Metadata for generic models; contains data used for a similar purpose to **args** , **origin** , **parameters** in typing-module generics. May eventually be replaced by these.  
Source code in `pydantic/main.py`
```
 
```
| ```
class BaseModel(metaclass=_model_construction.ModelMetaclass):
  A base class for creating Pydantic models.
  Attributes:
    __class_vars__: The names of the class variables defined on the model.
    __private_attributes__: Metadata about the private attributes of the model.
    __signature__: The synthesized `__init__` [`Signature`][inspect.Signature] of the model.
    __pydantic_complete__: Whether model building is completed, or if there are still undefined fields.
    __pydantic_core_schema__: The core schema of the model.
    __pydantic_custom_init__: Whether the model has a custom `__init__` function.
    __pydantic_decorators__: Metadata containing the decorators defined on the model.
      This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1.
    __pydantic_generic_metadata__: Metadata for generic models; contains data used for a similar purpose to
      __args__, __origin__, __parameters__ in typing-module generics. May eventually be replaced by these.
    __pydantic_parent_namespace__: Parent namespace of the model, used for automatic rebuilding of models.
    __pydantic_post_init__: The name of the post-init method for the model, if defined.
    __pydantic_root_model__: Whether the model is a [`RootModel`][pydantic.root_model.RootModel].
    __pydantic_serializer__: The `pydantic-core` `SchemaSerializer` used to dump instances of the model.
    __pydantic_validator__: The `pydantic-core` `SchemaValidator` used to validate instances of the model.
    __pydantic_fields__: A dictionary of field names and their corresponding [`FieldInfo`][pydantic.fields.FieldInfo] objects.
    __pydantic_computed_fields__: A dictionary of computed field names and their corresponding [`ComputedFieldInfo`][pydantic.fields.ComputedFieldInfo] objects.
    __pydantic_extra__: A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]
      is set to `'allow'`.
    __pydantic_fields_set__: The names of fields explicitly set during instantiation.
    __pydantic_private__: Values of private attributes set on the model instance.
  """
  # Note: Many of the below class vars are defined in the metaclass, but we define them here for type checking purposes.
  model_config: ClassVar[ConfigDict] = ConfigDict()
"""
  Configuration for the model, should be a dictionary conforming to [`ConfigDict`][pydantic.config.ConfigDict].
  """
  # Because `dict` is in the local namespace of the `BaseModel` class, we use `Dict` for annotations.
  # TODO v3 fallback to `dict` when the deprecated `dict` method gets removed.
  __class_vars__: ClassVar[set[str]]
"""The names of the class variables defined on the model."""
  __private_attributes__: ClassVar[Dict[str, ModelPrivateAttr]] # noqa: UP006
"""Metadata about the private attributes of the model."""
  __signature__: ClassVar[Signature]
"""The synthesized `__init__` [`Signature`][inspect.Signature] of the model."""
  __pydantic_complete__: ClassVar[bool] = False
"""Whether model building is completed, or if there are still undefined fields."""
  __pydantic_core_schema__: ClassVar[CoreSchema]
"""The core schema of the model."""
  __pydantic_custom_init__: ClassVar[bool]
"""Whether the model has a custom `__init__` method."""
  # Must be set for `GenerateSchema.model_schema` to work for a plain `BaseModel` annotation.
  __pydantic_decorators__: ClassVar[_decorators.DecoratorInfos] = _decorators.DecoratorInfos()
"""Metadata containing the decorators defined on the model.
  This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1."""
  __pydantic_generic_metadata__: ClassVar[_generics.PydanticGenericMetadata]
"""Metadata for generic models; contains data used for a similar purpose to
  __args__, __origin__, __parameters__ in typing-module generics. May eventually be replaced by these."""
  __pydantic_parent_namespace__: ClassVar[Dict[str, Any] | None] = None # noqa: UP006
"""Parent namespace of the model, used for automatic rebuilding of models."""
  __pydantic_post_init__: ClassVar[None | Literal['model_post_init']]
"""The name of the post-init method for the model, if defined."""
  __pydantic_root_model__: ClassVar[bool] = False
"""Whether the model is a [`RootModel`][pydantic.root_model.RootModel]."""
  __pydantic_serializer__: ClassVar[SchemaSerializer]
"""The `pydantic-core` `SchemaSerializer` used to dump instances of the model."""
  __pydantic_validator__: ClassVar[SchemaValidator | PluggableSchemaValidator]
"""The `pydantic-core` `SchemaValidator` used to validate instances of the model."""
  __pydantic_fields__: ClassVar[Dict[str, FieldInfo]] # noqa: UP006
"""A dictionary of field names and their corresponding [`FieldInfo`][pydantic.fields.FieldInfo] objects.
  This replaces `Model.__fields__` from Pydantic V1.
  """
  __pydantic_computed_fields__: ClassVar[Dict[str, ComputedFieldInfo]] # noqa: UP006
"""A dictionary of computed field names and their corresponding [`ComputedFieldInfo`][pydantic.fields.ComputedFieldInfo] objects."""
  __pydantic_extra__: dict[str, Any] | None = _model_construction.NoInitField(init=False)
"""A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra] is set to `'allow'`."""
  __pydantic_fields_set__: set[str] = _model_construction.NoInitField(init=False)
"""The names of fields explicitly set during instantiation."""
  __pydantic_private__: dict[str, Any] | None = _model_construction.NoInitField(init=False)
"""Values of private attributes set on the model instance."""
  if not TYPE_CHECKING:
    # Prevent `BaseModel` from being instantiated directly
    # (defined in an `if not TYPE_CHECKING` block for clarity and to avoid type checking errors):
    __pydantic_core_schema__ = _mock_val_ser.MockCoreSchema(
      'Pydantic models should inherit from BaseModel, BaseModel cannot be instantiated directly',
      code='base-model-instantiated',
    )
    __pydantic_validator__ = _mock_val_ser.MockValSer(
      'Pydantic models should inherit from BaseModel, BaseModel cannot be instantiated directly',
      val_or_ser='validator',
      code='base-model-instantiated',
    )
    __pydantic_serializer__ = _mock_val_ser.MockValSer(
      'Pydantic models should inherit from BaseModel, BaseModel cannot be instantiated directly',
      val_or_ser='serializer',
      code='base-model-instantiated',
    )
  __slots__ = '__dict__', '__pydantic_fields_set__', '__pydantic_extra__', '__pydantic_private__'
  def __init__(self, /, **data: Any) -> None:
"""Create a new model by parsing and validating input data from keyword arguments.
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    `self` is explicitly positional-only to allow `self` as a field name.
    """
    # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks
    __tracebackhide__ = True
    validated_self = self.__pydantic_validator__.validate_python(data, self_instance=self)
    if self is not validated_self:
      warnings.warn(
        'A custom validator is returning a value other than `self`.\n'
        "Returning anything other than `self` from a top level model validator isn't supported when validating via `__init__`.\n"
        stacklevel=2,
      )
  # The following line sets a flag that we use to determine when `__init__` gets overridden by the user
  __init__.__pydantic_base_init__ = True # pyright: ignore[reportFunctionMemberAccess]
  if TYPE_CHECKING:
    model_fields: ClassVar[dict[str, FieldInfo]]
    model_computed_fields: ClassVar[dict[str, ComputedFieldInfo]]
  else:
    # TODO: V3 - remove `model_fields` and `model_computed_fields` properties from the `BaseModel` class - they should only
    # be accessible on the model class, not on instances. We have these purely for backwards compatibility with Pydantic <v2.10.
    # This is similar to the fact that we have __fields__ defined here (on `BaseModel`) and on `ModelMetaClass`.
    # Another problem here is that there's no great way to have class properties :(
    @property
    def model_fields(self) -> dict[str, FieldInfo]:
"""Get metadata about the fields defined on the model.
      Deprecation warning: you should be getting this information from the model class, not from an instance.
      In V3, this property will be removed from the `BaseModel` class.
      Returns:
        A mapping of field names to [`FieldInfo`][pydantic.fields.FieldInfo] objects.
      """
      # Must be set for `GenerateSchema.model_schema` to work for a plain `BaseModel` annotation, hence the default here.
      return getattr(self, '__pydantic_fields__', {})
    @property
    def model_computed_fields(self) -> dict[str, ComputedFieldInfo]:
"""Get metadata about the computed fields defined on the model.
      Deprecation warning: you should be getting this information from the model class, not from an instance.
      In V3, this property will be removed from the `BaseModel` class.
      Returns:
        A mapping of computed field names to [`ComputedFieldInfo`][pydantic.fields.ComputedFieldInfo] objects.
      """
      # Must be set for `GenerateSchema.model_schema` to work for a plain `BaseModel` annotation, hence the default here.
      return getattr(self, '__pydantic_computed_fields__', {})
  @property
  def model_extra(self) -> dict[str, Any] | None:
"""Get extra fields set during validation.
    Returns:
      A dictionary of extra fields, or `None` if `config.extra` is not set to `"allow"`.
    """
    return self.__pydantic_extra__
  @property
  def model_fields_set(self) -> set[str]:
"""Returns the set of fields that have been explicitly set on this model instance.
    Returns:
      A set of strings representing the fields that have been set,
        i.e. that were not filled from defaults.
    """
    return self.__pydantic_fields_set__
  @classmethod
  def model_construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self: # noqa: C901
"""Creates a new instance of the `Model` class with validated data.
    Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
    Default values are respected, but no other validation is performed.
    !!! note
      `model_construct()` generally respects the `model_config.extra` setting on the provided model.
      That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
      and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
      Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
      an error if extra values are passed, but they will be ignored.
    Args:
      _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
        this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
        Otherwise, the field names from the `values` argument will be used.
      values: Trusted or pre-validated data dictionary.
    Returns:
      A new instance of the `Model` class with validated data.
    """
    m = cls.__new__(cls)
    fields_values: dict[str, Any] = {}
    fields_set = set()
    for name, field in cls.__pydantic_fields__.items():
      if field.alias is not None and field.alias in values:
        fields_values[name] = values.pop(field.alias)
        fields_set.add(name)
      if (name not in fields_set) and (field.validation_alias is not None):
        validation_aliases: list[str | AliasPath] = (
          field.validation_alias.choices
          if isinstance(field.validation_alias, AliasChoices)
          else [field.validation_alias]
        )
        for alias in validation_aliases:
          if isinstance(alias, str) and alias in values:
            fields_values[name] = values.pop(alias)
            fields_set.add(name)
            break
          elif isinstance(alias, AliasPath):
            value = alias.search_dict_for_path(values)
            if value is not PydanticUndefined:
              fields_values[name] = value
              fields_set.add(name)
              break
      if name not in fields_set:
        if name in values:
          fields_values[name] = values.pop(name)
          fields_set.add(name)
        elif not field.is_required():
          fields_values[name] = field.get_default(call_default_factory=True, validated_data=fields_values)
    if _fields_set is None:
      _fields_set = fields_set
    _extra: dict[str, Any] | None = values if cls.model_config.get('extra') == 'allow' else None
    _object_setattr(m, '__dict__', fields_values)
    _object_setattr(m, '__pydantic_fields_set__', _fields_set)
    if not cls.__pydantic_root_model__:
      _object_setattr(m, '__pydantic_extra__', _extra)
    if cls.__pydantic_post_init__:
      m.model_post_init(None)
      # update private attributes with values set
      if hasattr(m, '__pydantic_private__') and m.__pydantic_private__ is not None:
        for k, v in values.items():
          if k in m.__private_attributes__:
            m.__pydantic_private__[k] = v
    elif not cls.__pydantic_root_model__:
      # Note: if there are any private attributes, cls.__pydantic_post_init__ would exist
      # Since it doesn't, that means that `__pydantic_private__` should be set to None
      _object_setattr(m, '__pydantic_private__', None)
    return m
  def model_copy(self, *, update: Mapping[str, Any] | None = None, deep: bool = False) -> Self:
    Returns a copy of the model.
    Args:
      update: Values to change/add in the new model. Note: the data is not validated
        before creating the new model. You should trust this data.
      deep: Set to `True` to make a deep copy of the model.
    Returns:
      New model instance.
    """
    copied = self.__deepcopy__() if deep else self.__copy__()
    if update:
      if self.model_config.get('extra') == 'allow':
        for k, v in update.items():
          if k in self.__pydantic_fields__:
            copied.__dict__[k] = v
          else:
            if copied.__pydantic_extra__ is None:
              copied.__pydantic_extra__ = {}
            copied.__pydantic_extra__[k] = v
      else:
        copied.__dict__.update(update)
      copied.__pydantic_fields_set__.update(update.keys())
    return copied
  def model_dump(
    self,
    *,
    mode: Literal['json', 'python'] | str = 'python',
    include: IncEx | None = None,
    exclude: IncEx | None = None,
    context: Any | None = None,
    by_alias: bool = False,
    exclude_unset: bool = False,
    exclude_defaults: bool = False,
    exclude_none: bool = False,
    round_trip: bool = False,
    warnings: bool | Literal['none', 'warn', 'error'] = True,
    serialize_as_any: bool = False,
  ) -> dict[str, Any]:
    Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
    Args:
      mode: The mode in which `to_python` should run.
        If mode is 'json', the output will only contain JSON serializable types.
        If mode is 'python', the output may contain non-JSON-serializable Python objects.
      include: A set of fields to include in the output.
      exclude: A set of fields to exclude from the output.
      context: Additional context to pass to the serializer.
      by_alias: Whether to use the field's alias in the dictionary key if defined.
      exclude_unset: Whether to exclude fields that have not been explicitly set.
      exclude_defaults: Whether to exclude fields that are set to their default value.
      exclude_none: Whether to exclude fields that have a value of `None`.
      round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
      warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
      serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
    Returns:
      A dictionary representation of the model.
    """
    return self.__pydantic_serializer__.to_python(
      self,
      mode=mode,
      by_alias=by_alias,
      include=include,
      exclude=exclude,
      context=context,
      exclude_unset=exclude_unset,
      exclude_defaults=exclude_defaults,
      exclude_none=exclude_none,
      round_trip=round_trip,
      warnings=warnings,
      serialize_as_any=serialize_as_any,
    )
  def model_dump_json(
    self,
    *,
    indent: int | None = None,
    include: IncEx | None = None,
    exclude: IncEx | None = None,
    context: Any | None = None,
    by_alias: bool = False,
    exclude_unset: bool = False,
    exclude_defaults: bool = False,
    exclude_none: bool = False,
    round_trip: bool = False,
    warnings: bool | Literal['none', 'warn', 'error'] = True,
    serialize_as_any: bool = False,
  ) -> str:
    Generates a JSON representation of the model using Pydantic's `to_json` method.
    Args:
      indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
      include: Field(s) to include in the JSON output.
      exclude: Field(s) to exclude from the JSON output.
      context: Additional context to pass to the serializer.
      by_alias: Whether to serialize using field aliases.
      exclude_unset: Whether to exclude fields that have not been explicitly set.
      exclude_defaults: Whether to exclude fields that are set to their default value.
      exclude_none: Whether to exclude fields that have a value of `None`.
      round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
      warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
      serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
    Returns:
      A JSON string representation of the model.
    """
    return self.__pydantic_serializer__.to_json(
      self,
      indent=indent,
      include=include,
      exclude=exclude,
      context=context,
      by_alias=by_alias,
      exclude_unset=exclude_unset,
      exclude_defaults=exclude_defaults,
      exclude_none=exclude_none,
      round_trip=round_trip,
      warnings=warnings,
      serialize_as_any=serialize_as_any,
    ).decode()
  @classmethod
  def model_json_schema(
    cls,
    by_alias: bool = True,
    ref_template: str = DEFAULT_REF_TEMPLATE,
    schema_generator: type[GenerateJsonSchema] = GenerateJsonSchema,
    mode: JsonSchemaMode = 'validation',
  ) -> dict[str, Any]:
"""Generates a JSON schema for a model class.
    Args:
      by_alias: Whether to use attribute aliases or not.
      ref_template: The reference template.
      schema_generator: To override the logic used to generate the JSON schema, as a subclass of
        `GenerateJsonSchema` with your desired modifications
      mode: The mode in which to generate the schema.
    Returns:
      The JSON schema for the given model class.
    """
    return model_json_schema(
      cls, by_alias=by_alias, ref_template=ref_template, schema_generator=schema_generator, mode=mode
    )
  @classmethod
  def model_parametrized_name(cls, params: tuple[type[Any], ...]) -> str:
"""Compute the class name for parametrizations of generic classes.
    This method can be overridden to achieve a custom naming scheme for generic BaseModels.
    Args:
      params: Tuple of types of the class. Given a generic class
        `Model` with 2 type variables and a concrete model `Model[str, int]`,
        the value `(str, int)` would be passed to `params`.
    Returns:
      String representing the new class where `params` are passed to `cls` as type variables.
    Raises:
      TypeError: Raised when trying to generate concrete names for non-generic models.
    """
    if not issubclass(cls, typing.Generic):
      raise TypeError('Concrete names should only be generated for generic models.')
    # Any strings received should represent forward references, so we handle them specially below.
    # If we eventually move toward wrapping them in a ForwardRef in __class_getitem__ in the future,
    # we may be able to remove this special case.
    param_names = [param if isinstance(param, str) else _repr.display_as_type(param) for param in params]
    params_component = ', '.join(param_names)
    return f'{cls.__name__}[{params_component}]'
  def model_post_init(self, __context: Any) -> None:
"""Override this method to perform additional initialization after `__init__` and `model_construct`.
    This is useful if you want to do some validation that requires the entire model to be initialized.
    """
    pass
  @classmethod
  def model_rebuild(
    cls,
    *,
    force: bool = False,
    raise_errors: bool = True,
    _parent_namespace_depth: int = 2,
    _types_namespace: MappingNamespace | None = None,
  ) -> bool | None:
"""Try to rebuild the pydantic-core schema for the model.
    This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
    the initial attempt to build the schema, and automatic rebuilding fails.
    Args:
      force: Whether to force the rebuilding of the model schema, defaults to `False`.
      raise_errors: Whether to raise errors, defaults to `True`.
      _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
      _types_namespace: The types namespace, defaults to `None`.
    Returns:
      Returns `None` if the schema is already "complete" and rebuilding was not required.
      If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
    """
    if not force and cls.__pydantic_complete__:
      return None
    if '__pydantic_core_schema__' in cls.__dict__:
      delattr(cls, '__pydantic_core_schema__') # delete cached value to ensure full rebuild happens
    if _types_namespace is not None:
      rebuild_ns = _types_namespace
    elif _parent_namespace_depth > 0:
      rebuild_ns = _typing_extra.parent_frame_namespace(parent_depth=_parent_namespace_depth, force=True) or {}
    else:
      rebuild_ns = {}
    parent_ns = _model_construction.unpack_lenient_weakvaluedict(cls.__pydantic_parent_namespace__) or {}
    ns_resolver = _namespace_utils.NsResolver(
      parent_namespace={**rebuild_ns, **parent_ns},
    )
    # manually override defer_build so complete_model_class doesn't skip building the model again
    config = {**cls.model_config, 'defer_build': False}
    return _model_construction.complete_model_class(
      cls,
      cls.__name__,
      _config.ConfigWrapper(config, check=False),
      raise_errors=raise_errors,
      ns_resolver=ns_resolver,
    )
  @classmethod
  def model_validate(
    cls,
    obj: Any,
    *,
    strict: bool | None = None,
    from_attributes: bool | None = None,
    context: Any | None = None,
  ) -> Self:
"""Validate a pydantic model instance.
    Args:
      obj: The object to validate.
      strict: Whether to enforce types strictly.
      from_attributes: Whether to extract data from object attributes.
      context: Additional context to pass to the validator.
    Raises:
      ValidationError: If the object could not be validated.
    Returns:
      The validated model instance.
    """
    # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks
    __tracebackhide__ = True
    return cls.__pydantic_validator__.validate_python(
      obj, strict=strict, from_attributes=from_attributes, context=context
    )
  @classmethod
  def model_validate_json(
    cls,
    json_data: str | bytes | bytearray,
    *,
    strict: bool | None = None,
    context: Any | None = None,
  ) -> Self:
    Validate the given JSON data against the Pydantic model.
    Args:
      json_data: The JSON data to validate.
      strict: Whether to enforce types strictly.
      context: Extra variables to pass to the validator.
    Returns:
      The validated Pydantic model.
    Raises:
      ValidationError: If `json_data` is not a JSON string or the object could not be validated.
    """
    # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks
    __tracebackhide__ = True
    return cls.__pydantic_validator__.validate_json(json_data, strict=strict, context=context)
  @classmethod
  def model_validate_strings(
    cls,
    obj: Any,
    *,
    strict: bool | None = None,
    context: Any | None = None,
  ) -> Self:
"""Validate the given object with string data against the Pydantic model.
    Args:
      obj: The object containing string data to validate.
      strict: Whether to enforce types strictly.
      context: Extra variables to pass to the validator.
    Returns:
      The validated Pydantic model.
    """
    # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks
    __tracebackhide__ = True
    return cls.__pydantic_validator__.validate_strings(obj, strict=strict, context=context)
  @classmethod
  def __get_pydantic_core_schema__(cls, source: type[BaseModel], handler: GetCoreSchemaHandler, /) -> CoreSchema:
"""Hook into generating the model's CoreSchema.
    Args:
      source: The class we are generating a schema for.
        This will generally be the same as the `cls` argument if this is a classmethod.
      handler: A callable that calls into Pydantic's internal CoreSchema generation logic.
    Returns:
      A `pydantic-core` `CoreSchema`.
    """
    # Only use the cached value from this _exact_ class; we don't want one from a parent class
    # This is why we check `cls.__dict__` and don't use `cls.__pydantic_core_schema__` or similar.
    schema = cls.__dict__.get('__pydantic_core_schema__')
    if schema is not None and not isinstance(schema, _mock_val_ser.MockCoreSchema):
      # Due to the way generic classes are built, it's possible that an invalid schema may be temporarily
      # set on generic classes. I think we could resolve this to ensure that we get proper schema caching
      # for generics, but for simplicity for now, we just always rebuild if the class has a generic origin.
      if not cls.__pydantic_generic_metadata__['origin']:
        return cls.__pydantic_core_schema__
    return handler(source)
  @classmethod
  def __get_pydantic_json_schema__(
    cls,
    core_schema: CoreSchema,
    handler: GetJsonSchemaHandler,
    /,
  ) -> JsonSchemaValue:
"""Hook into generating the model's JSON schema.
    Args:
      core_schema: A `pydantic-core` CoreSchema.
        You can ignore this argument and call the handler with a new CoreSchema,
        wrap this CoreSchema (`{'type': 'nullable', 'schema': current_schema}`),
        or just call the handler with the original schema.
      handler: Call into Pydantic's internal JSON schema generation.
        This will raise a `pydantic.errors.PydanticInvalidForJsonSchema` if JSON schema
        generation fails.
        Since this gets called by `BaseModel.model_json_schema` you can override the
        `schema_generator` argument to that function to change JSON schema generation globally
        for a type.
    Returns:
      A JSON schema, as a Python object.
    """
    return handler(core_schema)
  @classmethod
  def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
"""This is intended to behave just like `__init_subclass__`, but is called by `ModelMetaclass`
    only after the class is actually fully initialized. In particular, attributes like `model_fields` will
    be present when this is called.
    This is necessary because `__init_subclass__` will always be called by `type.__new__`,
    and it would require a prohibitively large refactor to the `ModelMetaclass` to ensure that
    `type.__new__` was called in such a manner that the class would already be sufficiently initialized.
    This will receive the same `kwargs` that would be passed to the standard `__init_subclass__`, namely,
    any kwargs passed to the class definition that aren't used internally by pydantic.
    Args:
      **kwargs: Any keyword arguments passed to the class definition that aren't used internally
        by pydantic.
    """
    pass
  def __class_getitem__(
    cls, typevar_values: type[Any] | tuple[type[Any], ...]
  ) -> type[BaseModel] | _forward_ref.PydanticRecursiveRef:
    cached = _generics.get_cached_generic_type_early(cls, typevar_values)
    if cached is not None:
      return cached
    if cls is BaseModel:
      raise TypeError('Type parameters should be placed on typing.Generic, not BaseModel')
    if not hasattr(cls, '__parameters__'):
      raise TypeError(f'{cls} cannot be parametrized because it does not inherit from typing.Generic')
    if not cls.__pydantic_generic_metadata__['parameters'] and typing.Generic not in cls.__bases__:
      raise TypeError(f'{cls} is not a generic class')
    if not isinstance(typevar_values, tuple):
      typevar_values = (typevar_values,)
    _generics.check_parameters_count(cls, typevar_values)
    # Build map from generic typevars to passed params
    typevars_map: dict[TypeVar, type[Any]] = dict(
      zip(cls.__pydantic_generic_metadata__['parameters'], typevar_values)
    )
    if _utils.all_identical(typevars_map.keys(), typevars_map.values()) and typevars_map:
      submodel = cls # if arguments are equal to parameters it's the same object
      _generics.set_cached_generic_type(cls, typevar_values, submodel)
    else:
      parent_args = cls.__pydantic_generic_metadata__['args']
      if not parent_args:
        args = typevar_values
      else:
        args = tuple(_generics.replace_types(arg, typevars_map) for arg in parent_args)
      origin = cls.__pydantic_generic_metadata__['origin'] or cls
      model_name = origin.model_parametrized_name(args)
      params = tuple(
        {param: None for param in _generics.iter_contained_typevars(typevars_map.values())}
      ) # use dict as ordered set
      with _generics.generic_recursion_self_type(origin, args) as maybe_self_type:
        cached = _generics.get_cached_generic_type_late(cls, typevar_values, origin, args)
        if cached is not None:
          return cached
        if maybe_self_type is not None:
          return maybe_self_type
        # Attempt to rebuild the origin in case new types have been defined
        try:
          # depth 2 gets you above this __class_getitem__ call.
          # Note that we explicitly provide the parent ns, otherwise
          # `model_rebuild` will use the parent ns no matter if it is the ns of a module.
          # We don't want this here, as this has unexpected effects when a model
          # is being parametrized during a forward annotation evaluation.
          parent_ns = _typing_extra.parent_frame_namespace(parent_depth=2) or {}
          origin.model_rebuild(_types_namespace=parent_ns)
        except PydanticUndefinedAnnotation:
          # It's okay if it fails, it just means there are still undefined types
          # that could be evaluated later.
          pass
        submodel = _generics.create_generic_submodel(model_name, origin, args, params)
        # Update cache
        _generics.set_cached_generic_type(cls, typevar_values, submodel, origin, args)
    return submodel
  def __copy__(self) -> Self:
"""Returns a shallow copy of the model."""
    cls = type(self)
    m = cls.__new__(cls)
    _object_setattr(m, '__dict__', copy(self.__dict__))
    _object_setattr(m, '__pydantic_extra__', copy(self.__pydantic_extra__))
    _object_setattr(m, '__pydantic_fields_set__', copy(self.__pydantic_fields_set__))
    if not hasattr(self, '__pydantic_private__') or self.__pydantic_private__ is None:
      _object_setattr(m, '__pydantic_private__', None)
    else:
      _object_setattr(
        m,
        '__pydantic_private__',
        {k: v for k, v in self.__pydantic_private__.items() if v is not PydanticUndefined},
      )
    return m
  def __deepcopy__(self, memo: dict[int, Any] | None = None) -> Self:
"""Returns a deep copy of the model."""
    cls = type(self)
    m = cls.__new__(cls)
    _object_setattr(m, '__dict__', deepcopy(self.__dict__, memo=memo))
    _object_setattr(m, '__pydantic_extra__', deepcopy(self.__pydantic_extra__, memo=memo))
    # This next line doesn't need a deepcopy because __pydantic_fields_set__ is a set[str],
    # and attempting a deepcopy would be marginally slower.
    _object_setattr(m, '__pydantic_fields_set__', copy(self.__pydantic_fields_set__))
    if not hasattr(self, '__pydantic_private__') or self.__pydantic_private__ is None:
      _object_setattr(m, '__pydantic_private__', None)
    else:
      _object_setattr(
        m,
        '__pydantic_private__',
        deepcopy({k: v for k, v in self.__pydantic_private__.items() if v is not PydanticUndefined}, memo=memo),
      )
    return m
  if not TYPE_CHECKING:
    # We put `__getattr__` in a non-TYPE_CHECKING block because otherwise, mypy allows arbitrary attribute access
    def __getattr__(self, item: str) -> Any:
      private_attributes = object.__getattribute__(self, '__private_attributes__')
      if item in private_attributes:
        attribute = private_attributes[item]
        if hasattr(attribute, '__get__'):
          return attribute.__get__(self, type(self)) # type: ignore
        try:
          # Note: self.__pydantic_private__ cannot be None if self.__private_attributes__ has items
          return self.__pydantic_private__[item] # type: ignore
        except KeyError as exc:
          raise AttributeError(f'{type(self).__name__!r} object has no attribute {item!r}') from exc
      else:
        # `__pydantic_extra__` can fail to be set if the model is not yet fully initialized.
        # See `BaseModel.__repr_args__` for more details
        try:
          pydantic_extra = object.__getattribute__(self, '__pydantic_extra__')
        except AttributeError:
          pydantic_extra = None
        if pydantic_extra:
          try:
            return pydantic_extra[item]
          except KeyError as exc:
            raise AttributeError(f'{type(self).__name__!r} object has no attribute {item!r}') from exc
        else:
          if hasattr(self.__class__, item):
            return super().__getattribute__(item) # Raises AttributeError if appropriate
          else:
            # this is the current error
            raise AttributeError(f'{type(self).__name__!r} object has no attribute {item!r}')
    def __setattr__(self, name: str, value: Any) -> None:
      if name in self.__class_vars__:
        raise AttributeError(
          f'{name!r} is a ClassVar of `{self.__class__.__name__}` and cannot be set on an instance. '
          f'If you want to set a value on the class, use `{self.__class__.__name__}.{name} = value`.'
        )
      elif not _fields.is_valid_field_name(name):
        if self.__pydantic_private__ is None or name not in self.__private_attributes__:
          _object_setattr(self, name, value)
        else:
          attribute = self.__private_attributes__[name]
          if hasattr(attribute, '__set__'):
            attribute.__set__(self, value) # type: ignore
          else:
            self.__pydantic_private__[name] = value
        return
      self._check_frozen(name, value)
      attr = getattr(self.__class__, name, None)
      # NOTE: We currently special case properties and `cached_property`, but we might need
      # to generalize this to all data/non-data descriptors at some point. For non-data descriptors
      # (such as `cached_property`), it isn't obvious though. `cached_property` caches the value
      # to the instance's `__dict__`, but other non-data descriptors might do things differently.
      if isinstance(attr, property):
        attr.__set__(self, value)
      elif isinstance(attr, cached_property):
        self.__dict__[name] = value
      elif self.model_config.get('validate_assignment', None):
        self.__pydantic_validator__.validate_assignment(self, name, value)
      elif self.model_config.get('extra') != 'allow' and name not in self.__pydantic_fields__:
        # TODO - matching error
        raise ValueError(f'"{self.__class__.__name__}" object has no field "{name}"')
      elif self.model_config.get('extra') == 'allow' and name not in self.__pydantic_fields__:
        if self.model_extra and name in self.model_extra:
          self.__pydantic_extra__[name] = value # type: ignore
        else:
          try:
            getattr(self, name)
          except AttributeError:
            # attribute does not already exist on instance, so put it in extra
            self.__pydantic_extra__[name] = value # type: ignore
          else:
            # attribute _does_ already exist on instance, and was not in extra, so update it
            _object_setattr(self, name, value)
      else:
        self.__dict__[name] = value
        self.__pydantic_fields_set__.add(name)
    def __delattr__(self, item: str) -> Any:
      if item in self.__private_attributes__:
        attribute = self.__private_attributes__[item]
        if hasattr(attribute, '__delete__'):
          attribute.__delete__(self) # type: ignore
          return
        try:
          # Note: self.__pydantic_private__ cannot be None if self.__private_attributes__ has items
          del self.__pydantic_private__[item] # type: ignore
          return
        except KeyError as exc:
          raise AttributeError(f'{type(self).__name__!r} object has no attribute {item!r}') from exc
      self._check_frozen(item, None)
      if item in self.__pydantic_fields__:
        object.__delattr__(self, item)
      elif self.__pydantic_extra__ is not None and item in self.__pydantic_extra__:
        del self.__pydantic_extra__[item]
      else:
        try:
          object.__delattr__(self, item)
        except AttributeError:
          raise AttributeError(f'{type(self).__name__!r} object has no attribute {item!r}')
    # Because we make use of `@dataclass_transform()`, `__replace__` is already synthesized by
    # type checkers, so we define the implementation in this `if not TYPE_CHECKING:` block:
    def __replace__(self, **changes: Any) -> Self:
      return self.model_copy(update=changes)
  def _check_frozen(self, name: str, value: Any) -> None:
    if self.model_config.get('frozen', None):
      typ = 'frozen_instance'
    elif getattr(self.__pydantic_fields__.get(name), 'frozen', False):
      typ = 'frozen_field'
    else:
      return
    error: pydantic_core.InitErrorDetails = {
      'type': typ,
      'loc': (name,),
      'input': value,
    }
    raise pydantic_core.ValidationError.from_exception_data(self.__class__.__name__, [error])
  def __getstate__(self) -> dict[Any, Any]:
    private = self.__pydantic_private__
    if private:
      private = {k: v for k, v in private.items() if v is not PydanticUndefined}
    return {
      '__dict__': self.__dict__,
      '__pydantic_extra__': self.__pydantic_extra__,
      '__pydantic_fields_set__': self.__pydantic_fields_set__,
      '__pydantic_private__': private,
    }
  def __setstate__(self, state: dict[Any, Any]) -> None:
    _object_setattr(self, '__pydantic_fields_set__', state.get('__pydantic_fields_set__', {}))
    _object_setattr(self, '__pydantic_extra__', state.get('__pydantic_extra__', {}))
    _object_setattr(self, '__pydantic_private__', state.get('__pydantic_private__', {}))
    _object_setattr(self, '__dict__', state.get('__dict__', {}))
  if not TYPE_CHECKING:
    def __eq__(self, other: Any) -> bool:
      if isinstance(other, BaseModel):
        # When comparing instances of generic types for equality, as long as all field values are equal,
        # only require their generic origin types to be equal, rather than exact type equality.
        # This prevents headaches like MyGeneric(x=1) != MyGeneric[Any](x=1).
        self_type = self.__pydantic_generic_metadata__['origin'] or self.__class__
        other_type = other.__pydantic_generic_metadata__['origin'] or other.__class__
        # Perform common checks first
        if not (
          self_type == other_type
          and getattr(self, '__pydantic_private__', None) == getattr(other, '__pydantic_private__', None)
          and self.__pydantic_extra__ == other.__pydantic_extra__
        ):
          return False
        # We only want to compare pydantic fields but ignoring fields is costly.
        # We'll perform a fast check first, and fallback only when needed
        # See GH-7444 and GH-7825 for rationale and a performance benchmark
        # First, do the fast (and sometimes faulty) __dict__ comparison
        if self.__dict__ == other.__dict__:
          # If the check above passes, then pydantic fields are equal, we can return early
          return True
        # We don't want to trigger unnecessary costly filtering of __dict__ on all unequal objects, so we return
        # early if there are no keys to ignore (we would just return False later on anyway)
        model_fields = type(self).__pydantic_fields__.keys()
        if self.__dict__.keys() <= model_fields and other.__dict__.keys() <= model_fields:
          return False
        # If we reach here, there are non-pydantic-fields keys, mapped to unequal values, that we need to ignore
        # Resort to costly filtering of the __dict__ objects
        # We use operator.itemgetter because it is much faster than dict comprehensions
        # NOTE: Contrary to standard python class and instances, when the Model class has a default value for an
        # attribute and the model instance doesn't have a corresponding attribute, accessing the missing attribute
        # raises an error in BaseModel.__getattr__ instead of returning the class attribute
        # So we can use operator.itemgetter() instead of operator.attrgetter()
        getter = operator.itemgetter(*model_fields) if model_fields else lambda _: _utils._SENTINEL
        try:
          return getter(self.__dict__) == getter(other.__dict__)
        except KeyError:
          # In rare cases (such as when using the deprecated BaseModel.copy() method),
          # the __dict__ may not contain all model fields, which is how we can get here.
          # getter(self.__dict__) is much faster than any 'safe' method that accounts
          # for missing keys, and wrapping it in a `try` doesn't slow things down much
          # in the common case.
          self_fields_proxy = _utils.SafeGetItemProxy(self.__dict__)
          other_fields_proxy = _utils.SafeGetItemProxy(other.__dict__)
          return getter(self_fields_proxy) == getter(other_fields_proxy)
      # other instance is not a BaseModel
      else:
        return NotImplemented # delegate to the other item in the comparison
  if TYPE_CHECKING:
    # We put `__init_subclass__` in a TYPE_CHECKING block because, even though we want the type-checking benefits
    # described in the signature of `__init_subclass__` below, we don't want to modify the default behavior of
    # subclass initialization.
    def __init_subclass__(cls, **kwargs: Unpack[ConfigDict]):
"""This signature is included purely to help type-checkers check arguments to class declaration, which
      provides a way to conveniently set model_config key/value pairs.
  ```python
      from pydantic import BaseModel
      class MyModel(BaseModel, extra='allow'): ...
  ```
      However, this may be deceiving, since the _actual_ calls to `__init_subclass__` will not receive any
      of the config arguments, and will only receive any keyword arguments passed during class initialization
      that are _not_ expected keys in ConfigDict. (This is due to the way `ModelMetaclass.__new__` works.)
      Args:
        **kwargs: Keyword arguments passed to the class definition, which set model_config
      Note:
        You may want to override `__pydantic_init_subclass__` instead, which behaves similarly but is called
        *after* the class is fully initialized.
      """
  def __iter__(self) -> TupleGenerator:
"""So `dict(model)` works."""
    yield from [(k, v) for (k, v) in self.__dict__.items() if not k.startswith('_')]
    extra = self.__pydantic_extra__
    if extra:
      yield from extra.items()
  def __repr__(self) -> str:
    return f'{self.__repr_name__()}({self.__repr_str__(", ")})'
  def __repr_args__(self) -> _repr.ReprArgs:
    for k, v in self.__dict__.items():
      field = self.__pydantic_fields__.get(k)
      if field and field.repr:
        if v is not self:
          yield k, v
        else:
          yield k, self.__repr_recursion__(v)
    # `__pydantic_extra__` can fail to be set if the model is not yet fully initialized.
    # This can happen if a `ValidationError` is raised during initialization and the instance's
    # repr is generated as part of the exception handling. Therefore, we use `getattr` here
    # with a fallback, even though the type hints indicate the attribute will always be present.
    try:
      pydantic_extra = object.__getattribute__(self, '__pydantic_extra__')
    except AttributeError:
      pydantic_extra = None
    if pydantic_extra is not None:
      yield from ((k, v) for k, v in pydantic_extra.items())
    yield from ((k, getattr(self, k)) for k, v in self.__pydantic_computed_fields__.items() if v.repr)
  # take logic from `_repr.Representation` without the side effects of inheritance, see #5740
  __repr_name__ = _repr.Representation.__repr_name__
  __repr_recursion__ = _repr.Representation.__repr_recursion__
  __repr_str__ = _repr.Representation.__repr_str__
  __pretty__ = _repr.Representation.__pretty__
  __rich_repr__ = _repr.Representation.__rich_repr__
  def __str__(self) -> str:
    return self.__repr_str__(' ')
  # ##### Deprecated methods from v1 #####
  @property
  @typing_extensions.deprecated(
    'The `__fields__` attribute is deprecated, use `model_fields` instead.', category=None
  )
  def __fields__(self) -> dict[str, FieldInfo]:
    warnings.warn(
      'The `__fields__` attribute is deprecated, use `model_fields` instead.',
      category=PydanticDeprecatedSince20,
      stacklevel=2,
    )
    return self.model_fields
  @property
  @typing_extensions.deprecated(
    'The `__fields_set__` attribute is deprecated, use `model_fields_set` instead.',
    category=None,
  )
  def __fields_set__(self) -> set[str]:
    warnings.warn(
      'The `__fields_set__` attribute is deprecated, use `model_fields_set` instead.',
      category=PydanticDeprecatedSince20,
      stacklevel=2,
    )
    return self.__pydantic_fields_set__
  @typing_extensions.deprecated('The `dict` method is deprecated; use `model_dump` instead.', category=None)
  def dict( # noqa: D102
    self,
    *,
    include: IncEx | None = None,
    exclude: IncEx | None = None,
    by_alias: bool = False,
    exclude_unset: bool = False,
    exclude_defaults: bool = False,
    exclude_none: bool = False,
  ) -> Dict[str, Any]: # noqa UP006
    warnings.warn(
      'The `dict` method is deprecated; use `model_dump` instead.',
      category=PydanticDeprecatedSince20,
      stacklevel=2,
    )
    return self.model_dump(
      include=include,
      exclude=exclude,
      by_alias=by_alias,
      exclude_unset=exclude_unset,
      exclude_defaults=exclude_defaults,
      exclude_none=exclude_none,
    )
  @typing_extensions.deprecated('The `json` method is deprecated; use `model_dump_json` instead.', category=None)
  def json( # noqa: D102
    self,
    *,
    include: IncEx | None = None,
    exclude: IncEx | None = None,
    by_alias: bool = False,
    exclude_unset: bool = False,
    exclude_defaults: bool = False,
    exclude_none: bool = False,
    encoder: Callable[[Any], Any] | None = PydanticUndefined, # type: ignore[assignment]
    models_as_dict: bool = PydanticUndefined, # type: ignore[assignment]
    **dumps_kwargs: Any,
  ) -> str:
    warnings.warn(
      'The `json` method is deprecated; use `model_dump_json` instead.',
      category=PydanticDeprecatedSince20,
      stacklevel=2,
    )
    if encoder is not PydanticUndefined:
      raise TypeError('The `encoder` argument is no longer supported; use field serializers instead.')
    if models_as_dict is not PydanticUndefined:
      raise TypeError('The `models_as_dict` argument is no longer supported; use a model serializer instead.')
    if dumps_kwargs:
      raise TypeError('`dumps_kwargs` keyword arguments are no longer supported.')
    return self.model_dump_json(
      include=include,
      exclude=exclude,
      by_alias=by_alias,
      exclude_unset=exclude_unset,
      exclude_defaults=exclude_defaults,
      exclude_none=exclude_none,
    )
  @classmethod
  @typing_extensions.deprecated('The `parse_obj` method is deprecated; use `model_validate` instead.', category=None)
  def parse_obj(cls, obj: Any) -> Self: # noqa: D102
    warnings.warn(
      'The `parse_obj` method is deprecated; use `model_validate` instead.',
      category=PydanticDeprecatedSince20,
      stacklevel=2,
    )
    return cls.model_validate(obj)
  @classmethod
  @typing_extensions.deprecated(
    'The `parse_raw` method is deprecated; if your data is JSON use `model_validate_json`, '
    'otherwise load the data then use `model_validate` instead.',
    category=None,
  )
  def parse_raw( # noqa: D102
    cls,
    b: str | bytes,
    *,
    content_type: str | None = None,
    encoding: str = 'utf8',
    proto: DeprecatedParseProtocol | None = None,
    allow_pickle: bool = False,
  ) -> Self: # pragma: no cover
    warnings.warn(
      'The `parse_raw` method is deprecated; if your data is JSON use `model_validate_json`, '
      'otherwise load the data then use `model_validate` instead.',
      category=PydanticDeprecatedSince20,
      stacklevel=2,
    )
    from .deprecated import parse
    try:
      obj = parse.load_str_bytes(
        b,
        proto=proto,
        content_type=content_type,
        encoding=encoding,
        allow_pickle=allow_pickle,
      )
    except (ValueError, TypeError) as exc:
      import json
      # try to match V1
      if isinstance(exc, UnicodeDecodeError):
        type_str = 'value_error.unicodedecode'
      elif isinstance(exc, json.JSONDecodeError):
        type_str = 'value_error.jsondecode'
      elif isinstance(exc, ValueError):
        type_str = 'value_error'
      else:
        type_str = 'type_error'
      # ctx is missing here, but since we've added `input` to the error, we're not pretending it's the same
      error: pydantic_core.InitErrorDetails = {
        # The type: ignore on the next line is to ignore the requirement of LiteralString
        'type': pydantic_core.PydanticCustomError(type_str, str(exc)), # type: ignore
        'loc': ('__root__',),
        'input': b,
      }
      raise pydantic_core.ValidationError.from_exception_data(cls.__name__, [error])
    return cls.model_validate(obj)
  @classmethod
  @typing_extensions.deprecated(
    'The `parse_file` method is deprecated; load the data from file, then if your data is JSON '
    'use `model_validate_json`, otherwise `model_validate` instead.',
    category=None,
  )
  def parse_file( # noqa: D102
    cls,
    path: str | Path,
    *,
    content_type: str | None = None,
    encoding: str = 'utf8',
    proto: DeprecatedParseProtocol | None = None,
    allow_pickle: bool = False,
  ) -> Self:
    warnings.warn(
      'The `parse_file` method is deprecated; load the data from file, then if your data is JSON '
      'use `model_validate_json`, otherwise `model_validate` instead.',
      category=PydanticDeprecatedSince20,
      stacklevel=2,
    )
    from .deprecated import parse
    obj = parse.load_file(
      path,
      proto=proto,
      content_type=content_type,
      encoding=encoding,
      allow_pickle=allow_pickle,
    )
    return cls.parse_obj(obj)
  @classmethod
  @typing_extensions.deprecated(
    'The `from_orm` method is deprecated; set '
    "`model_config['from_attributes']=True` and use `model_validate` instead.",
    category=None,
  )
  def from_orm(cls, obj: Any) -> Self: # noqa: D102
    warnings.warn(
      'The `from_orm` method is deprecated; set '
      "`model_config['from_attributes']=True` and use `model_validate` instead.",
      category=PydanticDeprecatedSince20,
      stacklevel=2,
    )
    if not cls.model_config.get('from_attributes', None):
      raise PydanticUserError(
        'You must set the config attribute `from_attributes=True` to use from_orm', code=None
      )
    return cls.model_validate(obj)
  @classmethod
  @typing_extensions.deprecated('The `construct` method is deprecated; use `model_construct` instead.', category=None)
  def construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self: # noqa: D102
    warnings.warn(
      'The `construct` method is deprecated; use `model_construct` instead.',
      category=PydanticDeprecatedSince20,
      stacklevel=2,
    )
    return cls.model_construct(_fields_set=_fields_set, **values)
  @typing_extensions.deprecated(
    'The `copy` method is deprecated; use `model_copy` instead. '
    'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',
    category=None,
  )
  def copy(
    self,
    *,
    include: AbstractSetIntStr | MappingIntStrAny | None = None,
    exclude: AbstractSetIntStr | MappingIntStrAny | None = None,
    update: Dict[str, Any] | None = None, # noqa UP006
    deep: bool = False,
  ) -> Self: # pragma: no cover
"""Returns a copy of the model.
    !!! warning "Deprecated"
      This method is now deprecated; use `model_copy` instead.
    If you need `include` or `exclude`, use:
```python {test="skip" lint="skip"}
    data = self.model_dump(include=include, exclude=exclude, round_trip=True)
    data = {**data, **(update or {})}
    copied = self.model_validate(data)
```
    Args:
      include: Optional set or mapping specifying which fields to include in the copied model.
      exclude: Optional set or mapping specifying which fields to exclude in the copied model.
      update: Optional dictionary of field-value pairs to override field values in the copied model.
      deep: If True, the values of fields that are Pydantic models will be deep-copied.
    Returns:
      A copy of the model with included, excluded and updated fields as specified.
    """
    warnings.warn(
      'The `copy` method is deprecated; use `model_copy` instead. '
      'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',
      category=PydanticDeprecatedSince20,
      stacklevel=2,
    )
    from .deprecated import copy_internals
    values = dict(
      copy_internals._iter(
        self, to_dict=False, by_alias=False, include=include, exclude=exclude, exclude_unset=False
      ),
      **(update or {}),
    )
    if self.__pydantic_private__ is None:
      private = None
    else:
      private = {k: v for k, v in self.__pydantic_private__.items() if v is not PydanticUndefined}
    if self.__pydantic_extra__ is None:
      extra: dict[str, Any] | None = None
    else:
      extra = self.__pydantic_extra__.copy()
      for k in list(self.__pydantic_extra__):
        if k not in values: # k was in the exclude
          extra.pop(k)
      for k in list(values):
        if k in self.__pydantic_extra__: # k must have come from extra
          extra[k] = values.pop(k)
    # new `__pydantic_fields_set__` can have unset optional fields with a set value in `update` kwarg
    if update:
      fields_set = self.__pydantic_fields_set__ | update.keys()
    else:
      fields_set = set(self.__pydantic_fields_set__)
    # removing excluded fields from `__pydantic_fields_set__`
    if exclude:
      fields_set -= set(exclude)
    return copy_internals._copy_and_set_values(self, values, fields_set, extra, private, deep=deep)
  @classmethod
  @typing_extensions.deprecated('The `schema` method is deprecated; use `model_json_schema` instead.', category=None)
  def schema( # noqa: D102
    cls, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE
  ) -> Dict[str, Any]: # noqa UP006
    warnings.warn(
      'The `schema` method is deprecated; use `model_json_schema` instead.',
      category=PydanticDeprecatedSince20,
      stacklevel=2,
    )
    return cls.model_json_schema(by_alias=by_alias, ref_template=ref_template)
  @classmethod
  @typing_extensions.deprecated(
    'The `schema_json` method is deprecated; use `model_json_schema` and json.dumps instead.',
    category=None,
  )
  def schema_json( # noqa: D102
    cls, *, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE, **dumps_kwargs: Any
  ) -> str: # pragma: no cover
    warnings.warn(
      'The `schema_json` method is deprecated; use `model_json_schema` and json.dumps instead.',
      category=PydanticDeprecatedSince20,
      stacklevel=2,
    )
    import json
    from .deprecated.json import pydantic_encoder
    return json.dumps(
      cls.model_json_schema(by_alias=by_alias, ref_template=ref_template),
      default=pydantic_encoder,
      **dumps_kwargs,
    )
  @classmethod
  @typing_extensions.deprecated('The `validate` method is deprecated; use `model_validate` instead.', category=None)
  def validate(cls, value: Any) -> Self: # noqa: D102
    warnings.warn(
      'The `validate` method is deprecated; use `model_validate` instead.',
      category=PydanticDeprecatedSince20,
      stacklevel=2,
    )
    return cls.model_validate(value)
  @classmethod
  @typing_extensions.deprecated(
    'The `update_forward_refs` method is deprecated; use `model_rebuild` instead.',
    category=None,
  )
  def update_forward_refs(cls, **localns: Any) -> None: # noqa: D102
    warnings.warn(
      'The `update_forward_refs` method is deprecated; use `model_rebuild` instead.',
      category=PydanticDeprecatedSince20,
      stacklevel=2,
    )
    if localns: # pragma: no cover
      raise TypeError('`localns` arguments are not longer accepted.')
    cls.model_rebuild(force=True)
  @typing_extensions.deprecated(
    'The private method `_iter` will be removed and should no longer be used.', category=None
  )
  def _iter(self, *args: Any, **kwargs: Any) -> Any:
    warnings.warn(
      'The private method `_iter` will be removed and should no longer be used.',
      category=PydanticDeprecatedSince20,
      stacklevel=2,
    )
    from .deprecated import copy_internals
    return copy_internals._iter(self, *args, **kwargs)
  @typing_extensions.deprecated(
    'The private method `_copy_and_set_values` will be removed and should no longer be used.',
    category=None,
  )
  def _copy_and_set_values(self, *args: Any, **kwargs: Any) -> Any:
    warnings.warn(
      'The private method `_copy_and_set_values` will be removed and should no longer be used.',
      category=PydanticDeprecatedSince20,
      stacklevel=2,
    )
    from .deprecated import copy_internals
    return copy_internals._copy_and_set_values(self, *args, **kwargs)
  @classmethod
  @typing_extensions.deprecated(
    'The private method `_get_value` will be removed and should no longer be used.',
    category=None,
  )
  def _get_value(cls, *args: Any, **kwargs: Any) -> Any:
    warnings.warn(
      'The private method `_get_value` will be removed and should no longer be used.',
      category=PydanticDeprecatedSince20,
      stacklevel=2,
    )
    from .deprecated import copy_internals
    return copy_internals._get_value(cls, *args, **kwargs)
  @typing_extensions.deprecated(
    'The private method `_calculate_keys` will be removed and should no longer be used.',
    category=None,
  )
  def _calculate_keys(self, *args: Any, **kwargs: Any) -> Any:
    warnings.warn(
      'The private method `_calculate_keys` will be removed and should no longer be used.',
      category=PydanticDeprecatedSince20,
      stacklevel=2,
    )
    from .deprecated import copy_internals
    return copy_internals._calculate_keys(self, *args, **kwargs)

```
  
---|---  
```

```

`self` is explicitly positional-only to allow `self` as a field name.
Source code in `pydantic/main.py`
```
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
```
| ```
def __init__(self, /, **data: Any) -> None:
"""Create a new model by parsing and validating input data from keyword arguments.
  Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
  validated to form a valid model.
  `self` is explicitly positional-only to allow `self` as a field name.
  """
  # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks
  __tracebackhide__ = True
  validated_self = self.__pydantic_validator__.validate_python(data, self_instance=self)
  if self is not validated_self:
    warnings.warn(
      'A custom validator is returning a value other than `self`.\n'
      "Returning anything other than `self` from a top level model validator isn't supported when validating via `__init__`.\n"
      stacklevel=2,
    )

```
  
---|---  
```

```

```

```

Get metadata about the computed fields defined on the model.
Deprecation warning: you should be getting this information from the model class, not from an instance. In V3, this property will be removed from the `BaseModel` class.
Returns:
Type | Description  
---|---  
```

```

Get extra fields set during validation.
Returns:
Type | Description  
---|---  
```

```

Get metadata about the fields defined on the model.
Deprecation warning: you should be getting this information from the model class, not from an instance. In V3, this property will be removed from the `BaseModel` class.
Returns:
Type | Description  
---|---  
```

```

Returns the set of fields that have been explicitly set on this model instance.
Returns:
Type | Description  
---|---  
```
__pydantic_core_schema__: CoreSchema

```

The core schema of the model.
```
model_construct(
) -> Self

```

Creates a new instance of the `Model` class with validated data.
Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data. Default values are respected, but no other validation is performed.
Note
`model_construct()` generally respects the `model_config.extra` setting on the provided model. That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__` and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored. Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in an error if extra values are passed, but they will be ignored.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
Returns:
Type | Description  
---|---  
`Self` |  A new instance of the `Model` class with validated data.  
Source code in `pydantic/main.py`
```
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
```
| ```
@classmethod
def model_construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self: # noqa: C901
"""Creates a new instance of the `Model` class with validated data.
  Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
  Default values are respected, but no other validation is performed.
  !!! note
    `model_construct()` generally respects the `model_config.extra` setting on the provided model.
    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
    an error if extra values are passed, but they will be ignored.
  Args:
    _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,
      this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.
      Otherwise, the field names from the `values` argument will be used.
    values: Trusted or pre-validated data dictionary.
  Returns:
    A new instance of the `Model` class with validated data.
  """
  m = cls.__new__(cls)
  fields_values: dict[str, Any] = {}
  fields_set = set()
  for name, field in cls.__pydantic_fields__.items():
    if field.alias is not None and field.alias in values:
      fields_values[name] = values.pop(field.alias)
      fields_set.add(name)
    if (name not in fields_set) and (field.validation_alias is not None):
      validation_aliases: list[str | AliasPath] = (
        field.validation_alias.choices
        if isinstance(field.validation_alias, AliasChoices)
        else [field.validation_alias]
      )
      for alias in validation_aliases:
        if isinstance(alias, str) and alias in values:
          fields_values[name] = values.pop(alias)
          fields_set.add(name)
          break
        elif isinstance(alias, AliasPath):
          value = alias.search_dict_for_path(values)
          if value is not PydanticUndefined:
            fields_values[name] = value
            fields_set.add(name)
            break
    if name not in fields_set:
      if name in values:
        fields_values[name] = values.pop(name)
        fields_set.add(name)
      elif not field.is_required():
        fields_values[name] = field.get_default(call_default_factory=True, validated_data=fields_values)
  if _fields_set is None:
    _fields_set = fields_set
  _extra: dict[str, Any] | None = values if cls.model_config.get('extra') == 'allow' else None
  _object_setattr(m, '__dict__', fields_values)
  _object_setattr(m, '__pydantic_fields_set__', _fields_set)
  if not cls.__pydantic_root_model__:
    _object_setattr(m, '__pydantic_extra__', _extra)
  if cls.__pydantic_post_init__:
    m.model_post_init(None)
    # update private attributes with values set
    if hasattr(m, '__pydantic_private__') and m.__pydantic_private__ is not None:
      for k, v in values.items():
        if k in m.__private_attributes__:
          m.__pydantic_private__[k] = v
  elif not cls.__pydantic_root_model__:
    # Note: if there are any private attributes, cls.__pydantic_post_init__ would exist
    # Since it doesn't, that means that `__pydantic_private__` should be set to None
    _object_setattr(m, '__pydantic_private__', None)
  return m

```
  
---|---  
```
model_copy(
  *,
) -> Self

```

Usage Documentation
Returns a copy of the model.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
Returns:
Type | Description  
---|---  
`Self` |  New model instance.  
Source code in `pydantic/main.py`
```
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
```
| ```
def model_copy(self, *, update: Mapping[str, Any] | None = None, deep: bool = False) -> Self:
  Returns a copy of the model.
  Args:
    update: Values to change/add in the new model. Note: the data is not validated
      before creating the new model. You should trust this data.
    deep: Set to `True` to make a deep copy of the model.
  Returns:
    New model instance.
  """
  copied = self.__deepcopy__() if deep else self.__copy__()
  if update:
    if self.model_config.get('extra') == 'allow':
      for k, v in update.items():
        if k in self.__pydantic_fields__:
          copied.__dict__[k] = v
        else:
          if copied.__pydantic_extra__ is None:
            copied.__pydantic_extra__ = {}
          copied.__pydantic_extra__[k] = v
    else:
      copied.__dict__.update(update)
    copied.__pydantic_fields_set__.update(update.keys())
  return copied

```
  
---|---  
```
model_dump(
  *,
  include: IncEx | None = None,
  exclude: IncEx | None = None,
  warnings: (
  ) = True,

```

Usage Documentation
Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`include` |  `IncEx | None` |  A set of fields to include in the output. |  `None`  
`exclude` |  `IncEx | None` |  A set of fields to exclude from the output. |  `None`  
Returns:
Type | Description  
---|---  
Source code in `pydantic/main.py`
```
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
```
| ```
def model_dump(
  self,
  *,
  mode: Literal['json', 'python'] | str = 'python',
  include: IncEx | None = None,
  exclude: IncEx | None = None,
  context: Any | None = None,
  by_alias: bool = False,
  exclude_unset: bool = False,
  exclude_defaults: bool = False,
  exclude_none: bool = False,
  round_trip: bool = False,
  warnings: bool | Literal['none', 'warn', 'error'] = True,
  serialize_as_any: bool = False,
) -> dict[str, Any]:
  Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.
  Args:
    mode: The mode in which `to_python` should run.
      If mode is 'json', the output will only contain JSON serializable types.
      If mode is 'python', the output may contain non-JSON-serializable Python objects.
    include: A set of fields to include in the output.
    exclude: A set of fields to exclude from the output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to use the field's alias in the dictionary key if defined.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
      "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
  Returns:
    A dictionary representation of the model.
  """
  return self.__pydantic_serializer__.to_python(
    self,
    mode=mode,
    by_alias=by_alias,
    include=include,
    exclude=exclude,
    context=context,
    exclude_unset=exclude_unset,
    exclude_defaults=exclude_defaults,
    exclude_none=exclude_none,
    round_trip=round_trip,
    warnings=warnings,
    serialize_as_any=serialize_as_any,
  )

```
  
---|---  
```
model_dump_json(
  *,
  include: IncEx | None = None,
  exclude: IncEx | None = None,
  warnings: (
  ) = True,

```

Usage Documentation
Generates a JSON representation of the model using Pydantic's `to_json` method.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`include` |  `IncEx | None` |  Field(s) to include in the JSON output. |  `None`  
`exclude` |  `IncEx | None` |  Field(s) to exclude from the JSON output. |  `None`  
Returns:
Type | Description  
---|---  
Source code in `pydantic/main.py`
```
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
484
485
486
487
488
489
490
```
| ```
def model_dump_json(
  self,
  *,
  indent: int | None = None,
  include: IncEx | None = None,
  exclude: IncEx | None = None,
  context: Any | None = None,
  by_alias: bool = False,
  exclude_unset: bool = False,
  exclude_defaults: bool = False,
  exclude_none: bool = False,
  round_trip: bool = False,
  warnings: bool | Literal['none', 'warn', 'error'] = True,
  serialize_as_any: bool = False,
) -> str:
  Generates a JSON representation of the model using Pydantic's `to_json` method.
  Args:
    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.
    include: Field(s) to include in the JSON output.
    exclude: Field(s) to exclude from the JSON output.
    context: Additional context to pass to the serializer.
    by_alias: Whether to serialize using field aliases.
    exclude_unset: Whether to exclude fields that have not been explicitly set.
    exclude_defaults: Whether to exclude fields that are set to their default value.
    exclude_none: Whether to exclude fields that have a value of `None`.
    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].
    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,
      "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].
    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.
  Returns:
    A JSON string representation of the model.
  """
  return self.__pydantic_serializer__.to_json(
    self,
    indent=indent,
    include=include,
    exclude=exclude,
    context=context,
    by_alias=by_alias,
    exclude_unset=exclude_unset,
    exclude_defaults=exclude_defaults,
    exclude_none=exclude_none,
    round_trip=round_trip,
    warnings=warnings,
    serialize_as_any=serialize_as_any,
  ).decode()

```
  
---|---  
```
model_json_schema(
  ] = GenerateJsonSchema,

```

Generates a JSON schema for a model class.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
Returns:
Type | Description  
---|---  
Source code in `pydantic/main.py`
```
492
493
494
495
496
497
498
499
500
501
502
503
504
505
506
507
508
509
510
511
512
513
514
```
| ```
@classmethod
def model_json_schema(
  cls,
  by_alias: bool = True,
  ref_template: str = DEFAULT_REF_TEMPLATE,
  schema_generator: type[GenerateJsonSchema] = GenerateJsonSchema,
  mode: JsonSchemaMode = 'validation',
) -> dict[str, Any]:
"""Generates a JSON schema for a model class.
  Args:
    by_alias: Whether to use attribute aliases or not.
    ref_template: The reference template.
    schema_generator: To override the logic used to generate the JSON schema, as a subclass of
      `GenerateJsonSchema` with your desired modifications
    mode: The mode in which to generate the schema.
  Returns:
    The JSON schema for the given model class.
  """
  return model_json_schema(
    cls, by_alias=by_alias, ref_template=ref_template, schema_generator=schema_generator, mode=mode
  )

```
  
---|---  
```
model_parametrized_name(

```

Compute the class name for parametrizations of generic classes.
This method can be overridden to achieve a custom naming scheme for generic BaseModels.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
Returns:
Type | Description  
---|---  
Raises:
Type | Description  
---|---  
Source code in `pydantic/main.py`
```

```
| ```
@classmethod
def model_parametrized_name(cls, params: tuple[type[Any], ...]) -> str:
"""Compute the class name for parametrizations of generic classes.
  This method can be overridden to achieve a custom naming scheme for generic BaseModels.
  Args:
    params: Tuple of types of the class. Given a generic class
      `Model` with 2 type variables and a concrete model `Model[str, int]`,
      the value `(str, int)` would be passed to `params`.
  Returns:
    String representing the new class where `params` are passed to `cls` as type variables.
  Raises:
    TypeError: Raised when trying to generate concrete names for non-generic models.
  """
  if not issubclass(cls, typing.Generic):
    raise TypeError('Concrete names should only be generated for generic models.')
  # Any strings received should represent forward references, so we handle them specially below.
  # If we eventually move toward wrapping them in a ForwardRef in __class_getitem__ in the future,
  # we may be able to remove this special case.
  param_names = [param if isinstance(param, str) else _repr.display_as_type(param) for param in params]
  params_component = ', '.join(param_names)
  return f'{cls.__name__}[{params_component}]'

```
  
---|---  
```

```

Override this method to perform additional initialization after `__init__` and `model_construct`. This is useful if you want to do some validation that requires the entire model to be initialized.
Source code in `pydantic/main.py`
```

```
| ```
def model_post_init(self, __context: Any) -> None:
"""Override this method to perform additional initialization after `__init__` and `model_construct`.
  This is useful if you want to do some validation that requires the entire model to be initialized.
  """
  pass

```
  
---|---  
```
model_rebuild(
  *,
  _types_namespace: MappingNamespace | None = None

```

Try to rebuild the pydantic-core schema for the model.
This may be necessary when one of the annotations is a ForwardRef which could not be resolved during the initial attempt to build the schema, and automatic rebuilding fails.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`_types_namespace` |  `MappingNamespace | None` |  The types namespace, defaults to `None`. |  `None`  
Returns:
Type | Description  
---|---  
Source code in `pydantic/main.py`
```

```
| ```
@classmethod
def model_rebuild(
  cls,
  *,
  force: bool = False,
  raise_errors: bool = True,
  _parent_namespace_depth: int = 2,
  _types_namespace: MappingNamespace | None = None,
) -> bool | None:
"""Try to rebuild the pydantic-core schema for the model.
  This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
  the initial attempt to build the schema, and automatic rebuilding fails.
  Args:
    force: Whether to force the rebuilding of the model schema, defaults to `False`.
    raise_errors: Whether to raise errors, defaults to `True`.
    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
    _types_namespace: The types namespace, defaults to `None`.
  Returns:
    Returns `None` if the schema is already "complete" and rebuilding was not required.
    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
  """
  if not force and cls.__pydantic_complete__:
    return None
  if '__pydantic_core_schema__' in cls.__dict__:
    delattr(cls, '__pydantic_core_schema__') # delete cached value to ensure full rebuild happens
  if _types_namespace is not None:
    rebuild_ns = _types_namespace
  elif _parent_namespace_depth > 0:
    rebuild_ns = _typing_extra.parent_frame_namespace(parent_depth=_parent_namespace_depth, force=True) or {}
  else:
    rebuild_ns = {}
  parent_ns = _model_construction.unpack_lenient_weakvaluedict(cls.__pydantic_parent_namespace__) or {}
  ns_resolver = _namespace_utils.NsResolver(
    parent_namespace={**rebuild_ns, **parent_ns},
  )
  # manually override defer_build so complete_model_class doesn't skip building the model again
  config = {**cls.model_config, 'defer_build': False}
  return _model_construction.complete_model_class(
    cls,
    cls.__name__,
    _config.ConfigWrapper(config, check=False),
    raise_errors=raise_errors,
    ns_resolver=ns_resolver,
  )

```
  
---|---  
```
model_validate(
  *,
) -> Self

```

Validate a pydantic model instance.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
Raises:
Type | Description  
---|---  
`ValidationError` |  If the object could not be validated.  
Returns:
Type | Description  
---|---  
`Self` |  The validated model instance.  
Source code in `pydantic/main.py`
```

```
| ```
@classmethod
def model_validate(
  cls,
  obj: Any,
  *,
  strict: bool | None = None,
  from_attributes: bool | None = None,
  context: Any | None = None,
) -> Self:
"""Validate a pydantic model instance.
  Args:
    obj: The object to validate.
    strict: Whether to enforce types strictly.
    from_attributes: Whether to extract data from object attributes.
    context: Additional context to pass to the validator.
  Raises:
    ValidationError: If the object could not be validated.
  Returns:
    The validated model instance.
  """
  # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks
  __tracebackhide__ = True
  return cls.__pydantic_validator__.validate_python(
    obj, strict=strict, from_attributes=from_attributes, context=context
  )

```
  
---|---  
```
model_validate_json(
  *,
) -> Self

```

Usage Documentation
Validate the given JSON data against the Pydantic model.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
Returns:
Type | Description  
---|---  
`Self` |  The validated Pydantic model.  
Raises:
Type | Description  
---|---  
`ValidationError` |  If `json_data` is not a JSON string or the object could not be validated.  
Source code in `pydantic/main.py`
```

```
| ```
@classmethod
def model_validate_json(
  cls,
  json_data: str | bytes | bytearray,
  *,
  strict: bool | None = None,
  context: Any | None = None,
) -> Self:
  Validate the given JSON data against the Pydantic model.
  Args:
    json_data: The JSON data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.
  Returns:
    The validated Pydantic model.
  Raises:
    ValidationError: If `json_data` is not a JSON string or the object could not be validated.
  """
  # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks
  __tracebackhide__ = True
  return cls.__pydantic_validator__.validate_json(json_data, strict=strict, context=context)

```
  
---|---  
```
model_validate_strings(
  *,
) -> Self

```

Validate the given object with string data against the Pydantic model.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
Returns:
Type | Description  
---|---  
`Self` |  The validated Pydantic model.  
Source code in `pydantic/main.py`
```

```
| ```
@classmethod
def model_validate_strings(
  cls,
  obj: Any,
  *,
  strict: bool | None = None,
  context: Any | None = None,
) -> Self:
"""Validate the given object with string data against the Pydantic model.
  Args:
    obj: The object containing string data to validate.
    strict: Whether to enforce types strictly.
    context: Extra variables to pass to the validator.
  Returns:
    The validated Pydantic model.
  """
  # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks
  __tracebackhide__ = True
  return cls.__pydantic_validator__.validate_strings(obj, strict=strict, context=context)

```
  
---|---  
```
copy(
  *,
  include: (
    AbstractSetIntStr | MappingIntStrAny | None
  ) = None,
  exclude: (
    AbstractSetIntStr | MappingIntStrAny | None
  ) = None,
) -> Self

```

Returns a copy of the model.
Deprecated
This method is now deprecated; use `model_copy` instead.
If you need `include` or `exclude`, use:
```
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)

```

Parameters:
Name | Type | Description | Default  
---|---|---|---  
`include` |  `AbstractSetIntStr | MappingIntStrAny | None` |  Optional set or mapping specifying which fields to include in the copied model. |  `None`  
`exclude` |  `AbstractSetIntStr | MappingIntStrAny | None` |  Optional set or mapping specifying which fields to exclude in the copied model. |  `None`  
Returns:
Type | Description  
---|---  
`Self` |  A copy of the model with included, excluded and updated fields as specified.  
Source code in `pydantic/main.py`
```

```
| ```
@typing_extensions.deprecated(
  'The `copy` method is deprecated; use `model_copy` instead. '
  'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',
  category=None,
)
def copy(
  self,
  *,
  include: AbstractSetIntStr | MappingIntStrAny | None = None,
  exclude: AbstractSetIntStr | MappingIntStrAny | None = None,
  update: Dict[str, Any] | None = None, # noqa UP006
  deep: bool = False,
) -> Self: # pragma: no cover
"""Returns a copy of the model.
  !!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.
  If you need `include` or `exclude`, use:
  ```python {test="skip" lint="skip"}
  data = self.model_dump(include=include, exclude=exclude, round_trip=True)
  data = {**data, **(update or {})}
  copied = self.model_validate(data)
  ```
  Args:
    include: Optional set or mapping specifying which fields to include in the copied model.
    exclude: Optional set or mapping specifying which fields to exclude in the copied model.
    update: Optional dictionary of field-value pairs to override field values in the copied model.
    deep: If True, the values of fields that are Pydantic models will be deep-copied.
  Returns:
    A copy of the model with included, excluded and updated fields as specified.
  """
  warnings.warn(
    'The `copy` method is deprecated; use `model_copy` instead. '
    'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',
    category=PydanticDeprecatedSince20,
    stacklevel=2,
  )
  from .deprecated import copy_internals
  values = dict(
    copy_internals._iter(
      self, to_dict=False, by_alias=False, include=include, exclude=exclude, exclude_unset=False
    ),
    **(update or {}),
  )
  if self.__pydantic_private__ is None:
    private = None
  else:
    private = {k: v for k, v in self.__pydantic_private__.items() if v is not PydanticUndefined}
  if self.__pydantic_extra__ is None:
    extra: dict[str, Any] | None = None
  else:
    extra = self.__pydantic_extra__.copy()
    for k in list(self.__pydantic_extra__):
      if k not in values: # k was in the exclude
        extra.pop(k)
    for k in list(values):
      if k in self.__pydantic_extra__: # k must have come from extra
        extra[k] = values.pop(k)
  # new `__pydantic_fields_set__` can have unset optional fields with a set value in `update` kwarg
  if update:
    fields_set = self.__pydantic_fields_set__ | update.keys()
  else:
    fields_set = set(self.__pydantic_fields_set__)
  # removing excluded fields from `__pydantic_fields_set__`
  if exclude:
    fields_set -= set(exclude)
  return copy_internals._copy_and_set_values(self, values, fields_set, extra, private, deep=deep)

```
  
---|---  
```
create_model(
  /,
  *,
  __base__: (
  ) = None,
  __validators__: (
  ) = None,

```

Usage Documentation
Parameters:
Name | Type | Description | Default  
---|---|---|---  
Returns:
Type | Description  
---|---  
Raises:
Type | Description  
---|---  
Source code in `pydantic/main.py`
```

```
| ```
def create_model( # noqa: C901
  model_name: str,
  /,
  *,
  __config__: ConfigDict | None = None,
  __doc__: str | None = None,
  __base__: type[ModelT] | tuple[type[ModelT], ...] | None = None,
  __module__: str | None = None,
  __validators__: dict[str, Callable[..., Any]] | None = None,
  __cls_kwargs__: dict[str, Any] | None = None,
  __slots__: tuple[str, ...] | None = None,
  **field_definitions: Any,
) -> type[ModelT]:
  Dynamically creates and returns a new Pydantic model, in other words, `create_model` dynamically creates a
  subclass of [`BaseModel`][pydantic.BaseModel].
  Args:
    model_name: The name of the newly created model.
    __config__: The configuration of the new model.
    __doc__: The docstring of the new model.
    __base__: The base class or classes for the new model.
    __module__: The name of the module that the model belongs to;
      if `None`, the value is taken from `sys._getframe(1)`
    __validators__: A dictionary of methods that validate fields. The keys are the names of the validation methods to
      be added to the model, and the values are the validation methods themselves. You can read more about functional
    __cls_kwargs__: A dictionary of keyword arguments for class creation, such as `metaclass`.
    __slots__: Deprecated. Should not be passed to `create_model`.
    **field_definitions: Attributes of the new model. They should be passed in the format:
      `<name>=(<type>, <default value>)`, `<name>=(<type>, <FieldInfo>)`, or `typing.Annotated[<type>, <FieldInfo>]`.
      Any additional metadata in `typing.Annotated[<type>, <FieldInfo>, ...]` will be ignored.
      Note, `FieldInfo` instances should be created via `pydantic.Field(...)`.
      Initializing `FieldInfo` instances directly is not supported.
  Returns:
    The new [model][pydantic.BaseModel].
  Raises:
    PydanticUserError: If `__base__` and `__config__` are both passed.
  """
  if __slots__ is not None:
    # __slots__ will be ignored from here on
    warnings.warn('__slots__ should not be passed to create_model', RuntimeWarning)
  if __base__ is not None:
    if __config__ is not None:
      raise PydanticUserError(
        'to avoid confusion `__config__` and `__base__` cannot be used together',
        code='create-model-config-base',
      )
    if not isinstance(__base__, tuple):
      __base__ = (__base__,)
  else:
    __base__ = (cast('type[ModelT]', BaseModel),)
  __cls_kwargs__ = __cls_kwargs__ or {}
  fields = {}
  annotations = {}
  for f_name, f_def in field_definitions.items():
    if not _fields.is_valid_field_name(f_name):
      warnings.warn(f'fields may not start with an underscore, ignoring "{f_name}"', RuntimeWarning)
    if isinstance(f_def, tuple):
      f_def = cast('tuple[str, Any]', f_def)
      try:
        f_annotation, f_value = f_def
      except ValueError as e:
        raise PydanticUserError(
          'Field definitions should be a `(<type>, <default>)`.',
          code='create-model-field-definitions',
        ) from e
    elif _typing_extra.is_annotated(f_def):
      (f_annotation, f_value, *_) = typing_extensions.get_args(
        f_def
      FieldInfo = _import_utils.import_cached_field_info()
      if not isinstance(f_value, FieldInfo):
        raise PydanticUserError(
          'Field definitions should be a Annotated[<type>, <FieldInfo>]',
          code='create-model-field-definitions',
        )
    else:
      f_annotation, f_value = None, f_def
    if f_annotation:
      annotations[f_name] = f_annotation
    fields[f_name] = f_value
  if __module__ is None:
    f = sys._getframe(1)
    __module__ = f.f_globals['__name__']
  namespace: dict[str, Any] = {'__annotations__': annotations, '__module__': __module__}
  if __doc__:
    namespace.update({'__doc__': __doc__})
  if __validators__:
    namespace.update(__validators__)
  namespace.update(fields)
  if __config__:
    namespace['model_config'] = _config.ConfigWrapper(__config__).config_dict
  resolved_bases = types.resolve_bases(__base__)
  meta, ns, kwds = types.prepare_class(model_name, resolved_bases, kwds=__cls_kwargs__)
  if resolved_bases is not __base__:
    ns['__orig_bases__'] = __base__
  namespace.update(ns)
  return meta(
    model_name,
    resolved_bases,
    namespace,
    __pydantic_reset_parent_namespace__=False,
    _create_model_module=__module__,
    **kwds,
  )

```
  
---|---  
Was this page helpful? 
Thanks for your feedback! 
Thanks for your feedback! 
Back to top 

---

<a id='latest_api_config'></a>

## latest api config

Pydantic 
dev


Configuration 
Initializing search 


  * Get Started  Get Started 
  * Concepts  Concepts 
  * API Documentation  API Documentation 
    * Pydantic  Pydantic 
    * Pydantic Core  Pydantic Core 
    * Pydantic Extra Types  Pydantic Extra Types 
  * Internals  Internals 
  * Examples  Examples 
  * Error Messages  Error Messages 
  * Integrations  Integrations 
    * Dev Tools  Dev Tools 
    * Production Tools  Production Tools 


Page contents 


# Configuration
Configuration for Pydantic models.
Bases: `TypedDict`
A TypedDict for configuring Pydantic behaviour.
```

```

The title for the generated JSON schema, defaults to the model's name
```

```

A callable that takes a model class and returns the title for it. Defaults to `None`.
```
field_title_generator: (
  | None
)

```

A callable that takes a field's name and info and returns title for it. Defaults to `None`.
```

```

Whether to convert all characters to lowercase for str types. Defaults to `False`.
```

```

Whether to convert all characters to uppercase for str types. Defaults to `False`.
```

```

Whether to strip leading and trailing whitespace for str types.
```

```

The minimum length for str types. Defaults to `None`.
```

```

The maximum length for str types. Defaults to `None`.
```

```

Whether to ignore, allow, or forbid extra attributes during model initialization. Defaults to `'ignore'`.
You can configure how pydantic handles the attributes that are not defined in the model:
  * `allow` - Allow any extra attributes.
  * `forbid` - Forbid any extra attributes.
  * `ignore` - Ignore any extra attributes.


```
from pydantic import BaseModel, ConfigDict
class User(BaseModel):
  name: str
print(user)
#> name='John Doe'

```

Instead, with `extra='allow'`, the `age` argument is included:
```
from pydantic import BaseModel, ConfigDict
class User(BaseModel):
  model_config = ConfigDict(extra='allow')
  name: str
print(user)
#> name='John Doe' age=20

```

With `extra='forbid'`, an error is raised:
```
from pydantic import BaseModel, ConfigDict, ValidationError
class User(BaseModel):
  model_config = ConfigDict(extra='forbid')
  name: str
try:
  User(name='John Doe', age=20)
except ValidationError as e:
  print(e)
'''
  1 validation error for User
  age
   Extra inputs are not permitted [type=extra_forbidden, input_value=20, input_type=int]
  '''

```

```

```

Whether models are faux-immutable, i.e. whether `__setattr__` is allowed, and also generates a `__hash__()` method for the model. This makes instances of the model potentially hashable if all the attributes are hashable. Defaults to `False`.
Note
On V1, the inverse of this setting was called `allow_mutation`, and was `True` by default.
```

```

Whether an aliased field may be populated by its name as given by the model attribute, as well as the alias. Defaults to `False`.
Note
The name of this configuration setting was changed in **v2.0** from `allow_population_by_field_name` to `populate_by_name`.
```
from pydantic import BaseModel, ConfigDict, Field
class User(BaseModel):
  model_config = ConfigDict(populate_by_name=True)
  age: int
print(user)
#> name='John Doe' age=20
print(user)
#> name='John Doe' age=20

```

```

```

Whether to populate models with the `value` property of enums, rather than the raw enum. This may be useful if you want to serialize `model.model_dump()` later. Defaults to `False`.
Note
If you have an `Optional[Enum]` value that you set a default for, you need to use `validate_default=True` for said Field to ensure that the `use_enum_values` flag takes effect on the default, as extracting an enum's value occurs during validation, not serialization.
```
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
class SomeEnum(Enum):
  FOO = 'foo'
  BAR = 'bar'
  BAZ = 'baz'
class SomeModel(BaseModel):
  model_config = ConfigDict(use_enum_values=True)
  some_enum: SomeEnum
  another_enum: Optional[SomeEnum] = Field(
    default=SomeEnum.FOO, validate_default=True
  )
model1 = SomeModel(some_enum=SomeEnum.BAR)
print(model1.model_dump())
#> {'some_enum': 'bar', 'another_enum': 'foo'}
model2 = SomeModel(some_enum=SomeEnum.BAR, another_enum=SomeEnum.BAZ)
print(model2.model_dump())
#> {'some_enum': 'bar', 'another_enum': 'baz'}

```

```

```

Whether to validate the data when the model is changed. Defaults to `False`.
The default behavior of Pydantic is to validate the data when the model is created.
In case the user changes the data after the model is created, the model is _not_ revalidated.
```
from pydantic import BaseModel
class User(BaseModel):
  name: str
print(user)
#> name='John Doe'
print(user)
#> name=123

```

  1. The validation does not happen when the data is changed.


In case you want to revalidate the model when the data is changed, you can use `validate_assignment=True`:
```
from pydantic import BaseModel, ValidationError
  name: str
print(user)
#> name='John Doe'
try:
except ValidationError as e:
  print(e)
'''
  1 validation error for User
  name
   Input should be a valid string [type=string_type, input_value=123, input_type=int]
  '''

```

```

```

Whether arbitrary types are allowed for field types. Defaults to `False`.
```
from pydantic import BaseModel, ConfigDict, ValidationError
# This is not a pydantic model, it's an arbitrary class
class Pet:
  def __init__(self, name: str):
    self.name = name
class Model(BaseModel):
  model_config = ConfigDict(arbitrary_types_allowed=True)
  pet: Pet
  owner: str
pet = Pet(name='Hedwig')
# A simple check of instance type is used to validate the data
model = Model(owner='Harry', pet=pet)
print(model)
#> pet=<__main__.Pet object at 0x0123456789ab> owner='Harry'
print(model.pet)
#> <__main__.Pet object at 0x0123456789ab>
print(model.pet.name)
#> Hedwig
print(type(model.pet))
#> <class '__main__.Pet'>
try:
  # If the value is not an instance of the type, it's invalid
  Model(owner='Harry', pet='Hedwig')
except ValidationError as e:
  print(e)
'''
  1 validation error for Model
  pet
   Input should be an instance of Pet [type=is_instance_of, input_value='Hedwig', input_type=str]
  '''
# Nothing in the instance of the arbitrary type is checked
# Here name probably should have been a str, but it's not validated
pet2 = Pet(name=42)
model2 = Model(owner='Harry', pet=pet2)
print(model2)
#> pet=<__main__.Pet object at 0x0123456789ab> owner='Harry'
print(model2.pet)
#> <__main__.Pet object at 0x0123456789ab>
print(model2.pet.name)
#> 42
print(type(model2.pet))
#> <class '__main__.Pet'>

```

```

```

Whether to build models and look up discriminators of tagged unions using python object attributes.
```

```

Whether to use the actual key provided in the data (e.g. alias) for error `loc`s rather than the field's name. Defaults to `True`.
```
alias_generator: (
)

```

If data source field names do not match your code style (e. g. CamelCase fields), you can automatically generate aliases using `alias_generator`. Here's an example with a basic callable:
```
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_pascal
class Voice(BaseModel):
  model_config = ConfigDict(alias_generator=to_pascal)
  name: str
  language_code: str
voice = Voice(Name='Filiz', LanguageCode='tr-TR')
print(voice.language_code)
#> tr-TR
print(voice.model_dump(by_alias=True))
#> {'Name': 'Filiz', 'LanguageCode': 'tr-TR'}

```

```
from pydantic import AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel, to_pascal
class Athlete(BaseModel):
  first_name: str
  last_name: str
  sport: str
  model_config = ConfigDict(
    alias_generator=AliasGenerator(
      validation_alias=to_camel,
      serialization_alias=to_pascal,
    )
  )
athlete = Athlete(firstName='John', lastName='Doe', sport='track')
print(athlete.model_dump(by_alias=True))
#> {'FirstName': 'John', 'LastName': 'Doe', 'Sport': 'track'}

```

Note
```

```

A tuple of types that may occur as values of class attributes without annotations. This is typically used for custom descriptors (classes that behave like `property`). If an attribute is set on a class without an annotation and has a type that is not in this tuple (or otherwise recognized by _pydantic_), an error will be raised. Defaults to `()`.
```

```

Whether to allow infinity (`+inf` an `-inf`) and NaN values to float and decimal fields. Defaults to `True`.
```
json_schema_extra: JsonDict | JsonSchemaExtraCallable | None

```

A dict or callable to provide extra JSON schema properties. Defaults to `None`.
```

```

A `dict` of custom JSON encoders for specific types. Defaults to `None`.
Deprecated
This config option is a carryover from v1. We originally planned to remove it in v2 but didn't have a 1:1 replacement so we are keeping it for now. It is still deprecated and will likely be removed in the future.
```

```

_(new in V2)_ If `True`, strict validation is applied to all fields on the model.
By default, Pydantic attempts to coerce values to the correct type, when possible.
There are situations in which you may want to disable this behavior, and instead raise an error if a value's type does not match the field's type annotation.
To configure strict mode for all fields on a model, you can set `strict=True` on the model.
```
from pydantic import BaseModel, ConfigDict
class Model(BaseModel):
  model_config = ConfigDict(strict=True)
  name: str
  age: int

```

```
revalidate_instances: Literal[
  "always", "never", "subclass-instances"
]

```

When and how to revalidate models and dataclasses during validation. Accepts the string values of `'never'`, `'always'` and `'subclass-instances'`. Defaults to `'never'`.
  * `'never'` will not revalidate models and dataclasses during validation
  * `'always'` will revalidate models and dataclasses during validation
  * `'subclass-instances'` will revalidate models and dataclasses during validation if the instance is a subclass of the model or dataclass


By default, model and dataclass instances are not revalidated during validation.
```
from typing import List
from pydantic import BaseModel
  hobbies: List[str]
class SubUser(User):
  sins: List[str]
class Transaction(BaseModel):
  user: User
my_user = User(hobbies=['reading'])
t = Transaction(user=my_user)
print(t)
#> user=User(hobbies=['reading'])
print(t)
#> user=User(hobbies=[1])
my_sub_user = SubUser(hobbies=['scuba diving'], sins=['lying'])
t = Transaction(user=my_sub_user)
print(t)
#> user=SubUser(hobbies=['scuba diving'], sins=['lying'])

```

If you want to revalidate instances during validation, you can set `revalidate_instances` to `'always'` in the model's config.
```
from typing import List
from pydantic import BaseModel, ValidationError
  hobbies: List[str]
class SubUser(User):
  sins: List[str]
class Transaction(BaseModel):
  user: User
my_user = User(hobbies=['reading'])
t = Transaction(user=my_user)
print(t)
#> user=User(hobbies=['reading'])
my_user.hobbies = [1]
try:
except ValidationError as e:
  print(e)
'''
  1 validation error for Transaction
  user.hobbies.0
   Input should be a valid string [type=string_type, input_value=1, input_type=int]
  '''
my_sub_user = SubUser(hobbies=['scuba diving'], sins=['lying'])
t = Transaction(user=my_sub_user)
#> user=User(hobbies=['scuba diving'])

```

It's also possible to set `revalidate_instances` to `'subclass-instances'` to only revalidate instances of subclasses of the model.
```
from typing import List
from pydantic import BaseModel
  hobbies: List[str]
class SubUser(User):
  sins: List[str]
class Transaction(BaseModel):
  user: User
my_user = User(hobbies=['reading'])
t = Transaction(user=my_user)
print(t)
#> user=User(hobbies=['reading'])
my_user.hobbies = [1]
print(t)
#> user=User(hobbies=[1])
my_sub_user = SubUser(hobbies=['scuba diving'], sins=['lying'])
t = Transaction(user=my_sub_user)
#> user=User(hobbies=['scuba diving'])

```

```
ser_json_timedelta: Literal['iso8601', 'float']

```

The format of JSON serialized timedeltas. Accepts the string values of `'iso8601'` and `'float'`. Defaults to `'iso8601'`.
  * `'iso8601'` will serialize timedeltas to ISO 8601 durations.
  * `'float'` will serialize timedeltas to the total number of seconds.


```
ser_json_bytes: Literal['utf8', 'base64', 'hex']

```

The encoding of JSON serialized bytes. Defaults to `'utf8'`. Set equal to `val_json_bytes` to get back an equal value after serialization round trip.
  * `'utf8'` will serialize bytes to UTF-8 strings.
  * `'base64'` will serialize bytes to URL safe base64 strings.
  * `'hex'` will serialize bytes to hexadecimal strings.


```
val_json_bytes: Literal['utf8', 'base64', 'hex']

```

The encoding of JSON serialized bytes to decode. Defaults to `'utf8'`. Set equal to `ser_json_bytes` to get back an equal value after serialization round trip.
  * `'utf8'` will deserialize UTF-8 strings to bytes.
  * `'base64'` will deserialize URL safe base64 strings to bytes.
  * `'hex'` will deserialize hexadecimal strings to bytes.


```
ser_json_inf_nan: Literal['null', 'constants', 'strings']

```

The encoding of JSON serialized infinity and NaN float values. Defaults to `'null'`.
  * `'null'` will serialize infinity and NaN values as `null`.
  * `'constants'` will serialize infinity and NaN values as `Infinity` and `NaN`.
  * `'strings'` will serialize infinity as string `"Infinity"` and NaN as string `"NaN"`.


```

```

Whether to validate default values during validation. Defaults to `False`.
```

```

Whether to validate the return value from call validators. Defaults to `False`.
```

```

A `tuple` of strings and/or patterns that prevent models from having fields with names that conflict with them. For strings, we match on a prefix basis. Ex, if 'dog' is in the protected namespace, 'dog_name' will be protected. For patterns, we match on the entire field name. Ex, if `re.compile(r'^dog$')` is in the protected namespace, 'dog' will be protected, but 'dog_name' will not be. Defaults to `('model_validate', 'model_dump',)`.
The reason we've selected these is to prevent collisions with other validation / dumping formats in the future - ex, `model_validate_{some_newly_supported_format}`.
Before v2.10, Pydantic used `('model_',)` as the default value for this setting to prevent collisions between model attributes and `BaseModel`'s own methods. This was changed in v2.10 given feedback that this restriction was limiting in AI and data science contexts, where it is common to have fields with names like `model_id`, `model_input`, `model_output`, etc.
```
import warnings
from pydantic import BaseModel
warnings.filterwarnings('error') # Raise warnings as errors
try:
  class Model(BaseModel):
    model_dump_something: str
except UserWarning as e:
  print(e)
'''
  Field "model_dump_something" in Model has conflict with protected namespace "model_dump".
  You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ('model_validate',)`.
  '''

```

You can customize this behavior using the `protected_namespaces` setting:
```
import re
import warnings
from pydantic import BaseModel, ConfigDict
with warnings.catch_warnings(record=True) as caught_warnings:
  warnings.simplefilter('always') # Catch all warnings
  class Model(BaseModel):
    safe_field: str
    also_protect_field: str
    protect_this: str
    model_config = ConfigDict(
      protected_namespaces=(
        'protect_me_',
        'also_protect_',
        re.compile('^protect_this$'),
      )
    )
for warning in caught_warnings:
  print(f'{warning.message}')
'''
  Field "also_protect_field" in Model has conflict with protected namespace "also_protect_".
  You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ('protect_me_', re.compile('^protect_this$'))`.
  Field "protect_this" in Model has conflict with protected namespace "re.compile('^protect_this$')".
  You may be able to resolve this warning by setting `model_config['protected_namespaces'] = ('protect_me_', 'also_protect_')`.
  '''

```

While Pydantic will only emit a warning when an item is in a protected namespace but does not actually have a collision, an error _is_ raised if there is an actual collision with an existing attribute:
```
from pydantic import BaseModel, ConfigDict
try:
  class Model(BaseModel):
    model_validate: str
    model_config = ConfigDict(protected_namespaces=('model_',))
except NameError as e:
  print(e)
'''
  Field "model_validate" conflicts with member <bound method BaseModel.model_validate of <class 'pydantic.main.BaseModel'>> of protected namespace "model_".
  '''

```

```

```

Whether to hide inputs when printing errors. Defaults to `False`.
Pydantic shows the input value and type when it raises `ValidationError` during the validation.
```
from pydantic import BaseModel, ValidationError
class Model(BaseModel):
  a: str
try:
  Model(a=123)
except ValidationError as e:
  print(e)
'''
  1 validation error for Model
  a
   Input should be a valid string [type=string_type, input_value=123, input_type=int]
  '''

```

You can hide the input value and type by setting the `hide_input_in_errors` config to `True`.
```
from pydantic import BaseModel, ConfigDict, ValidationError
class Model(BaseModel):
  a: str
  model_config = ConfigDict(hide_input_in_errors=True)
try:
  Model(a=123)
except ValidationError as e:
  print(e)
'''
  1 validation error for Model
  a
   Input should be a valid string [type=string_type]
  '''

```

```

```

Whether to defer model validator and serializer construction until the first model validation. Defaults to False.
Since v2.10, this setting also applies to pydantic dataclasses and TypeAdapter instances.
```

```

A `dict` of settings for plugins. Defaults to `None`.
```

```

Warning
`schema_generator` is deprecated in v2.10.
Prior to v2.10, this setting was advertised as highly subject to change. It's possible that this interface may once again become public once the internal core schema generation API is more stable, but that will likely come after significant performance improvements have been made.
```

```

Whether fields with default values should be marked as required in the serialization schema. Defaults to `False`.
This ensures that the serialization schema will reflect the fact a field with a default will always be present when serializing the model, even though it is not required for validation.
```
from pydantic import BaseModel, ConfigDict
class Model(BaseModel):
  a: str = 'a'
  model_config = ConfigDict(json_schema_serialization_defaults_required=True)
print(Model.model_json_schema(mode='validation'))
'''
{
  'properties': {'a': {'default': 'a', 'title': 'A', 'type': 'string'}},
  'title': 'Model',
  'type': 'object',
}
'''
print(Model.model_json_schema(mode='serialization'))
'''
{
  'properties': {'a': {'default': 'a', 'title': 'A', 'type': 'string'}},
  'required': ['a'],
  'title': 'Model',
  'type': 'object',
}
'''

```

```
json_schema_mode_override: Literal[
  "validation", "serialization", None
]

```

If not `None`, the specified mode will be used to generate the JSON schema regardless of what `mode` was passed to the function call. Defaults to `None`.
This provides a way to force the JSON schema generation to reflect a specific mode, e.g., to always use the validation schema.
It can be useful when using frameworks (such as FastAPI) that may generate different schemas for validation and serialization that must both be referenced from the same schema; when this happens, we automatically append `-Input` to the definition reference for the validation schema and `-Output` to the definition reference for the serialization schema. By specifying a `json_schema_mode_override` though, this prevents the conflict between the validation and serialization schemas (since both will use the specified schema), and so prevents the suffixes from being added to the definition references.
```
from pydantic import BaseModel, ConfigDict, Json
class Model(BaseModel):
  a: Json[int] # requires a string to validate, but will dump an int
print(Model.model_json_schema(mode='serialization'))
'''
{
  'properties': {'a': {'title': 'A', 'type': 'integer'}},
  'required': ['a'],
  'title': 'Model',
  'type': 'object',
}
'''
class ForceInputModel(Model):
  # the following ensures that even with mode='serialization', we
  # will get the schema that would be generated for validation.
  model_config = ConfigDict(json_schema_mode_override='validation')
print(ForceInputModel.model_json_schema(mode='serialization'))
'''
{
  'properties': {
    'a': {
      'contentMediaType': 'application/json',
      'contentSchema': {'type': 'integer'},
      'title': 'A',
      'type': 'string',
    }
  },
  'required': ['a'],
  'title': 'ForceInputModel',
  'type': 'object',
}
'''

```

```

```

If `True`, enables automatic coercion of any `Number` type to `str` in "lax" (non-strict) mode. Defaults to `False`.
Pydantic doesn't allow number types (`int`, `float`, `Decimal`) to be coerced as type `str` by default.
```
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, ValidationError
class Model(BaseModel):
  value: str
try:
  print(Model(value=42))
except ValidationError as e:
  print(e)
'''
  1 validation error for Model
  value
   Input should be a valid string [type=string_type, input_value=42, input_type=int]
  '''
class Model(BaseModel):
  model_config = ConfigDict(coerce_numbers_to_str=True)
  value: str
repr(Model(value=42).value)
#> "42"
repr(Model(value=42.13).value)
#> "42.13"
repr(Model(value=Decimal('42.13')).value)
#> "42.13"

```

```
regex_engine: Literal['rust-regex', 'python-re']

```

The regex engine to be used for pattern validation. Defaults to `'rust-regex'`.


Note
If you use a compiled regex pattern, the python-re engine will be used regardless of this setting. This is so that flags such as `re.IGNORECASE` are respected.
```
from pydantic import BaseModel, ConfigDict, Field, ValidationError
class Model(BaseModel):
  model_config = ConfigDict(regex_engine='python-re')
  value: str = Field(pattern=r'^abc(?=def)')
print(Model(value='abcdef').value)
#> abcdef
try:
  print(Model(value='abxyzcdef'))
except ValidationError as e:
  print(e)
'''
  1 validation error for Model
  value
   String should match pattern '^abc(?=def)' [type=string_pattern_mismatch, input_value='abxyzcdef', input_type=str]
  '''

```

```

```

If `True`, Python exceptions that were part of a validation failure will be shown as an exception group as a cause. Can be useful for debugging. Defaults to `False`.
Note
Python 3.10 and older don't support exception groups natively. <=3.10, backport must be installed: `pip install exceptiongroup`.
Note
The structure of validation errors are likely to change in future Pydantic versions. Pydantic offers no guarantees about their structure. Should be used for visual traceback debugging only.
```

```

Whether docstrings of attributes (bare string literals immediately following the attribute declaration) should be used for field descriptions. Defaults to `False`.
Available in Pydantic v2.7+.
```
from pydantic import BaseModel, ConfigDict, Field

class Model(BaseModel):
  model_config = ConfigDict(use_attribute_docstrings=True)
  x: str
"""
  Example of an attribute docstring
  """
  y: int = Field(description="Description in Field")
"""
  Description in Field overrides attribute docstring
  """

print(Model.model_fields["x"].description)
# > Example of an attribute docstring
print(Model.model_fields["y"].description)
# > Description in Field

```

This requires the source code of the class to be available at runtime. 
Usage with `TypedDict`
Due to current limitations, attribute docstrings detection may not work as expected when using `TypedDict` (in particular when multiple `TypedDict` classes have the same name in the same source file). The behavior can be different depending on the Python version used.
```

```

Whether to cache strings to avoid constructing new Python objects. Defaults to True.
Enabling this setting should significantly improve validation performance while increasing memory usage slightly.
  * `True` or `'all'` (the default): cache all strings
  * `'keys'`: cache only dictionary keys
  * `False` or `'none'`: no caching


Note
`True` or `'all'` is required to cache strings during general validation because validators don't know if they're in a key or a value.
Tip
If repeated strings are rare, it's recommended to use `'keys'` or `'none'` to reduce memory usage, as the performance difference is minimal if repeated strings are rare.
```
with_config(

```

Usage Documentation
Although the configuration can be set using the `__pydantic_config__` attribute, it does not play well with type checkers, especially with `TypedDict`.
Usage
```
from typing_extensions import TypedDict
from pydantic import ConfigDict, TypeAdapter, with_config
@with_config(ConfigDict(str_to_lower=True))
class Model(TypedDict):
  x: str
ta = TypeAdapter(Model)
print(ta.validate_python({'x': 'ABC'}))
#> {'x': 'abc'}

```

Source code in `pydantic/config.py`
```

```
| ```
def with_config(config: ConfigDict) -> Callable[[_TypeT], _TypeT]:
  A convenience decorator to set a [Pydantic configuration](config.md) on a `TypedDict` or a `dataclass` from the standard library.
  Although the configuration can be set using the `__pydantic_config__` attribute, it does not play well with type checkers,
  especially with `TypedDict`.
  !!! example "Usage"
```python
    from typing_extensions import TypedDict
    from pydantic import ConfigDict, TypeAdapter, with_config
    @with_config(ConfigDict(str_to_lower=True))
    class Model(TypedDict):
      x: str
    ta = TypeAdapter(Model)
    print(ta.validate_python({'x': 'ABC'}))
    #> {'x': 'abc'}
```
  """
  def inner(class_: _TypeT, /) -> _TypeT:
    # Ideally, we would check for `class_` to either be a `TypedDict` or a stdlib dataclass.
    # However, the `@with_config` decorator can be applied *after* `@dataclass`. To avoid
    # common mistakes, we at least check for `class_` to not be a Pydantic model.
    from ._internal._utils import is_model_class
    if is_model_class(class_):
      raise PydanticUserError(
        f'Cannot use `with_config` on {class_.__name__} as it is a Pydantic model',
        code='with-config-on-model',
      )
    class_.__pydantic_config__ = config
    return class_
  return inner

```
  
---|---  
```
ExtraValues = Literal['allow', 'ignore', 'forbid']

```

Alias generators for converting between different capitalization conventions.
```

```

Convert a snake_case string to PascalCase.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
Returns:
Type | Description  
---|---  
Source code in `pydantic/alias_generators.py`
```

```
| ```
def to_pascal(snake: str) -> str:
"""Convert a snake_case string to PascalCase.
  Args:
    snake: The string to convert.
  Returns:
    The PascalCase string.
  """
  camel = snake.title()
  return re.sub('([0-9A-Za-z])_(?=[0-9A-Z])', lambda m: m.group(1), camel)

```
  
---|---  
```

```

Convert a snake_case string to camelCase.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
Returns:
Type | Description  
---|---  
Source code in `pydantic/alias_generators.py`
```

```
| ```
def to_camel(snake: str) -> str:
"""Convert a snake_case string to camelCase.
  Args:
    snake: The string to convert.
  Returns:
    The converted camelCase string.
  """
  # If the string is already in camelCase and does not contain a digit followed
  # by a lowercase letter, return it as it is
  if re.match('^[a-z]+[A-Za-z0-9]*$', snake) and not re.search(r'\d[a-z]', snake):
    return snake
  camel = to_pascal(snake)
  return re.sub('(^_*[A-Z])', lambda m: m.group(1).lower(), camel)

```
  
---|---  
```

```

Convert a PascalCase, camelCase, or kebab-case string to snake_case.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
Returns:
Type | Description  
---|---  
Source code in `pydantic/alias_generators.py`
```

```
| ```
def to_snake(camel: str) -> str:
"""Convert a PascalCase, camelCase, or kebab-case string to snake_case.
  Args:
    camel: The string to convert.
  Returns:
    The converted string in snake_case.
  """
  # Handle the sequence of uppercase letters followed by a lowercase letter
  snake = re.sub(r'([A-Z]+)([A-Z][a-z])', lambda m: f'{m.group(1)}_{m.group(2)}', camel)
  # Insert an underscore between a lowercase letter and an uppercase letter
  snake = re.sub(r'([a-z])([A-Z])', lambda m: f'{m.group(1)}_{m.group(2)}', snake)
  # Insert an underscore between a digit and an uppercase letter
  snake = re.sub(r'([0-9])([A-Z])', lambda m: f'{m.group(1)}_{m.group(2)}', snake)
  # Insert an underscore between a lowercase letter and a digit
  snake = re.sub(r'([a-z])([0-9])', lambda m: f'{m.group(1)}_{m.group(2)}', snake)
  # Replace hyphens with underscores to handle kebab-case
  snake = snake.replace('-', '_')
  return snake.lower()

```
  
---|---  
Was this page helpful? 
Thanks for your feedback! 
Thanks for your feedback! 
Back to top 

---

<a id='latest_api_dataclasses'></a>

## latest api dataclasses

Pydantic 
dev


Pydantic Dataclasses 
Initializing search 


  * Get Started  Get Started 
  * Concepts  Concepts 
  * API Documentation  API Documentation 
    * Pydantic  Pydantic 
    * Pydantic Core  Pydantic Core 
    * Pydantic Extra Types  Pydantic Extra Types 
  * Internals  Internals 
  * Examples  Examples 
  * Error Messages  Error Messages 
  * Integrations  Integrations 
    * Dev Tools  Dev Tools 
    * Production Tools  Production Tools 


Page contents 


# Pydantic Dataclasses
Provide an enhanced dataclass that performs validation.
```
dataclass(
  *,
  init: Literal[False] = False,
) -> (
)

```

Usage Documentation
A decorator used to create a Pydantic-enhanced dataclass, similar to the standard Python `dataclass`, but with added validation.
This function should be used similarly to `dataclasses.dataclass`.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`init` |  `Literal[False]` |  Included for signature compatibility with `dataclasses.dataclass`, and is passed through to `dataclasses.dataclass` when appropriate. If specified, must be set to `False`, as pydantic inserts its own `__init__` function. |  `False`  
Returns:
Type | Description  
---|---  
Raises:
Type | Description  
---|---  
Source code in `pydantic/dataclasses.py`
```
 
```
| ```
@dataclass_transform(field_specifiers=(dataclasses.field, Field, PrivateAttr))
def dataclass(
  _cls: type[_T] | None = None,
  *,
  init: Literal[False] = False,
  repr: bool = True,
  eq: bool = True,
  order: bool = False,
  unsafe_hash: bool = False,
  frozen: bool | None = None,
  config: ConfigDict | type[object] | None = None,
  validate_on_init: bool | None = None,
  kw_only: bool = False,
  slots: bool = False,
) -> Callable[[type[_T]], type[PydanticDataclass]] | type[PydanticDataclass]:
  A decorator used to create a Pydantic-enhanced dataclass, similar to the standard Python `dataclass`,
  but with added validation.
  This function should be used similarly to `dataclasses.dataclass`.
  Args:
    _cls: The target `dataclass`.
    init: Included for signature compatibility with `dataclasses.dataclass`, and is passed through to
      `dataclasses.dataclass` when appropriate. If specified, must be set to `False`, as pydantic inserts its
      own `__init__` function.
    repr: A boolean indicating whether to include the field in the `__repr__` output.
    eq: Determines if a `__eq__` method should be generated for the class.
    order: Determines if comparison magic methods should be generated, such as `__lt__`, but not `__eq__`.
    unsafe_hash: Determines if a `__hash__` method should be included in the class, as in `dataclasses.dataclass`.
    frozen: Determines if the generated class should be a 'frozen' `dataclass`, which does not allow its
      attributes to be modified after it has been initialized. If not set, the value from the provided `config` argument will be used (and will default to `False` otherwise).
    config: The Pydantic config to use for the `dataclass`.
    validate_on_init: A deprecated parameter included for backwards compatibility; in V2, all Pydantic dataclasses
      are validated on init.
    kw_only: Determines if `__init__` method parameters must be specified by keyword only. Defaults to `False`.
    slots: Determines if the generated class should be a 'slots' `dataclass`, which does not allow the addition of
      new attributes after instantiation.
  Returns:
    A decorator that accepts a class as its argument and returns a Pydantic `dataclass`.
  Raises:
    AssertionError: Raised if `init` is not `False` or `validate_on_init` is `False`.
  """
  assert init is False, 'pydantic.dataclasses.dataclass only supports init=False'
  assert validate_on_init is not False, 'validate_on_init=False is no longer supported'
  if sys.version_info >= (3, 10):
    kwargs = {'kw_only': kw_only, 'slots': slots}
  else:
    kwargs = {}
  def make_pydantic_fields_compatible(cls: type[Any]) -> None:
"""Make sure that stdlib `dataclasses` understands `Field` kwargs like `kw_only`
    To do that, we simply change
     `x: int = pydantic.Field(..., kw_only=True)`
    into
     `x: int = dataclasses.field(default=pydantic.Field(..., kw_only=True), kw_only=True)`
    """
    for annotation_cls in cls.__mro__:
      # In Python < 3.9, `__annotations__` might not be present if there are no fields.
      # we therefore need to use `getattr` to avoid an `AttributeError`.
      annotations = getattr(annotation_cls, '__annotations__', [])
      for field_name in annotations:
        field_value = getattr(cls, field_name, None)
        # Process only if this is an instance of `FieldInfo`.
        if not isinstance(field_value, FieldInfo):
          continue
        # Initialize arguments for the standard `dataclasses.field`.
        field_args: dict = {'default': field_value}
        # Handle `kw_only` for Python 3.10+
        if sys.version_info >= (3, 10) and field_value.kw_only:
          field_args['kw_only'] = True
        # Set `repr` attribute if it's explicitly specified to be not `True`.
        if field_value.repr is not True:
          field_args['repr'] = field_value.repr
        setattr(cls, field_name, dataclasses.field(**field_args))
        # In Python 3.8, dataclasses checks cls.__dict__['__annotations__'] for annotations,
        # so we must make sure it's initialized before we add to it.
        if cls.__dict__.get('__annotations__') is None:
          cls.__annotations__ = {}
        cls.__annotations__[field_name] = annotations[field_name]
  def create_dataclass(cls: type[Any]) -> type[PydanticDataclass]:
"""Create a Pydantic dataclass from a regular dataclass.
    Args:
      cls: The class to create the Pydantic dataclass from.
    Returns:
      A Pydantic dataclass.
    """
    from ._internal._utils import is_model_class
    if is_model_class(cls):
      raise PydanticUserError(
        f'Cannot create a Pydantic dataclass from {cls.__name__} as it is already a Pydantic model',
        code='dataclass-on-model',
      )
    original_cls = cls
    # we warn on conflicting config specifications, but only if the class doesn't have a dataclass base
    # because a dataclass base might provide a __pydantic_config__ attribute that we don't want to warn about
    has_dataclass_base = any(dataclasses.is_dataclass(base) for base in cls.__bases__)
    if not has_dataclass_base and config is not None and hasattr(cls, '__pydantic_config__'):
      warn(
        f'`config` is set via both the `dataclass` decorator and `__pydantic_config__` for dataclass {cls.__name__}. '
        f'The `config` specification from `dataclass` decorator will take priority.',
        category=UserWarning,
        stacklevel=2,
      )
    # if config is not explicitly provided, try to read it from the type
    config_dict = config if config is not None else getattr(cls, '__pydantic_config__', None)
    config_wrapper = _config.ConfigWrapper(config_dict)
    decorators = _decorators.DecoratorInfos.build(cls)
    # Keep track of the original __doc__ so that we can restore it after applying the dataclasses decorator
    # Otherwise, classes with no __doc__ will have their signature added into the JSON schema description,
    # since dataclasses.dataclass will set this as the __doc__
    original_doc = cls.__doc__
    if _pydantic_dataclasses.is_builtin_dataclass(cls):
      # Don't preserve the docstring for vanilla dataclasses, as it may include the signature
      # This matches v1 behavior, and there was an explicit test for it
      original_doc = None
      # We don't want to add validation to the existing std lib dataclass, so we will subclass it
      #  If the class is generic, we need to make sure the subclass also inherits from Generic
      #  with all the same parameters.
      bases = (cls,)
      if issubclass(cls, Generic):
        generic_base = Generic[cls.__parameters__] # type: ignore
        bases = bases + (generic_base,)
      cls = types.new_class(cls.__name__, bases)
    make_pydantic_fields_compatible(cls)
    # Respect frozen setting from dataclass constructor and fallback to config setting if not provided
    if frozen is not None:
      frozen_ = frozen
      if config_wrapper.frozen:
        # It's not recommended to define both, as the setting from the dataclass decorator will take priority.
        warn(
          f'`frozen` is set via both the `dataclass` decorator and `config` for dataclass {cls.__name__!r}.'
          'This is not recommended. The `frozen` specification on `dataclass` will take priority.',
          category=UserWarning,
          stacklevel=2,
        )
    else:
      frozen_ = config_wrapper.frozen or False
    cls = dataclasses.dataclass( # type: ignore[call-overload]
      cls,
      # the value of init here doesn't affect anything except that it makes it easier to generate a signature
      init=True,
      repr=repr,
      eq=eq,
      order=order,
      unsafe_hash=unsafe_hash,
      frozen=frozen_,
      **kwargs,
    )
    cls.__pydantic_decorators__ = decorators # type: ignore
    cls.__doc__ = original_doc
    cls.__module__ = original_cls.__module__
    cls.__qualname__ = original_cls.__qualname__
    cls.__pydantic_complete__ = False # `complete_dataclass` will set it to `True` if successful.
    # TODO `parent_namespace` is currently None, but we could do the same thing as Pydantic models:
    # fetch the parent ns using `parent_frame_namespace` (if the dataclass was defined in a function),
    # and possibly cache it (see the `__pydantic_parent_namespace__` logic for models).
    _pydantic_dataclasses.complete_dataclass(cls, config_wrapper, raise_errors=False)
    return cls
  return create_dataclass if _cls is None else create_dataclass(_cls)

```
  
---|---  
```
rebuild_dataclass(
  *,
  _types_namespace: MappingNamespace | None = None

```

Try to rebuild the pydantic-core schema for the dataclass.
This may be necessary when one of the annotations is a ForwardRef which could not be resolved during the initial attempt to build the schema, and automatic rebuilding fails.
This is analogous to `BaseModel.model_rebuild`.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
`_types_namespace` |  `MappingNamespace | None` |  The types namespace, defaults to `None`. |  `None`  
Returns:
Type | Description  
---|---  
Source code in `pydantic/dataclasses.py`
```

```
| ```
def rebuild_dataclass(
  cls: type[PydanticDataclass],
  *,
  force: bool = False,
  raise_errors: bool = True,
  _parent_namespace_depth: int = 2,
  _types_namespace: MappingNamespace | None = None,
) -> bool | None:
"""Try to rebuild the pydantic-core schema for the dataclass.
  This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
  the initial attempt to build the schema, and automatic rebuilding fails.
  This is analogous to `BaseModel.model_rebuild`.
  Args:
    cls: The class to rebuild the pydantic-core schema for.
    force: Whether to force the rebuilding of the schema, defaults to `False`.
    raise_errors: Whether to raise errors, defaults to `True`.
    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.
    _types_namespace: The types namespace, defaults to `None`.
  Returns:
    Returns `None` if the schema is already "complete" and rebuilding was not required.
    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.
  """
  if not force and cls.__pydantic_complete__:
    return None
  if '__pydantic_core_schema__' in cls.__dict__:
    delattr(cls, '__pydantic_core_schema__') # delete cached value to ensure full rebuild happens
  if _types_namespace is not None:
    rebuild_ns = _types_namespace
  elif _parent_namespace_depth > 0:
    rebuild_ns = _typing_extra.parent_frame_namespace(parent_depth=_parent_namespace_depth, force=True) or {}
  else:
    rebuild_ns = {}
  ns_resolver = _namespace_utils.NsResolver(
    parent_namespace=rebuild_ns,
  )
  return _pydantic_dataclasses.complete_dataclass(
    cls,
    _config.ConfigWrapper(cls.__pydantic_config__, check=False),
    raise_errors=raise_errors,
    ns_resolver=ns_resolver,
    # We could provide a different config instead (with `'defer_build'` set to `True`)
    # of this explicit `_force_build` argument, but because config can come from the
    # decorator parameter or the `__pydantic_config__` attribute, `complete_dataclass`
    # will overwrite `__pydantic_config__` with the provided config above:
    _force_build=True,
  )

```
  
---|---  
```
is_pydantic_dataclass(

```

Whether a class is a pydantic dataclass.
Parameters:
Name | Type | Description | Default  
---|---|---|---  
Returns:
Type | Description  
---|---  
Source code in `pydantic/dataclasses.py`
```
```
| ```
def is_pydantic_dataclass(class_: type[Any], /) -> TypeGuard[type[PydanticDataclass]]:
"""Whether a class is a pydantic dataclass.
  Args:
    class_: The class.
  Returns:
    `True` if the class is a pydantic dataclass, `False` otherwise.
  """
  try:
    return '__pydantic_validator__' in class_.__dict__ and dataclasses.is_dataclass(class_)
  except AttributeError:
    return False

```
  