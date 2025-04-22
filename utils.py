import json

frequency_map = {"1": 1,
                 "9": 48,
                 "18": 84,
                 "36": 164
                }


def get_protocols_by_version(version_name: str, json_path:str) -> list:
    json_file = None
    with open(json_path,'r') as file:
        json_file = json.load(file)
    if json_file:
        protocols = json_file.get("protocols_by_version").get(version_name).get("protocols")
        return protocols
    return None

def count_protocols_in_session(data_file_path):
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


def get_frequency_for_protocol(protocol_json_path:str):
    frequency = {}
    protocols = None
    with open(protocol_json_path, 'r') as file:
        json_file = json.load(file)
    if json_file:
        protocols = json_file.get("protocols")
    for protocol_name, protocol_details in protocols.items():
        frequency[protocol_name] = frequency_map.get(str(protocol_details.get("fps")))
    return frequency

def get_not_dynamics_protocols(protocol_json_path: str):
    not_dynamics_protocols = []
    protocols = []
    with open(protocol_json_path, 'r') as file:
        json_file = json.load(file)
    if json_file:
        protocols = json_file.get("protocols")
    for protocol_name, protocol_details in protocols.items():
        is_dynamic = protocol_details.get("dynamic_size")
        if not is_dynamic:
            not_dynamics_protocols.append(protocol_name)
    return not_dynamics_protocols