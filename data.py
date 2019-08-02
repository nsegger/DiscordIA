import json

class Userdata:
    def __init__(self):
        with open('storage/userdata.json') as data_file:
            self.udata = json.load(data_file)
            data_file.close()
        self.data = self.udata["users"]
        self.currs = ["Niobium Oshit", "Chips"]

    def saveData(self):
        with open('storage/userdata.json', 'w') as data_file:
            self.udata["users"] = self.data
            json.dump(self.udata, data_file, indent=4, ensure_ascii=False)

    def currGet(self, pid, currency, amount):
        if currency in self.currs:
            if self.data[str(pid)][currency] >= amount:
                self.data[str(pid)][currency] -= amount
                return True
            else:
                return False

    def currGive(self, pid, currency, amount):
        if currency in self.currs:
            self.data[str(pid)][currency] += amount


uData = Userdata()