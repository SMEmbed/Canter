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

def gprop_to_json_type(gprop_type):
    if 'int' in gprop_type:
        return 'number'
    elif 'gboolean' == gprop_type:
        return 'bool'
    elif 'char' in gprop_type:
        return 'string'
    print(gprop_type)
    return None

def dump_to_json_schema(pipeline, json_file='props_schema.json'):
    elements = {}
    for element in reversed(pipeline.children):
        current_element = {'type' : 'object', 'properties' : {}}
        for prop in element.props:
            if 'Gst' in prop.value_type.name:
                print(prop.value_type.name)
                continue
            if prop.flags & 2:
                current_element['properties'][prop.name] =  {
                        'type' : gprop_to_json_type(prop.value_type.name), 
                        'default' : getattr(element.props, prop.name)}
        elements[element.name] = current_element

    print(elements)
    schema = {'type' : 'object', 'properties' : elements}
    with open(json_file, 'w') as f:
        json.dump(schema, f, indent=4)

