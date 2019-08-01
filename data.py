import json

class Userdata:
    def __init__(self):
        with open('storage/userdata.json') as data_file:
            self.data = json.load(data_file)
            data_file.close()

    def saveData(self):
        with open('storage/userdata.json', 'w') as data_file:
            json.dump(self.data, data_file, indent=4, ensure_ascii=False)

    def currGet(self, id, currency, amount):
        if currency == "no":
            self.data[id].no -= amount
        elif currency == "chips":
            self.data[id].chips -= amount

    def currGive(self, id, currency, amount):
        if currency == "no":
            self.data[id].no += amount
        elif currency == "chips":
            self.data[id].chips += amount