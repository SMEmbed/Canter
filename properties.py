import json

def load_from_json(pipeline, json_file='props.json'):
    with open(json_file, 'r') as f:
        properties = json.load(f)
    print(properties)
    for element in pipeline.children:
        for prop in element.props:
            try:
                json_config = properties[element.name][prop.name]
            except KeyError:
                continue
            if json_config[0] & 2:
                setattr(element.props, prop.name, json_config[2])


def dump_to_json(pipeline, json_file='props.json'):
    elements = {}
    for element in reversed(pipeline.children):
        current_element = {}
        for prop in element.props:
            if 'Gst' in prop.value_type.name:
                continue
            current_element[prop.name] =  [prop.flags, 
                                    prop.value_type.name, getattr(element.props, prop.name)]
        elements[element.name] = current_element
    print(elements)
    with open(json_file, 'w') as f:
        json.dump(elements, f, indent=4)

def gprop_to_json(gprop, default_value):
    gprop_type = gprop.value_type.name
    basic_prop = {'default' : default_value}
    if 'int' in gprop_type:
        basic_prop['type'] = 'number'
        basic_prop['maximum'] = gprop.maximum
        basic_prop['minimum'] = gprop.minimum
    elif 'gboolean' == gprop_type:
        basic_prop['type'] = 'boolean'
    elif 'char' in gprop_type:
        basic_prop['type'] = 'string'
    elif hasattr(gprop, 'enum_class'):
        enum_options = gprop.enum_class.__enum_values__.values()
        basic_prop['enum'] = [x.value_nick for x in enum_options]
        basic_prop['type'] = 'string'
        basic_prop['default'] = default_value.value_nick
    else:
        print('cant analyze type: ', gprop_type, gprop.name)
        return None
    return basic_prop

def dump_to_json_schema(pipeline, json_file='props_schema.json'):
    elements = {}
    for element in reversed(pipeline.children):
        current_element = {'type' : 'object', 'properties' : {}}
        for prop in element.props:
            if prop.name == 'name':
                continue
            if prop.flags & 2:
                json_serialized = gprop_to_json(prop, getattr(element.props, prop.name))
                if json_serialized:
                    current_element['properties'][prop.name] = json_serialized
        elements[element.name] = current_element

    print(elements)
    schema = {'type' : 'object', 'properties' : elements}
    with open(json_file, 'w') as f:
        json.dump(schema, f, indent=4)

