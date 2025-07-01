Monday, June 30, 2025.

This project is a lot more.. thinking than coding. Physical notebook ran out of space. Lol.

I've been trying to build my own Alexa-esque assistant pretty much, this project is something I was gonna get around to anyways, decided to make a public library out of it. Essentially:

- Take in a human sentence ("bro please help someone turn the lights off im scared")
- Accept contextual data
- Return a list of human-readable and machine-parseable 'declarations' ("turn \[device\] off")
- Throw some HA-intergration in there

For obvious reasons, I have to state that this will get nowhere close to the insanity of Alexa/Google Hub. The streaming and real-time processing tech they have is a *bit* above me. Pretty sure it does NLU processing on partial transcripts half-way through your sentence. WTF.


The main issues here are customizability and LLM limits.
1. The token limit. Passing context is a pain, a bit of scrabble and you realize the context tends to exceed the token limit once it gets large enough. What kind of "customizable" project is this if someone can't have a mansion full of smart devices and use this project with it? This means optimizing and allowing the LLM to request context, which complicates things.

2. Commands and routines. Everyone has different ideas of what they want, if a user tells their.. VA? to make a website, it better make a damn website. Which means no hard-coding. Need a system to group together keywords, recognize statements for what they are, use device IDs, all that jazz, while trying to minimize costs.

My current idea is this:
- User requests declaration with sentences and passes three types of contexts: Global, user and device. Ideally, these can carry over to the next part of this scheme to help with responses. Each.. type? has a whole thing. Questions may require the internet, things can be compound, a statement can have implicit things (ie brightness 100% requires the light to be turned ON as well, can't always expect the actual zigbee management software to recognize that).

- The first pass breaks down the target sentence into different types of declarations. Like, "Turn the timer on for 2 minutes" is "Timer 2m". Note that timer and alarm are seperate types entirely. These types have to be configurable.

- The next pass is optional, for questions, it does nothing, but for stuff like attributes/state changes (brightness or literally on/off) it needs to be broken down and match to the device id. So 'kitchen lights' has to translate to entity ID light.kitchen from a list of sorts. 

I like to think the first pass is the 'recognition pass', then the second the 'substitution pass'. Each type will be configurable via Python classes.

- Simply then return the list of declarations as a future. 


Currently the lib will just try to pass as relevant context as possible and pray its enough. There's really just a crazy amount of context. Just attribute/states alone require the list of groups, devices in those groups, their IDs, current states/attributes and all -- which means like 4~8 lines for a single device (anyone using this will have like 20+). 

Thinking of making the requesting another pass or happen in the recognition pass, not sure how much it'll interfere, tests are required. 

Oh yeah. Also, it's going to need compat. with pre-existing stuff like Home Assistant to get a list of all the devices in the correct format. Fun. Shit.

For today I think I'll work on creating the basic OOP stuff, so like, groups, whatnot.


7:42PM: Done with devices/device.py, pretty happy with how it is, pretty basic but had some thought to it OK :()

7:52PM: Done with devices/group.py (really wasn't much lol)


..considering bundling the device layer into its own library, since I'm thinking of making *another* abstraction for home assistant. Yeah. Work.


For the MVP thinking of making a basic spotlight-like app. Press CMD+B, opens a search bar, just type your sentence in, press enter, bam it happens. Wake word recognition and STT not really required just as of yet (though definitely do plan on it). That means four things:
- Frontend app
- Declaration maker (what i'm currently working on)
- Declaration parser/the actual logic
- Backends like home assistant for device management or some internet-enabled LLM for questions.

why have i decided to torture myself with work, oh why.

10:24PM: Been trying to come up with a general name since the scope is getting larger, not getting anywhere. 

Was thinking something nerdy, like a reference to Dune mentats (but from thufir import get_declaratives is just weird). Something starting with J would also be nice (honorary jarvis reference). This isn't really too relevant thought taking a quick 10 or so minutes out to get a decent name would be useful in the long run.

Decided on Saber. Why? It sounds cool and I like sabre more than epée. Also, American spelling, why not?
