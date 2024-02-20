import string 
from nltk.corpus import stopwords
import re

def cleanString(text):
    text = ''.join([word for word in text if word not in string.punctuation])
    text = text.lower()
    text = ' '.join([word for word in text.split() if word not in stopwords])
    return text
def get_url(string):
    match = re.search("(?P<url>https?://[^\s]+)", string)
    if match:
        return match.group("url")
    else:
        return None
def save_kb(kb, KBURI):
    with open(KBURI, "w") as f:
        for assertion in kb:
            f.write(str(assertion) + "\n")   
def get_last_word(text):
    """
    Given a string `text`, this function returns the last word in the string.
    """
    # Split the text into words
    words = text.split()

    # Check if there are any words in the text
    if len(words) == 0:
        return None

    # Return the last word
    return words[-1]