import sqlite3

class _printdb:
    def __init__(self):
        self._conn = sqlite3.connect('moncafe.db')
    def print(self):

