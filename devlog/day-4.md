July 12, 2025

Responses and response chaining are the biggest two problems needed to be tackled now. 

I think Responses are pretty easy, SaberSkill can have a method called `send_response`, since the target websocket is attached to the initial data package, its pretty easy to communicate.

Taking in responses is a bit harder, ideally this should work with the initial-response system instead of having a new one.

When a request is recieved, it is tossed into a queue. When processed, tagged with an ID and stored into a KV table like Redis IF the skill marks the request as a question, skills will wait upto TIMEOUT_SECONDS by default. Ideally, this system can dynamically be used to fill up slots. Maybe something like:

```python
await question_fill_slot("alarm", "What time would you like to set an alarm for?" slots)

await self.send_response(Beep())

try:
    response = await self.ask_question(
        Message("What time would you like to set an alarm for?"),
        attempts=1,
    )
    await self.send_response(Message(f"Okay, alarm set for {response}"))
except TimeoutError:
    await self.cancel()
```



