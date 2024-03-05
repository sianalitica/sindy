
from datetime import datetime
import uuid
import subprocess

def clear():
    subprocess.run("clear", shell=True, text=True)

def header(text="", date=True):
    clear()
    print("""\033[96m
    ┍╸┑╻┍┑ ┍╸╮╻ ╻
    ┕╸┑╽╽╽╽╽ ╽┕╻┙
     ╸┙╹ ┕┙┕╸╯ ╹ \033[93m v0.0.3
    """+text)
    if date:
        print("\033[92m iniciada em: "+ str(datetime.now())+"\x1b[0m")

def write_file_error(capture:str):
    file_name = str(uuid.uuid4().hex)+".txt"
    with open("./error_files/"+file_name, "a+") as f:
        f.write(capture)
        f.close()
    return file_name

def write_log(msg:str):
    agora = str(datetime.now())
    parts = agora.split(" ")
    with open("./logs/"+parts[0]+".txt", "a+") as f:
        f.write(parts[1]+" : "+msg+"\n")
        f.close()

def success(msg:str, write=True):
    print("\033[92m"+msg+"\x1b[0m")
    if write:
        write_log(msg)

def info(msg:str,  write=True):
    print("\033[94m"+msg+"\x1b[0m")
    if write:
        write_log(msg)

def warning(msg:str, write=True):
    print("\033[93m"+msg+"\x1b[0m")
    if write:
        write_log(msg)

def danger(msg:str, capture:str="", write=True):
    if capture != "":
        file_name = write_file_error(capture=capture)
        msg += " -> ./error_files/"+file_name
    print("\033[91m"+msg+"\x1b[0m")
    if write:
        write_log(msg)
    