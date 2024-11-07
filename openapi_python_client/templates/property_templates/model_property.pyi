{# This file is shadowed by the template with the same name
 # in aurelia/packages/api_client_generation/templates #}
{% macro construct(property, source, initial_value=None, nested=False) %}
{% if property.required and not property.nullable %}
{% if source == "response.yaml" %}
yaml_dict = yaml.safe_load(response.text.encode("utf-8"))
{{ property.python_name }} = {{ property.reference.class_name }}.from_dict(yaml_dict)
{% else %}
{{ property.python_name }} = {{ property.reference.class_name }}.from_dict({{ source }})
{% endif %}
{% else %}
{% if initial_value != None %}
{{ property.python_name }} = {{ initial_value }}
{% elif property.nullable %}
{{ property.python_name }} = None
{% else %}
{{ property.python_name }}: {{ property.get_type_string() }} = UNSET
{% endif %}
_{{ property.python_name }} = {{source}}
if {% if property.nullable %}_{{ property.python_name }} is not None{% endif %}{% if property.nullable and not property.required %} and {% endif %}{% if not property.required %}not isinstance(_{{ property.python_name }},  Unset){% endif %}:
    {{ property.python_name }} = {{ property.reference.class_name }}.from_dict(_{{ property.python_name }})
{% endif %}
{% endmacro %}

{% macro check_type_for_construct(source) %}isinstance({{ source }}, dict){% endmacro %}

{% macro transform(property, source, destination, declare_type=True, query_parameter=False) %}
{{ transform_extended(property, source, destination, declare_type=declare_type, query_parameter=query_parameter) }}
{% endmacro %}

{% macro transform_extended(property, source, destination, declare_type=True, query_parameter=False, skip_read_only_expr="") %}
{% set to_dict_params = ("_skip_read_only="+skip_read_only_expr) if skip_read_only_expr else "" %}
{% set to_dict_expr = source + ".to_dict(" + to_dict_params + ")" %}
{% if property.required %}
{% if property.nullable %}
{{ destination }} = {{ to_dict_expr }} if {{ source }} else None
{% else %}
{{ destination }} = {{ to_dict_expr }}
{% endif %}
{% else %}
{{ destination }}{% if declare_type %}: {{ property.get_type_string(query_parameter=query_parameter, json=True) }}{% endif %} = UNSET
if not isinstance({{ source }}, Unset):
{% if property.nullable %}
    {{ destination }} = {{ to_dict_expr }} if {{ source }} else None
{% else %}
    {{ destination }} = {{ to_dict_expr }}
{% endif %}
{% endif %}
{% endmacro %}
