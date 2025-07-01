# ruff: noqa
# how i envision the most basic usage
from smart_home_declaratives import get_declarations

sentence = "Turn the kitchen lights on, and set a timer for 45 seconds for the oven."

declarations = get_declarations(sentence)
for declaration in declarations:
    print(declaration)
    
# This will print:
# State 293 ON (or whatever the ID of the kitchen lights device is)
# Timer 45s 'oven timer'

# the most complicated thing is passing context, TODO: figure this out lol
