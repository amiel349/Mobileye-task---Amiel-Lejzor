import json

frequency_map = {"1": 1,
                 "9": 48,
                 "18": 84,
                 "36": 164
                }

def read_json_file(json_path: str):
        with open(json_path, 'r') as file:
            print(f"reading {json_path}")
            json_file = json.load(file)
            return json_file

def get_protocols_by_version(version_name: str, json_path:str) -> list:
    """
    return a list with all protocols listed by the version
    :param version_name:
    :param json_path:
    :return:
    """
    json_file = read_json_file(json_path)
    if json_file:
        protocols = json_file.get("protocols_by_version").get(version_name).get("protocols")
        return protocols
    return []

def count_protocols_in_session(data_file_path)-> dict:
    """
    :param data_file_path:
    :return: a map with protocols name as key and appearances in session as value
    """
    count_map = {}
    with open(data_file_path, 'r') as file:
        next(file)
        for line in file:
            line = line.strip()
            line = line.split(",")[2].replace(" ", "")
            if line in count_map:
                count_map[line] = count_map[line] + 1
            else:
                count_map[line] = 0
    return count_map


def get_frequency_for_protocol(json_path:str)->dict:
    """
    :param json_path:
    :return: a dict with protocol name as key and expected frequncy as value
    """
    frequency = {}
    protocols = None
    json_file = read_json_file(json_path)
    if json_file:
        protocols = json_file.get("protocols")
    for protocol_name, protocol_details in protocols.items():
        frequency[protocol_name] = frequency_map.get(str(protocol_details.get("fps")))
    return frequency

def get_not_dynamics_protocols(json_path: str)->list:
    """
    return a list with all protocols (hexa) with false dynamic size
    :param json_path:
    :return:
    """
    not_dynamics_protocols = []
    protocols = []
    json_file = read_json_file(json_path)
    if json_file:
        protocols = json_file.get("protocols")
    for protocol_name, protocol_details in protocols.items():
        is_dynamic = protocol_details.get("dynamic_size")
        if not is_dynamic:
            not_dynamics_protocols.append(protocol_name)
    return not_dynamics_protocols
