import json

import numpy as np
from flask.json.provider import JSONProvider


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


class CustomJSONProvider(JSONProvider):

    def dumps(self, obj, **kwargs):
        return json.dumps(obj, **kwargs, cls=NpEncoder)

    def loads(self, s: str | bytes, **kwargs):
        return json.loads(s, **kwargs)
