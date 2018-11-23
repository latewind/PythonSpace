import asyncio


@asyncio.coroutine
def hello():
    n = 5
    while n:
        yield from asyncio.sleep(1)
        print(n)
        n = n - 1

async def love_huan():
    n = 5
    while n:
        await asyncio.sleep(1)
        print('love you %s' % n)
        n = n - 1


loop = asyncio.get_event_loop()
loop.run_until_complete(hello())

tasks = [love_huan(), hello()]
loop.run_until_complete(asyncio.wait(tasks))