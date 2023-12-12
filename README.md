### Documentation:
After configuring your API key in to config.py (see config.py.template), you may begin using the program. Documentation is included for all functions. Sample inputs are availible in main.py. See Todo section for improving functionality.

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
**How it works in detail (needed for writing better code)**
1. [sentence1, sentence2, ...] become [group1-3, group4-6, ...] (with group_len = 3)
2. Parts of [group1-3, group4-6, ...] are simplifed (e.g. [group4-6, group7-9])
3. The simplified groups replace the originals (even if they have more or fewer sentences then group_len)
4. The list of groups is joined into one simplified text
5. The simplifed text is tokenized into new tokens, which are formed into new groups.

**What?** 
- Improving prompt engineering (Priority 1)
**How?** 
- chat.openai.com/gpts/editor allows you to tune the GPT context window to improve output
- main.py has "params" and "openai_params" that dictate how GPT returns responses. These can be set to good values 
  - (maybe one set is for "standard", another for "risky", and another for "short", etc.?)

