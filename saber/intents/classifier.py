def classify_intents(sentence: str):
    """
    Classify the given sentence into intents.
    This is a placeholder function that should be replaced with actual intent classification logic.
    """
    # recognize most common commands using elastisearch or similar
    # "Daylight on"

    # then resort to LLM

    # For now, we return a dummy classification
    return [{"intent": "dummy_intent", "confidence": 0.9, "sentence": sentence}]
