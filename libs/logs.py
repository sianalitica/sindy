
def success(msg:str):
    print("\033[92m"+msg+"\x1b[0m")

def info(msg:str):
    print("\033[94m"+msg+"\x1b[0m")

def warning(msg:str):
    print("\033[93m"+msg+"\x1b[0m")

def danger(msg:str):
    print("\033[91m"+msg+"\x1b[0m")