from argparse import ArgumentParser
import os

class Parser(object):
    def __init__(self):
        # set available arguments
        self._parser = self.setup()

    def run(self, argv):
        # parse using the given arguments
        arguments = self._parser.parse_args(argv)
        return arguments

    @staticmethod
    def setup():
        parser = ArgumentParser()

        parser.add_argument("host",
                            metavar = "HOST",
                            help = "target host")

        parser.add_argument("-q", "--quiet",
                            action = "store_true",
                            help = "do not print banner and version info",
                            dest = "quiet",
                            default = False)

        parser.add_argument("-o", "--output",
                            metavar = "FILE",
                            action = "store",
                            help = "save output to a file",
                            dest = "output")
        
        parser.add_argument("-m", "--min-rate",
                            metavar = "NUMBER",
                            action = "store",
                            help = "Send packets no slower than <number> per second",
                            dest = "min_rate",
                            default=100)

        parser.add_argument("-M", "--max-rate",
                            metavar = "NUMBER",
                            action = "store",
                            help = "Send packets no faster than <number> per second",
                            dest = "max_rate",
                            default=300)

        return parser


class FileManager(object):
    def __init__(self):
        self._path = None

    def create(self, path):
        self._path = path
        if os.path.exists(self._path):
            return False
        else:
            self.write("")
            return True

    def saveON(self):
        # check if save mode is ON(argument.output is set)/OFF(not set)
        if self._path != None:
            return True
        else:
            return False

    def write(self, txt):
        if not self.saveON(): return

        with open(self._path, "w") as f:
            f.write(txt)

    def append(self, txt):
        if not self.saveON(): return

        with open(self._path, "a") as f:
            f.write(txt)
