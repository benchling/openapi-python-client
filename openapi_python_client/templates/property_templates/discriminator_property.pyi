{% macro construct(property, source, initial_value=None) %}

{% if initial_value != None %}
{{ property.python_name }} = {{ initial_value }}
{% elif property.nullable %}
{{ property.python_name }} = None
{% else %}
{{ property.python_name }}: {{ property.get_type_string() }} = UNSET
{% endif %}

_{{ property.python_name }} = {{source}}

if {% if property.nullable %}_{{ property.python_name }} is not None{% endif %}{% if property.nullable and not property.required %} and {% endif %}{% if not property.required %}not isinstance(_{{ property.python_name }},  Unset){% endif %}:

    discriminator = d["{{ property.discriminator_property}}"]
    {% set ns = namespace(if_stmt='if') %}
    {% for (key, value) in property.discriminator_mappings.items() %}
    {{ ns.if_stmt }} discriminator == "{{ key }}":
        {{ property.python_name }} = {{ value.class_name }}.from_dict(_{{ property.python_name}})
        {% set ns.if_stmt = 'elif' %}
    {% endfor %}
    else:
        raise ValueError(f'Unexpected discriminator value: {discriminator}')
{% endif %}
return {{ property.python_name }}

{% endmacro %}
