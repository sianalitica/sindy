import asyncio
from sindy import extract,docs,transform
from datetime import datetime

async def start():

    print("""
    ┍╸┑╻┍┑ ┍╸╮╻ ╻
    ┕╸┑╽╽╽╽╽ ╽┕╻┙
     ╸┙╹ ┕┙┕╸╯ ╹ v0.0.2
    """)
    print("iniciada em: "+ str(datetime.now()))
    while True:
        # extract.start()
        docs.read()
        transform.now()
        await asyncio.sleep(60 * 60 * 2)

asyncio.run(start())

# usar essa lib para converter em html
# https://www.adobe.com/acrobat/hub/how-to-convert-pdf-to-html.html