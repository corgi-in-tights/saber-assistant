import asyncio
import logging

from fastapi import FastAPI
from fastapi import WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.websockets import WebSocketDisconnect

from .queue_store import queue_pop
from .queue_store import queue_put

app = FastAPI()
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("saber")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clients = set()
background_tasks = set()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if not data:
                continue
            if "sentence" not in data:
                await websocket.send_text("Invalid data format. Expected 'sentence' key.")
                continue

            sentence = data["sentence"]
            await queue_put(data)
            await websocket.send_text(f"Received: {sentence}")

    except WebSocketDisconnect:
        logger.debug("Client disconnected")
    finally:
        clients.remove(websocket)


async def process_item(item):
    if "sentence" not in item:
        logger.error("Item missing 'sentence' key: %r", item)
        return

    sentence = item["sentence"]
    logger.debug("Processing item: %s", sentence)

    # get intents
    intents = []

    


async def queue_worker():
    while True:
        item = await queue_pop()
        await process_item(item)
        await asyncio.sleep(0)  # prevent blocking


@app.on_event("startup")
async def start_queue_worker():
    task = asyncio.create_task(queue_worker())
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)
