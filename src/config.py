import os.path
from configobj import ConfigObj

class Configuration:
    def __init__(self):
        path = "../supersimon.conf"
        # TODO: "Get updates" approach instead of "has config"
        if not os.path.exists(path):
            self.__getconf(path)
        config = ConfigObj(path)
        self.game = GameInfo(config['Game'])
        self.protocol = ProtocolInfo(config['Protocol'])

    def __getconf(self, targetPath):
        f = open(targetPath, 'w')
        for line in open("config.conf"):
            if line.startswith('# !!'): continue
            f.write(line + '\n')
        f.close()

class GameInfo:
    def __init__(self, section):
        self.fullscreen = int(section['fullscreen']) == 1

class ProtocolInfo:
    def __init__(self, section):
        self.device = section['device']
        self.discoverMaximum = int(section['discoverMaximum'])
