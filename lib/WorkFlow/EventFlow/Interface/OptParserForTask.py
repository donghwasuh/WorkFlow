import optparse

class OptionParsingError(RuntimeError):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class OptionParsingExit(Exception):
    def __init__(self, status, msg):
        self.status = status
        self.msg = msg

class OptParserForTask(optparse.OptionParser):
    def error(self, msg):
        raise OptionParsingError(msg)

    def exit(self, status = 0, msg = None):
        raise OptionParsingError(msg)
        
