import sys
import json
from pprint import pprint

from marshmallow import Schema, fields, ValidationError

needed = ["devices", "last_open_file_path"]


class ItHilfeSchema(Schema):
    devices = fields.Dict(keys=fields.Str(), values=fields.List(fields.Str), required=True)
    last_open_file_path = fields.Str(required=True)


def validate(file_path):
    try:
        with open(file_path, "r") as file:
            pkg = json.load(file)
            for need in needed:
                if need not in dict(pkg).keys():
                    raise ValidationError(need, 'not in needed')
        return True

    except ValidationError as error:
        return error.messages