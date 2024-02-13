import mysql.connector

from libs import config

database = config.Config.instance().getDataBase()

class mysqli:

    _instance = None
    _db = None

    def __init__(self):
        
        self._db = mysql.connector.connect(
            host     = database['host'],
            user     = database['user'],
            password = database['pass'],
            database = database['dbas']
        )
        
    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance._db
    