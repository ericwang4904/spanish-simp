<<<<<<< HEAD
## Reqs
```
pip install flask
pip install python-dotenv
pip install -U spacy
pip install wheel
```
follow `https://github.com/danielibanezgarcia/less`
    `https://freeling-user-manual.readthedocs.io/en/v4.2/installation/requirements-mac/`
    `https://github.com/AdoptOpenJDK/homebrew-openjdk`
        `brew install --cask temurin8`
    `pip install JPype1 jvm`
    `pip install uralicNLP` <– important; I modified the less code to use this

have to edit:
    change `config.py` path to `/Library/Java/JavaVirtualMachines/temurin-11.jdk/Contents/Home/lib/server/libjvm.dylib` or similar

circumventing current weirdness:
   - version of pyYAML project uses doesn't support cpython3.0 so you have to `pip install "cython<3.0.0" && pip install --no-build-isolation pyyaml==5.4.1`
   - 
=======
### Documentation:
After configuring your API key in to config.py (see config.py.template), you may begin using the program. Documentation is included for all functions. Sample inputs are availible in main.py. See Todo section for improving functionality.
>>>>>>> 81f2f263213461503535818cfb4a7f34fc47d4cc


**How it works:**
text is tokenized into sentences ->
[s1, s2, ... ] is turned into groups ->
[g1, g2, ...] and some portion is simplifed -> 
[sg2, sg4, sg5] which updates the global variable for simplified groups -> 
[g1, sg2, g3, sg4, sg5, ...]

### Todo

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
  - The current method in TS.context_window() uses the original text aways; modified versions could somehow have options to refeed simplified texts with comments/etc (the optional part mentioned in Improving prompt engineering)
