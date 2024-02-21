
from datetime import datetime
import uuid

def write_file_error(capture:str):
    file_name = str(uuid.uuid4().hex)+".txt"
    with open("./error_files/"+file_name, "a+") as f:
        f.write(capture)
        f.close()
    return file_name

def write_log(msg:str, color):
    agora = str(datetime.now())
    parts = agora.split(" ")
    print(color+msg+"\x1b[0m")
    with open("./logs/"+parts[0]+".txt", "a+") as f:
        f.write(parts[1]+" : "+msg+"\n")
        f.close()

def success(msg:str):
    write_log(msg, "\033[92m")

def info(msg:str):
    write_log(msg, "\033[94m")

def warning(msg:str):
    write_log(msg, "\033[93m")

def danger(msg:str, capture:str=""):
    if capture != "":
        file_name = write_file_error(capture=capture)
        msg += " -> ./error_files/"+file_name
    write_log(msg, "\033[91m")
    