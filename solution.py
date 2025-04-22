from typing import List
import utils

PROTOCOL_ID = 2
MESSAGE_BYTE = 3
MESSAGE_DATA = -1


class Solution:
    def __init__(self, data_file_path: str, protocol_json_path: str):
        self.data_file_path = data_file_path
        self.protocol_json_path = protocol_json_path

    # Question 1: What is the version name used in the communication session?
    def q1(self) -> str:
        first_line = ""
        with open(self.data_file_path, 'r') as file:
            for line in file:
                first_line = line.strip()
                break
        first_line = first_line.split(",")[MESSAGE_DATA]
        version_name = bytes.fromhex(first_line.replace(" ", "")).decode("ASCII")
        return version_name

    # Question 2: Which protocols have wrong messages frequency in the session compared to their expected frequency based on FPS?
    def q2(self) -> List[str]:
        count_map = utils.count_protocols_in_session(self.data_file_path)
        frequency_for_protocol = utils.get_frequency_for_protocol(self.protocol_json_path)
        ans = []
        for protocol, count in count_map.items():
            if count > frequency_for_protocol.get(protocol):
                ans.append(protocol)
        print(ans)
        return ans

    # Question 3: Which protocols are listed as relevant for the version but are missing in the data file?
    def q3(self) -> List[str]:
        ans = []
        protocols_in_version = utils.get_protocols_by_version(self.q1(), self.protocol_json_path)
        protocols_in_session = utils.count_protocols_in_session(self.data_file_path)
        for protocol in protocols_in_version:
            if not hex(int(protocol)) in protocols_in_session.keys():
                ans.append(hex(int(protocol)))
        return ans


    # Question 4: Which protocols appear in the data file but are not listed as relevant for the version?
    def q4(self) -> List[str]:
        ans = []
        protocols_in_version = utils.get_protocols_by_version(self.q1(), self.protocol_json_path)
        protocols_in_session = utils.count_protocols_in_session(self.data_file_path)
        for protocol in protocols_in_session.keys():
            if not str(int(protocol, 16)) in protocols_in_version:
                ans.append(protocol)
        return ans

    # Question 5: Which protocols have at least one message in the session with mismatch between the expected size integer and the actual message content size?
    def q5(self) -> List[str]:
        ans = []
        with open(self.data_file_path, 'r') as file:
            next(file)
            for line in file:
                line = line.strip()
                protocol = line.split(",")[PROTOCOL_ID].replace(" ", "")
                byte_msg = line.split(",")[MESSAGE_BYTE].replace(" ", "").replace("bytes","")
                msg = line.split(",")[MESSAGE_DATA]
                msg = msg.split(" ")
                if len(msg[1:]) != int(byte_msg):
                    ans.append(protocol)
        return ans

    # Question 6: Which protocols are marked as non dynamic_size in protocol.json, but appear with inconsistent expected message sizes Integer in the data file?
    def q6(self) -> List[str]:
        not_dynamic_protocols = utils.get_not_dynamics_protocols(self.protocol_json_path)
        protocols_bytes_in_session = {}
        with open(self.data_file_path, 'r') as file:
            next(file)
            for line in file:
                line = line.strip()
                protocol = line.split(",")[PROTOCOL_ID].replace(" ", "")
                byte_msg = line.split(",")[MESSAGE_BYTE].replace(" ", "").replace("bytes","")
                if not protocol in protocols_bytes_in_session.keys():
                    protocols_bytes_in_session[protocol] = set(byte_msg)
                else:
                    protocols_bytes_in_session[protocol].add(byte_msg)
        ans = [protocol_name for protocol_name, cnt in protocols_bytes_in_session.items() if len(cnt) > 1]
        ans = [protocol for protocol in ans if protocol in not_dynamic_protocols]
        return ans


if __name__ == '__main__':
    my_solution = Solution("data.txt","protocol.json")
    print(my_solution.q1())
    print(my_solution.q2())
    print(my_solution.q3())
    print(my_solution.q4())
    print(my_solution.q5())
    print(my_solution.q6())
