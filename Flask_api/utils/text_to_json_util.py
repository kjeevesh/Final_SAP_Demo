import json
 
 

class TextToJson(object):

    def __init__(self, filename) -> None:
        self.textfile = filename

    def text_to_json(self):

 
        # dictionary where the lines from
        # text will be stored
        dict1 = {}
 
        # creating dictionary
        with open(self.textfile) as json_file:
            dict1 = json.load(json_file)


        return dict1