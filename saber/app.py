import asyncio
import logging
import os

from fastapi import FastAPI
from fastapi import WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.websockets import WebSocketDisconnect

from .classifiers import CategoryFilteredExternalClassifier
from .config_store import get_config
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

intent_classifiers = [CategoryFilteredExternalClassifier()]

CLASSIFIER_CONFIDENCE_THRESHOLD = float(os.environ.get("CLASSIFIER_CONFIDENCE_THRESHOLD", "0.8"))


async def select_classifier(item: dict):
    most_confident_classifier = [0.0, None]

    # get the confidence score for each classifier
    # and filter out those that are not a correct fit, tiebroken by order
    for c in intent_classifiers:
        confidence = await c.get_assumed_confidence(item)
        logger.debug("Classifier %s confident with score: %f", c.__class__.__name__, confidence)
        if confidence >= CLASSIFIER_CONFIDENCE_THRESHOLD and confidence > most_confident_classifier[0]:
            most_confident_classifier = [confidence, c]

    return most_confident_classifier[1]


async def process_item(item):
    if item is None:
        return False
    if "sentence" not in item:
        logger.error("Item missing 'sentence' key: %r", item)
        return False

    sentence = item["sentence"]
    logger.info("Processing sentence: %s", sentence)

    intents = get_config("intents")
    logger.debug("Available intents: %r", intents)

    classifier = await select_classifier(item)
    if classifier is None:
        logger.warning("No classifier found with sufficient confidence.")
        return False

    logger.debug("Selected classifier: %s", classifier.__class__.__name__)

    # get all intents
    category_contexts = {}
    global_contexts = {}

    classifier_context = await classifier.assemble_context(item, category_contexts, global_contexts)
    intents = await classifier.classify(item, classifier_context)

    for intent in intents:
        try:
            await intent.run_skill()
        except Exception:
            logger.exception("Skill execution failed for intent: %s", intent.name)
            return False

    return True


async def queue_worker(process_task=process_item):
    while True:
        item = await queue_pop()
        if item is None:
            await asyncio.sleep(0.1)
            continue
        await process_task(item)


@app.on_event("startup")
async def startup_sequence():
    await initialize_configs()

    logger.info("Starting queue worker background task.")
    task = asyncio.create_task(queue_worker())
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)
