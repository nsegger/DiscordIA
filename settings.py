import json

class Settings:
    def __init__(self):
        with open('storage/config.json') as cfg_file:
            self.cfg = json.load(cfg_file)
            cfg_file.close()
        self.bot = self.cfg["bot"]
        self.servers = self.cfg["servers"]
        
    def __updateSelf(self):
        #cfg["bot"] = self.bot      # We don't want to mess with this, I assure you.
        self.cfg["servers"] = self.servers

    def saveCfg(self):
        self.__updateSelf()
        with open('storage/config.json', 'w') as cfg_file:
            json.dump(self.cfg, cfg_file, indent=4, ensure_ascii=False)

    async def cfgServerCreate(self, sID, ch):
        if str(sID) in self.servers:
            print(f"Server {sID} already configured.")
        else:
            self.servers[str(sID)] = {"logs": ch.id, "welcome": ch.id, "amsht": ch.id, "poker":ch.id}
            await ch.send("***```Configure o canal de log, de boas vindas, e mais, utilizando .config```***")


Config = Settings()