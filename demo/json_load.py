import json
from io import StringIO

CONFIG_FILE = '''{
  "regular_count": 1,
  "express_count": 0,
  "self_serve_count": 0,
  "line_capacity": 1
}
'''
config_json: json = json.load(StringIO(CONFIG_FILE))

print(config_json)
