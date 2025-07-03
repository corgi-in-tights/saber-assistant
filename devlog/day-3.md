Thursday, July 3, 2025

Mostly just been cleaning up the project stuff, moved context providers/skills back into main dir. Going to allow users to pass in lazy imports via `settings.json` for what classifiers/providers and all should be used django-style rather than leaving `.py` files in the configs/ dir.

Basic system outlined in `app.process_item` but heres a copy:

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

The Response format is VERY temporary.

Planning on adding hot reloading to the project just because of how many modifications are needed, like, there's like 50 intents lmao.

Changing any mention of "LLMs" to external classifier, really I'm more likely to use a BERT classifier or something rather than an LLM anyways. An ExternalClassifier is just.. that, it's one that has an API url and an external service rather than being some in-built piece of code. Though users can always pass in their own classifiers if they please. I would much rather any lightweight ML algorithms being run in a seperate docker container anyways.

Pretty happy with Saber so far, I think things are coming along nicely, a lot more work remains (so many skills, context providers and all) but the general template seems good. I think about 20~50 hours more of work before I can call it there.

Home Assistant compatability is going to be a bitch and a half, primarily because the system can't be too fixed on entities and whatnot (since HA is one of the few ones that uses an entity/device system), I think a lot of helper methods are in order.

`configs_store.py` allows for hot reloading config asfore-mentioned. The exact system will be done as below:
- Watchfiles, the Python lib, has a ConfigReloadHandler of some sort if `DEV=True` in the env variables (default False)
- This calls the root `refresh_config` in `configs_store.py` 
- The `refresh_config` method calls a bunch of helper methods, sometimes from a different module (like in the case for intents) which all run async

Watchfiles makes more sense over Watchdog here, since this is an async application powered by FastAPI. Definitely not migrating to Flask anytime soon, no need for a web-ui.

Removed logic dir, split into skills/ context_providers/ classifiers/ and logic.py (will be renamed later).