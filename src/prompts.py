from typing import *

'''
    user: e.g. "beginner spanish learner", etc
    context: {article text}
    word: e.g. "antiquated"
'''
def context_window() -> Dict[str, str]:
    '''
    Returns an instruction context window
    '''

    cwi = """
Linguist Tailor is a highly precise, multilingual language tool designed to identify only truly complex words for a specific target user. It meticulously processes input in various languages, tailoring its analysis to accurately determine which words are difficult based on the individual's language proficiency, age, or other relevant characteristics. This tool is committed to restricting its output to only those words that are genuinely complex for the user, ensuring maximum relevance and accuracy. If no complex words are identified, Linguist Tailor will return a "NULL". Outputs are formatted as a string of words separated by commas. This focus on delivering highly specific and accurate linguistic analysis, tailored to each user's needs, makes Linguist Tailor an effective tool for users requiring detailed, user-centric language assessment.
    """# from openai editor
    
    output = {
        'cwi': cwi
    }

    return output

def return_cwi(user, context, language="Spanish") -> Dict[str, str]:
    zero_shot = f"User: {user}\n\n" \
                f"Context: {context}\n\n" \
                f"Question: Given the above context, list {language} words or phrases in the context that may be difficult to understand for the user.\n" \
                f"Answer:"
    
    output = {
        'zero_shot': zero_shot,
    }

    return output
    
def return_sg(user, context, word, language="Spanish") -> Dict[str, str]:
    zero_shot = f"User: {user}\n\n" \
                f"Context: {context}\n\n" \
                f"Question: Given the above context, list ten alternative {language} words or phrases for \"{word}\" that are easier to understand for the user while keeping the original meaning of the context\n" \
                f"Answer:"
    
    output = {
        'zero_shot': zero_shot,
    }

    return output

def clean_output(self, text):
    pass