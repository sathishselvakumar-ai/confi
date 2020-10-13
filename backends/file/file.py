import yaml
import os


def fetch_key_values(filename):
    key_values = {}
    # filename = "D:/ASPIRE/scripts/confd/confd/Source/test/backend.yaml"
    if not os.path.isfile(filename):
        print(f'backend file "{filename}" not found')
        return {}
    with open(filename, 'r') as stream:
        try:
            key_values = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return key_values
