import json
def dump_to_json(pipeline, json_file='props.json'):
    elements = {}
    for element in pipeline.children:
        current_element = {}
        for prop in element.props:
            if 'Gst' in prop.value_type.name:
                continue
            current_element[prop.name] =  [prop.flags, 
                                    prop.value_type.name, getattr(element.props, prop.name)]
        elements[element.name] = current_element
    print(elements)
    with open(json_file, 'w') as f:
        json.dump(elements, f, sort_keys=True, indent=4)


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
