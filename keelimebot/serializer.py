import jsonpickle
import logging
import json

logger = logging.getLogger(__name__)
jsonpickle.set_encoder_options('json', indent=2)

pickled_keys = ['cls', 'func']


def _serialize(obj):
    try:
        return obj.serialize()
    except Exception:
        return jsonpickle.encode(obj)


def _deserialize(obj: dict) -> dict:
    new_obj = obj.copy()

    for k, v in obj.items():
        if isinstance(v, dict):
            new_obj[k] = _deserialize(v)

        elif k in pickled_keys:
            new_obj[k] = jsonpickle.decode(v)

    return new_obj


def json_deserialize_from_file(file) -> dict:
    json_dict = json.load(file)
    return _deserialize(json_dict)


def json_serialize_to_string(obj) -> str:
    return json.dumps(obj, default=_serialize, indent=2)
