import json
import os

class Config:

    _instance = None

    _data_base = {
        "host":"",
        "user":"",
        "pass":"",
        "port":"",
        "dbas":""
    }

    _url_cvm_base = ''
    _link_base_2 = ''
    _temp_dir = ''
    _chatgpt_token = ''

    def __init__(self):
        try:
            data = json.load(open('config.json'))
            
            self._url_cvm_base  = data['url_cvm_base']
            self._link_base_2   = data['link_base_2']
            self._temp_dir      = data['temp_dir']
            self._chatgpt_token = data['chatgpt_token']

            self._data_base['host'] = data['data_base']['host']
            self._data_base['user'] = data['data_base']['user']
            self._data_base['pass'] = data['data_base']['pass']
            self._data_base['port'] = data['data_base']['port']
            self._data_base['dbas'] = data['data_base']['dbas']
            
        except:
            print("o arquivo config.json não foi configurado na raiz do diretório")

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def getLinkBase2(self):
        return self._link_base_2

    def getDataBase(self):
        return self._data_base
    
    def getUrlCvmBase(self):
        return self._url_cvm_base
    
    def getChatGPTToken(self):
        return self._chatgpt_token
    
    def getTempDir(self):
        return self._temp_dir