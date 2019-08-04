import yaml


__config = None

def config():
    """YAML FILE READER"""
    global __config
    if not __config:
        with open(r'src\common\config.yaml',mode='r') as f:
            __config = yaml.load(f)
    return __config        