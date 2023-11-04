from ibapi.client import *
from ibapi.wrapper import *
import time

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
