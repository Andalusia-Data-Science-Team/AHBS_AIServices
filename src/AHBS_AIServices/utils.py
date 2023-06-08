import json


def to_json(file_path, data_dict):
    # Serializing json
    json_object = json.dumps(data_dict, indent=4)

    # Writing to sample.json
    with open(file_path, "w") as outfile:
        outfile.write(json_object)


def load_from_json(file_path):
    data_dict = None
    with open(file_path) as json_file:
        data_dict = json.load(json_file)
    return data_dict
