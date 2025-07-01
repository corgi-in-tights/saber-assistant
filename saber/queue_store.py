import asyncio

_queue = asyncio.Queue()

async def queue_put(item):
    await _queue.put(item)

async def queue_get():
    return await _queue.get()

async def queue_pop():
    if _queue.empty():
        return None
    return await _queue.get()

def qsize():
    return _queue.qsize()
