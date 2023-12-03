from data import Data

class Backtester:

    def __init__(self, data: Data):
        self.data = data
        self.positions = self.position_getter()

    def position_getter(self):
        pass

    def get_stats(self):
        pass

    