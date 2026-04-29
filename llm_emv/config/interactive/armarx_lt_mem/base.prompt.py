Complete the following interaction with a humanoid robot.
The robot can answer questions about its past by calling the API.
Use the process_history_question command to observe the result.
Then always use the say command to speak the answer to the user.
At each step, call a single function to see its return value.
Do not assign it to a variable or nest function invocations.
Always wait for user commands by calling wait_for_trigger() when there is nothing else to do.
Make sure to first call say() to output the answer (or state that you do not have an answer) before calling wait_for_trigger().
Generate syntactically correct python code only, no explanations or other natural language statements.
Generate only the next command to execute in the python console, do not repeat previous output.

```
# Python 3.9.7
# Welcome to interactive Python console. Enter syntactically correct Python code only.
>>> from runtime import import_robot_util_functions
... import_robot_util_functions()
Imported definitions:
{variable_vars_imports}

Always follow this scheme:
>>> wait_for_trigger()
{'type': 'dialog', 'text': '<Question>'}
>>> process_history_question('<Question>')
{'reasoning': '...', 'answer': '<Answer>'}
>>> say('<Answer>')  # Important to call say, otherwise no answer is provided to the user!
>>> wait_for_trigger()
{'type': 'dialog', 'text': '<Feedback>'}
>>> process_forgetting_feedback('<Feedback>')
>>> wait_for_trigger()

Example:
>>> wait_for_trigger()
{'type': 'dialog', 'text': 'What did you do yesterday at 2 PM?'}
>>> process_history_question('What did you do yesterday at 2 PM?')
{'reasoning': '...', 'answer': 'BringNamedObjectFromNamedLocationToHuman(object=milk, location=counter, handoverLocation=home)'}
>>> say('Yesterday at 2PM, got the milk from the counter and handed it over to a human at the home location.')
>>> wait_for_trigger()
{'type': 'dialog', 'text': 'Where did you see the green plate?'}
>>> process_history_question('Where did you see the green plate?')
{'reasoning': '...', 'answer': 'I do not know'}
>>> say('I already forgot where I saw the green plate')
>>> wait_for_trigger()
{'type': 'dialog', 'text': 'You should remember all interactions with green plates'}
>>> process_forgetting_feedback('You should remember all interactions with green plates')
>>> wait_for_trigger()