import boto3
import configparser


def get_params(key_list):
    config_file_path = ""
    config = configparser.ConfigParser()
    config.read(config_file_path)

    client = boto3.client(
        'ssm',
        # region_name="us-east-1",
        region_name=config['aws_config']['region_name'],
        aws_access_key_id=config['aws_config']['aws_access_key_id'],
        aws_secret_access_key=config['aws_config']['aws_secret_access_key']
    )
    count = len(key_list)//10
    remain = len(key_list) - count * 10

    response = []
    key_value_dict = {}

    for i in range(count):
        response.append(client.get_parameters(
            Names=key_list[10 * i:10 * i + 10],
            WithDecryption=True
        ))
        if i + 1 == count and remain:
            response.append(client.get_parameters(
                Names=key_list[count*10: count*10 + remain],
                WithDecryption=True
            ))

    for data in response:
        if len(data["InvalidParameters"]) > 0:
            print(f"Parameter Not found {data['InvalidParameters']} in SSM")
            return
        for parameter in data["Parameters"]:
            key_value_dict[parameter['Name']] = parameter['Value']
    return key_value_dict
