import json
from marshmallow import Schema, fields


class ItHilfeDataSchema(Schema):
    devices = fields.Dict(keys=fields.Str(), values=fields.List(fields.Str), required=True)
    last_open_file_dir = fields.Str(required=True)


class ItHilfeUserPreferencesSchema(Schema):
    last_open_file_path = fields.Str(required=True)
    initial_theme = fields.Str(required=True)
    font_size = fields.Int(required=True)


def validate(file_path, schema):
    """vaildates a json file for it_hilfe_gui

    Arg:
        file_path: file path to json file aimed to be validated
        schema: contains the rules of validation
    Returns:
        None"""

    with open(file_path, "r") as file:
        pkg = json.load(file)

    schema().load(pkg)

