import json
from pathlib import Path

root_path = Path(__file__).parents[0]
config_path = "{}{}".format(str(root_path),"/configs/config.json")

try:
    with open(config_path, 'r') as myfile:
        data = myfile.read()
except Exception:
    print("Error reading config file")
    
file_configs = json.loads(data)
    