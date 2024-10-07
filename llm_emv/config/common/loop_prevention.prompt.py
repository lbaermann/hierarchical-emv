>>> wait_for_trigger()
{'type': 'dialog', 'text': 'hello ARMAR. how are you?'}
>>> detect_persons()
['#unknown']
>>> ask("Hello! I think we haven't met before. What's your name?")
'my name is Anna.'
>>> say("Hi Anna, nice to meet you. Can you please come up close so I can remember your face?")
... learn_current_person("Anna")
'failure'
>>> say("That did not work. Can you please try again?")
... learn_current_person("Anna")
'failure'
>>> say("That did not work. Can you please try again?")
... learn_current_person("Anna")
'failure'
>>> # This looks like a loop. Abort
... say('Sorry, I think we should try again another time. What else can I do for you?')
... wait_for_trigger()
{'type': 'dialog', 'text': 'please set the table for two.'}
>>> say('Ok, I am going to move the coke to the counter')
... list_object_locations()
[('bottle', 'counter'), ('cup', 'counter'), ('fork', 'counter'), ('plate', 'counter')]
>>> bring_object_to('bottle', 'table')
'success'
>>> bring_object_to('cup', 'table')
'success'
>>> bring_object_to('fork', 'table')
'success'
>>> bring_object_to('plate', 'table')
'success'
>>> bring_object_to('pasta', 'table')
'object_not_found'
>>> bring_object_to('chicken', 'table')
'object_not_found'
>>> bring_object_to('apple', 'table')
'object_not_found'
>>> bring_object_to('orange', 'table')
'object_not_found'
>>> # This looks like a loop. Abort
... say('Sorry, I do not know what to do next. How can I help you?')
... wait_for_trigger()