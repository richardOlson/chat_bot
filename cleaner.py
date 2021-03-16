# This is the file where we just try things to see how they work

import spacy


# Trying to use spacy to do the work
nlp = spacy.load("en_core_web_md")

s = ["y", "I ", "[Wwant","to", "Say", "?"]
t = "Man I think that this is something that is awesome]!"
v = "Are you..... Princess??? 😱😱😱😱😱😂😝"
doc1 = nlp(t)
doc2 = nlp(v)

def notin(string:str):
    if string.isalpha or string.isnumeric:
        return True
    return False
# doing the 
a = [word.lower_ for word in doc2 if word.is_ascii and  not word.is_bracket and not word.is_punct]
string = " ".join(a)
# then converting it back to a text

#b = [word.lower_ for word in v]
print(s)
# now making the word back into the word and not the tokens
print(string)
# retokenizing the string
doc3 = nlp(string)
# printing the tokens of the document
for token in doc3:
    print(token.text)