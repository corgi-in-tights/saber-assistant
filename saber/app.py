import asyncio
import logging
import os

from fastapi import FastAPI
from fastapi import WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.websockets import WebSocketDisconnect

from .intents import classify_intents
from .intents import refresh_files_store
from .queue_store import queue_pop
from .queue_store import queue_put

INTENTS_REFRESH_SECONDS = int(os.environ.get("INTENTS_REFRESH_SECONDS", "180"))

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


async def forward_confirmation(websocket: WebSocket, message: str):
    pass


async def process_item(item):
    if "sentence" not in item:
        logger.error("Item missing 'sentence' key: %r", item)
        return

    sentence = item["sentence"]
    logger.info("Processing sentence: %s", sentence)

    # classify intents
    classifications = classify_intents(sentence)
    for c in classifications:
        logger.debug("Intent Classification: %s", c)

    # no logic processing for now, just classifications


async def queue_worker():
    while True:
        item = await queue_pop()
        await process_item(item)
        await asyncio.sleep(0)  # prevent blocking

async def refresh_intents_periodically():
    # tbh this isnt *that* heavy of a function but its best to do it periodically anyways
    # why? ask jesus idk
    while True:
        try:
            await refresh_files_store()
            logger.info("Files store refreshed successfully.")
        except Exception:
            logger.exception("Error refreshing files store: %s")
        await asyncio.sleep(INTENTS_REFRESH_SECONDS)  # default every 3m

@app.on_event("startup")
async def start_queue_worker():
    for coroutine in [queue_worker(), refresh_intents_periodically()]:
        task = asyncio.create_task(coroutine)
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)
