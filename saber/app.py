import asyncio
import logging
import os

from fastapi import FastAPI
from fastapi import WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.websockets import WebSocketDisconnect

from .config_store import config
from .config_store import initialize_configs
from .queue_store import queue_pop
from .queue_store import queue_put

MINIMUM_UNCLASSIFIED_LENGTH = int(os.environ.get("MINIMUM_UNCLASSIFIED_LENGTH", "2"))

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
    if not item:
        return
    if "sentence" not in item:
        logger.error("Item missing 'sentence' key: %r", item)
        return

    sentence = item["sentence"]
    logger.info("Processing sentence: %s", sentence)

    logger.debug("Using classifiers: %r", config.intent_classifiers)
    logger.debug("Using context providers: %r", config.context_providers)

    # process each classifier
    # TODO: make this use interfaces? idk, currently just assumes each key exists
    for classifier_data in config.intent_classifiers:
        contexts = {}
        if "context_providers" in classifier_data:
            for context_provider_name in classifier_data["context_providers"]:
                context_provider = config.context_providers[context_provider_name]["class"]()
                data = await context_provider.get_context(item, {})
                if not data:
                    logger.warning("No context data returned from %s", context_provider_name)
                    continue

                logger.debug("Context from %s: %r", context_provider_name, data)
                contexts[context_provider_name] = data

        classifier = classifier_data["class"]()
        classified_data = await (classifier.classify(sentence, contexts))

        logger.debug("Intents from %s: %r", classifier_data["name"], classified_data)

        for intent in classified_data:
            logger.debug("Processing intent: %r", intent)

        # sentence is fully classified with a confidence score of 0.8+
        # TODO: make this configurable & add confidence scores
        unclassified_sentence = classified_data["sentence"]
        if len(unclassified_sentence) < MINIMUM_UNCLASSIFIED_LENGTH:
            break


async def queue_worker():
    while True:
        item = await queue_pop()
        await process_item(item)
        await asyncio.sleep(0)  # prevent blocking


@app.on_event("startup")
async def startup_sequence():
    await initialize_configs()

    logger.info("Starting queue worker background task.")
    task = asyncio.create_task(queue_worker())
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)
