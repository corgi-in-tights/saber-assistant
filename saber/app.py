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
            logger.debug("Received data: %r", data)
            if not data or not isinstance(data, dict):
                continue
            if "sentence" not in data:
                await websocket.send_text("Invalid data format. Expected 'sentence' key.")
                continue

            await queue_put(data)
            await websocket.send_text(f"Received: {data['sentence']}")

    except WebSocketDisconnect:
        logger.debug("Client disconnected")
    finally:
        clients.remove(websocket)



async def process_item(item):
    if "sentence" not in item:
        logger.error("Item missing 'sentence' key: %r", item)
        return

    sentence = item["sentence"]
    logger.info("Processing sentence: %s", sentence)

    # fetch all pre-category context providers by config_store.py
    # run them all to get a dict of pre-contexts (pass sentence)

    # fetch all category classifiers by config_store.py
    # pass sentence + dict of pre-contexts to each classifier
    # get list of intents with each having a confidence score of 0.8 or higher

    # fetch all post-category context providers by config_store.py
    # run them all to get a dict of post-contexts (pass sentence)

    # fetch all intent classifiers by config_store.py
    # pass sentence + dict of pre-contexts + dict of post-contexts to each classifier
    # run them all until one returns a list of intents with each having a confidence score of 0.8 or higher

    # fetch the skills attached to each intent, run in order of confidence score
    # allow skills to directly send responses to attached clients via the send method
    # response format is:
    """
    {
        "response_type": "deferral" | "message" | "nonverbal",
        "value": "string" | {"key": "value"},
        "additional_data": {"key": "value"}  # optional, for any extra data
        "sentence": ""
        "intent": "intent_name",  # the intent that triggered this response
        "confidence": 0.8,  # the confidence score of the intent
        "slots": {"slot_name": "value"}  # optional, for any slots extracted from the sentence
    }
    """


async def queue_worker():
    while True:
        item = await queue_pop()
        await process_item(item)
        await asyncio.sleep(0)  # prevent blocking

# sample config refresh thing
# need to add dir watch to configs/ and reload configs on change
async def refresh_intents_periodically():
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
