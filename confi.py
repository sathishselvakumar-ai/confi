import os
import argparse

"""
    Cli Options:
    --backend:
        - ssm
        - keyvault
        - file
    -f (required if backend file selected):
        - Backend file path
        - File should be in yaml
    --temp-dir:
        - Templates directory
        - Required for windows and optional for linux
        - default template directory for linux is /opt/confd
    --config(optional if role based access provided):
        - Configuration file for backends
        - Should be in yaml
"""
import utils.utils as util
import backends.file.file as fileback
import backends.ssm.ssm as ssm
import backends.keyvault.keyvault as keyvault


def main():

    parser = argparse.ArgumentParser(
        description="Cross platform Configuration management tool")

    parser.add_argument('--backend', help="backend for configurations",
                        choices=["file", "ssm", "keyvault"], required=True)
    parser.add_argument(
        '-f', help="file path for backend if backend is set to file. File should be yaml")
    parser.add_argument(
        '--temp_dir', help="configurations template directory path Required for Windows and Optional for *nix")
    parser.add_argument(
        '--config', help="configuration file for backends 'ssm/keyvault', can be omitted if role based access provided")
    args = parser.parse_args()

    if args.backend == "file":
        if args.f and os.path.isfile(args.f):
            pass
        else:
            print("-f backend file required")
            exit()

    # Test data
    template_dir = args.temp_dir
    # template_dir = "D:/ASPIRE/scripts/confd/confd/Source/test"
    backend = args.backend

    # Checking for valid directory
    if not os.path.isdir(template_dir):
        print("Enter a valid directory")
        exit()

    # Parsing the tmpl files
    template_keys = util.process_tmpl_files(template_dir)

    # Parsing the toml files
    toml_keys = util.process_toml_files(template_dir)

    # Checking for key existance
    util.check_template_and_keys_existance(
        template_keys, toml_keys)

    key_values = {}
    keys_existance = True

    key_list = []

    for file in toml_keys:
        key = toml_keys[file]["template"]["keys"]
        key_list.extend(key)

    if backend == "file":
        key_values = fileback.fetch_key_values(args.f)
        keys_existance = util.key_existance_checker(key_list, key_values)
    elif backend == "ssm":
        key_values = ssm.get_params(key_list)
    # elif backend == "keyvault":
    #     key_values = fileback.fetch_key_values()
    #     keys_existance = util.key_existance_checker(key_list, key_values)
    else:
        return

    if not keys_existance:
        return
    else:
        util.key_value_replace(template_dir, key_values, toml_keys)


if __name__ == "__main__":
    main()
