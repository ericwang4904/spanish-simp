### Documentation:
After configuring your API key in to config.py (see config.py.template), you may begin using the program. Documentation is included for all functions. Sample inputs are availible in main.py. See Todo section for improving functionality.


**How it works:**
[s1, s2, ... ] -> turned into groups
[g1, g2, ...] -> some portion is simplifed
[sg4, sg5] -> the global variable for simplified groups is updated
[g1, g2, g3, sg4, sg5, ...]

revert function: allows you to revert a specific range in s_group_tokens to their originals in group_tokens
redo function: revert writes the changed section to a buffer, and this buffer can be used to undo the revert

### Todo
**What?** 
- Writing a Web UI using Flask (Priority 0)
**What should it include?**
- Be easy to use 
- Undo functionality (functionality already provided in model.py via old_s)
- Ability to revert and re-simplify specific parts of the text
  - This would require a change to the way groups of sentences are processed. Right now, they are regenerated each simplification (so if the simplifed version has fewer or more sentences the token groups will be shifted, making it impossible to revert a specific token group).
    - Possible solution: store indexes along with token groups, with the indexes corresponding to the original text
- Ability to save stored text (copy to clipboard or as a file)


**What?** 
- Improving prompt engineering (Priority 1)
**How?** 
- chat.openai.com/gpts/editor (needs subscription) allows you to tune the GPT context window to improve output
- Maybe add an optional part in the query allowing for user input? (e.g. "Write this section in a sad tone")
- main.py has "params" and "openai_params" that dictate how GPT returns responses. These can be set to good values 
  - (maybe one set is for "standard", another for "risky", and another for "short", etc.?)

**What**
- multiple rounds of simplification/back and forth? (Priority 2)
**How?**
- openai's abiity to continue a conversation (see openai docs)
- changing the way simplified text is stored to allow for inputting simplifed text into gpt
