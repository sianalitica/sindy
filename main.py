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
        warning("====================================================")
        info("Extração iniciada")
        extract.start()
        info("Leitura e gravação de documento iniciado")
        docs.read()
        # info("Fazendo transformação de dados")
        #transform.now()
        warning('Fazendo uma pausa de 3h a partir de agora...')
        await asyncio.sleep(60 * 60 * 3)
        success('De volta ao trabalho!')

asyncio.run(start())


# usar essa lib para converter em html
# https://www.adobe.com/acrobat/hub/how-to-convert-pdf-to-html.html