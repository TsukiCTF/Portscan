from argparse import ArgumentParser

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
                            help = "target host")

        parser.add_argument("-q", "--quiet",
                            dest = "quiet",
                            action = "store_true",
                            help = "do not print banner and version info",
                            default = False)

        return parser
