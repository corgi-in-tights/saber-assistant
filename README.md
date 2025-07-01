# smart-home-declaratives

A Python library designed to aid in the creation smart home virtual assistants. Mainly, optimizing passing only the relevant context to the LLM.

Accepts general sentences and contextual information:
"Turn the kitchen lights on, and set a timer for 45 seconds for the oven."

And (asynchronously) returns declarations:
- "State 293 ON" (or whatever the ID of the kitchen lights device is)
- "Timer 45s 'oven timer'"

Supports any LLM API and wholly customizable. Built using fastapi.


Examples:
TBD


