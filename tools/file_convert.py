import struct
import json
import pickle


def text2binary(input_file_path, output_file_path, encoding='utf-8'):
    input_file = open(input_file_path, 'r', encoding=encoding, errors='ignore')
    input_file_content = input_file.read()

    # convert input_file_content to binary
    bytes = struct.pack('<10s', input_file_content)
    # wb is writing by binary, not need encoding
    open(output_file_path, "wb").write(bytes)


# useless function
def json2binary(input_file_path, output_file_path, encoding='utf-8'):
    input_file = open(input_file_path, 'r', encoding=encoding, errors='ignore')
    input_file_content = input_file.read()
    json_text = json.loads(input_file_content)
    json_binary = pickle.dumps(json_text)
    open(output_file_path, "wb").write(json_binary)


# useless function
def binary2json(input_file_path, output_file_path, encoding='utf-8'):
    input_file = open(input_file_path, 'rb')
    input_file_content = input_file.read()
    json_text = pickle.loads(input_file_content)
    open(output_file_path, "w", encoding=encoding, errors='ignore').write(str(json_text).replace("'", '"'))
