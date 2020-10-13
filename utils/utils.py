# Process templates
import os
import re
import toml
from string import Template


class CustomTemplate(Template):
    delimiter = '${'
    pattern = r'\${.*"(?:(?P<named>[^\{\}]+)"})'


def process_tmpl_files(template_dir):
    template_files_dir = f"{template_dir}/tmpl"
    template_files = os.listdir(template_files_dir)
    key_dict = {}
    # reg_ex = '(?<={{getv.*")(?="){}'
    key_regex = re.compile(r'\${".*"}')

    for file in template_files:
        key_set = set()
        with open(f"{template_files_dir}/{file}", encoding="utf-8") as f:
            for line in f.readlines():
                if key_regex.search(line):
                    key_set.add(key_regex.search(line).group().split('"')[1])
        key_dict[file[:-5]] = list(key_set)
    return(key_dict)


def process_toml_files(template_dir):
    toml_files_dir = f"{template_dir}/toml"
    toml_files = os.listdir(toml_files_dir)

    key_dict = {}

    for file in toml_files:
        toml_file = f"{toml_files_dir}/{file}"
        key_dict[file] = toml.load(toml_file)
    return key_dict


def check_template_and_keys_existance(template_keys, toml_keys):
    for files in toml_keys:
        if toml_keys[files]["template"]["src"][:-5] in template_keys:
            for key in template_keys[toml_keys[files]["template"]["src"][:-5]]:
                if key not in toml_keys[files]["template"]["keys"]:
                    print(
                        f'{toml_keys[files]["template"]["src"]} Key: "{key}" not found in {files} ')
                    exit()
        else:
            print(
                f'{toml_keys[files]["template"]["src"][:-5]} template file doesn\'t exists')
            exit()
    return False


# Checking whether the key is avaliable in backend file or not only for file backend

def key_existance_checker(keys_list, key_value):
    for keys in keys_list:
        if keys not in key_value:
            print(f'"{keys}" key not found in backend')
            return False
    return True

# Replacing key values and creating file at destination


def key_value_replace(template_dir, key_values, toml_keys):
    try:
        for file in toml_keys:
            new_data = True
            with open(f'{template_dir}/tmpl/{toml_keys[file]["template"]["src"]}') as stream:
                s = CustomTemplate(stream.read())
                new_data = s.safe_substitute(key_values)
            fout = open(
                f'{toml_keys[file]["template"]["dest"]}', "w")
            fout.write(new_data)
            fout.close()
        return True
    except Exception:
        return False
