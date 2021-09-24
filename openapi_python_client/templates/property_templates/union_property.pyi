{% macro construct(property, source, initial_value=None) %}
def _parse_{{ property.python_name }}(data: {{ property.get_type_string(json=True) }}) -> Union[UnknownType, {{ property.get_type_string() }}]:
    {{ property.python_name }}: {{ property.get_type_string() }}
    {% if "None" in property.get_type_strings_in_union(json=True) %}
    if data is None:
        return data
    {% endif %}
    {% if "Unset" in property.get_type_strings_in_union(json=True) %}
    if isinstance(data, Unset):
        return data
    {% endif %}
    {% if property.discriminator_property != None %}
    discriminator_value: str = cast(str, data.get("{{property.discriminator_property}}"))
    if discriminator_value is not None:
        {% for discriminated_by, inner_property in property.discriminator_mappings.items() %}
        if discriminator_value == "{{discriminated_by}}":
            {% from "property_templates/" + inner_property.template import construct %}
            {{ construct(inner_property, "data", initial_value="UNSET") | indent(12) }}
            return {{ property.python_name }}
        {% endfor %}

        return UnknownType(value=data)
    {% endif %}
    {% for inner_property in property.inner_properties_with_template() %}
    try:
    {% from "property_templates/" + inner_property.template import construct, check_type_for_construct %}
        if not {{ check_type_for_construct("data") }}:
            raise TypeError()
        {{ construct(inner_property, "data", initial_value="UNSET") | indent(8) }}
        return {{ property.python_name }}
    except: # noqa: E722
        pass
    {% endfor %}
    {% if property.has_properties_without_templates %}
    {# Doesn't really matter what we cast it to as this type will be erased, so cast to one of the options #}
    return cast({{ property.get_type_string() }}, data)
    {% else %}
    return UnknownType(data)
    {% endif %}

{{ property.python_name }} = _parse_{{ property.python_name }}({{ source }})
{% endmacro %}

{# For now we assume there will be no unions of unions #}
{% macro check_type_for_construct(source) %}True{% endmacro %}

{% macro transform(property, source, destination, declare_type=True, query_parameter=False) %}
{% if not property.required or property.nullable %}
{{ destination }}{% if declare_type %}: {{ property.get_type_string(query_parameter=query_parameter, json=True) }}{% endif %}

if isinstance({{ source }}, Unset):
    {{ destination }} = UNSET
{% endif %}
{% if property.nullable %}
    {% if property.required %}
if {{ source }} is None:
    {% else %}{# There's an if UNSET statement before this #}
elif {{ source }} is None:
    {% endif %}
    {{ destination }} = None
{% endif %}
{% if property.required and not property.nullable %}{# No if UNSET or if None statement before this #}
if isinstance({{ source }}, UnknownType):
    {{ destination }} = {{ source }}.value
{% else %}
elif isinstance({{ source }}, UnknownType):
    {{ destination }} = {{ source }}.value
{% endif %}
{% for inner_property in property.inner_properties_with_template() %}
    {% if not loop.last or property.has_properties_without_templates %}
elif isinstance({{ source }}, {{ inner_property.get_instance_type_string() }}):
    {% else %}
else:
    {% endif %}
    {% from "property_templates/" + inner_property.template import transform %}
    {{ transform(inner_property, source, destination, declare_type=False) | indent(4) }}
{% endfor %}
{% if property.has_properties_without_templates and (property.inner_properties_with_template() | any or not property.required)%}
else:
    {{ destination }} = {{ source }}
{% elif property.has_properties_without_templates %}
{{ destination }} = {{ source }}
{% endif %}

{% endmacro %}
