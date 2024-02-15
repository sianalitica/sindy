import asyncio
from sindy import extract,docs,transform

async def start():

    print("""
    ┍╸┑╻┍┑ ┍╸╮╻ ╻
    ┕╸┑╽╽╽╽╽ ╽┕╻┙
     ╸┙╹ ┕┙┕╸╯ ╹
    """)

    while True:
        extract.start()
        docs.read()
        transform.now()
        await asyncio.sleep(60 * 60 * 2)

asyncio.run(start())