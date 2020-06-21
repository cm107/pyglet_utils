# from colorama import Fore, init
# init()
from logger.logger_handler import TextHeader

class Error(Exception):
    def __init__ (self, message):
        super().__init__('\n\t' + TextHeader.red + message + TextHeader.std)