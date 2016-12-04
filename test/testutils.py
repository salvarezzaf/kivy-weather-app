import json


class TestUtils():

    def load_json_from_file(self,filename):

        with open(filename) as f:
            data = json.load(f)
        return data
