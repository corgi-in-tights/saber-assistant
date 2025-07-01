Tuesday, June 31, 2025
(its close enough im just making a new devlog)

SCRAP EVERYTHING

Did a lot more research. Realized all of this probably exists in a way better format. It does.

Still doing this, I don't like what's avaliable online. LeonAI and SEPIA are the two best options I found and.. meh, some things here and there (obviously way more complex than anything I could make right now still). My original idea:

Whisper (some STT) -> Declaratives -> Logic consumer <-> Home Assistant 
                                            |
                                            v
                                         some TTS
New idea:   
Merge declaratives and logic consumer into one app: Saber. I don't have the tech to host everything locally yet, so it needs to support both options.

Saber needs to be an API built to be fully dockerized. I like how Jellyfin and the others do it, super neat.

Device layer: Scrapping a bit of the device layer for now. Gonna couple with Home Assistant a bit tightly, but leave the functions open.


Intent classification layer: Was the declaration layer, this name fits way better. Accepts a sentence and returns the intents. Unsure of whether I'll build this and wrap a LLM or use a pre-existing one. Probably the latter. Current rule-based ML implementations seem a little weak for my purposes (like SEPIA) but there are some really good open source ones -- though then I have to find an external host? Maybe rent a server. 

I think using a finetuned LLM with a bunch of options would work nicely, and return the output as JSON in the SEPIA-style format. Two runs same as before, first to identify intents and the second to fill in the slots of each intent.


Logic layer: Use the device layer and intent classification layer to communicate with linked services (each intent has a linked service) in any manner. Saber also needs to be able to accept partial and real-time streaming, even if that'll never come to use. So, websocket.

11:54PM (still june 30th technically): For now it wont do streaming, something to the consider in the future. Just HTTP FastAPI for now.

1:26AM: Setup the FastAPI websocket (yeah we're using websockets now).