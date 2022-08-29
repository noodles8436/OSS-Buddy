PATH = "./Buddy_config.json"
import json, os


class configManager:
    """This class is for importing and storing the setting values of the client program.
    """

    config = dict()
    """It is a dict object that stores the setting value of the client program."""

    def __init__(self):
        """A function to initialize the configManager class
        Check if the config.json file already exists and read the setting values from the config.json file.
        If there is no config.json file, create a new one and save it to the config.json file
        using the initial values at the top of FileManager.py.
        """

        # if there is no config.json file
        if os.path.isfile(PATH) is not True:
            # Create config.json file
            fd = open(PATH, 'w', encoding='UTF-8')
            fd.write("{}")
            fd.close()

            # Store initial config datas in new created config.json file
            self.recoveryOptions()

        # read config.json and store config.json data in self.config ( dict variable ) using json.load()
        with open(PATH, 'r', encoding="UTF-8") as pf:
            self.config = json.load(pf)
            pf.close()

        return

    def setValue(self, option, value):
        """This function changes the setting value.
        :param str option: json key-value you want to change
        :param value: value you want to set
        """

        # change self.config
        self.config[option] = value

        # save changed self.config in config.json
        self.saveJSON()
        return

    def isKey(self, key):
        if key in self.config.keys():
            return True
        return False

    def getValue(self, key):
        if self.isKey(key):
            return self.config[key]
        return None

    def removeKey(self, key):
        if self.isKey(key):
            del self.config[key]

    def getConfig(self):
        """This function returns a self.config object."""
        return self.config

    def saveJSON(self):
        """This function stores the self.config object in the form of json in the config.json file."""

        with open(PATH, 'w', encoding='UTF-8') as pf:
            json.dump(self.config, pf, indent='\t', ensure_ascii=False)
        pf.close()
