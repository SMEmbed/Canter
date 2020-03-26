import json
import jsonschema
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst, GLib


def load_from_json(pipeline, json_file='props.json', schema_file='props_schema.json'):
    with open(json_file, 'r') as f:
        properties = json.load(f)
    with open(schema_file, 'r') as f:
        schema = json.load(f)

    try:
        jsonschema.validate(properties, schema)
    except jsonschema.exceptions.ValidationError as e:
        print('not matching to schema', e)
        return False

    for element in pipeline.children:
        for prop in element.props:
            try:
                json_config = properties[element.name][prop.name]
            except KeyError:
                continue
            setattr(element.props, prop.name, json_config)
    return True

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
    if 'gboolean' == gprop_type:
        basic_prop['type'] = 'boolean'
    elif 'gfloat' == gprop_type:
        basic_prop['type'] = 'number'
        basic_prop['maximum'] = gprop.maximum
        basic_prop['minimum'] = gprop.minimum
    elif 'gchararray' == gprop_type:
        basic_prop['type'] = 'string'
        #TODO check if there is length limit
    elif hasattr(gprop, 'enum_class'):
        enum_options = gprop.enum_class.__enum_values__.values()
        basic_prop['enum'] = [x.value_nick for x in enum_options]
        basic_prop['type'] = 'string'
        basic_prop['default'] = default_value.value_nick
    elif 'int' in gprop_type:
        basic_prop['type'] = 'integer'
        basic_prop['maximum'] = gprop.maximum
        basic_prop['minimum'] = gprop.minimum
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
            if prop.flags & GObject.ParamFlags.WRITABLE:
                json_serialized_prop = gprop_to_json(prop, getattr(element.props, prop.name))
                if json_serialized_prop:
                    current_element['properties'][prop.name] = json_serialized_prop
            #TODO also write readonly properties
        elements[element.name] = current_element

    schema = {'type' : 'object', 'properties' : elements}
    with open(json_file, 'w') as f:
        json.dump(schema, f, indent=4)

