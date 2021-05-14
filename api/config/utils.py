from .constants import CONFIG_FILE
import yaml

def load_config() -> dict:
    with open(CONFIG_FILE) as yaml_file:
        conf = yaml.load(yaml_file.read(), Loader=yaml.SafeLoader)
    return conf