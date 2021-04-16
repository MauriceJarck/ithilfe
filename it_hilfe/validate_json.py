import json
from marshmallow import Schema, fields


class ItHilfeSchema(Schema):
    devices = fields.Dict(keys=fields.Str(), values=fields.List(fields.Str), required=True)
    last_open_file_path = fields.Str(required=True)


def validate(file_path):
    """vaildates a json file for it_hilfe_gui

    Arg:
        file_path: file path to json file aimed to be validated

    Returns:
        None"""

    with open(file_path, "r") as file:
        pkg = json.load(file)

    ItHilfeSchema().load(pkg)

