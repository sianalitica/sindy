import asyncio
from sindy import extract,docs,transform
from datetime import datetime
from libs.logs import info,warning,success

async def start():

    print("""\033[96m
    ┍╸┑╻┍┑ ┍╸╮╻ ╻
    ┕╸┑╽╽╽╽╽ ╽┕╻┙
     ╸┙╹ ┕┙┕╸╯ ╹ \033[93m v0.0.3
    """)
    print("\033[92m iniciada em: "+ str(datetime.now())+"\x1b[0m")
    while True:
        info("Extração iniciada em: "+str(datetime.now()))
        extract.start()
        info("Leitura e gravação de documento iniciado em: "+str(datetime.now()))
        docs.read()
        info("Fazendo transformação de dados em: "+str(datetime.now()))
        transform.now()
        warning('Fazendo uma pausa de 2h...')
        await asyncio.sleep(60 * 60 * 2)
        success('Voltei!')

asyncio.run(start())

# usar essa lib para converter em html
# https://www.adobe.com/acrobat/hub/how-to-convert-pdf-to-html.html