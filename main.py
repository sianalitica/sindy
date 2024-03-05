import asyncio
from sindy import extract,docs,transform,analise
from datetime import datetime
from libs.logs import info,warning,success,header

async def start():

    header()

    while True:
        warning("====================================================")
        #info("Extração iniciada")
        #extract.start()
        #info("Leitura e gravação de documento iniciado")
        #docs.read()
        info("Fazendo análise dos dados nos documentos")
        analise.start()
        #info("Fazendo transformação de dados")
        #transform.now()
        warning('Fazendo uma pausa de 3h a partir de agora...')
        await asyncio.sleep(60 * 60 * 3)
        success('De volta ao trabalho!')

asyncio.run(start())