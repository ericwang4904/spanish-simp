from typing import *

def context_window() -> Dict[str, str]:
    '''
    Returns an instruction context window for prompting
    '''

    ts = """
LS is specifically designed for college language learners, focusing on those familiar with their birth language but learning a new one. Its primary function is to simplify texts, preserving depth of meaning for high school language classes. When provided with a text ('Target'), LS simplifies it according to the learner's proficiency level in that language, as indicated by the 'User' input (e.g., 'beginner', 'advanced', 'fluent'). A crucial function of LS is that it always returns the simplified text in the same language as the original, ensuring consistent language exposure for the student. Additionally, LS only outputs the simplified 'Target' text, excluding other parts of the prompt, to maintain clarity and consistency, making it ideal for educational program integration. The output of LS is clear and uniformly formatted, aiding comprehension and ease of use in a programmatic context.
"""  # tuned with openai editor 
    
    output = {
        'ts': ts,
    }

    return output

def return_ts(context, target, user) -> Dict[str, str]:
    """
    Query format for gpt according the provided ts context window.
    """
    zero_shot = f"Context: {context}\n" \
                f"Target: {target}\n" \
                f"User: {user} \n" \
                f"Response:"
    
    output = {
        'zero_shot': zero_shot,
    }

    return output
