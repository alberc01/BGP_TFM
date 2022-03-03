import json
class Writer():
    def write_dict_to_file(self, name, dict):
            with open(name, "a") as outfile:
                        json.dump(dict, outfile,indent=4)