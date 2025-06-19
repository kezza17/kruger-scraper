import string

def normalize(text):
    # Replace dashes and slashes with space, remove other punctuation
    text = text.lower().replace("-", " ").replace("/", " ").replace("'", "")
    text = text.translate(str.maketrans('', '', string.punctuation))
    return f" {text} "

def find_phrase(lookup, desc):
    desc_norm = normalize(desc)
    for key, phrases in lookup.items():
        for phrase in phrases:
            phrase_norm = normalize(phrase)
            if phrase_norm in desc_norm:
                return key, phrase  # return original (not normalized) for clean replacement
    return None, None