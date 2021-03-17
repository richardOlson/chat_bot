# This is the file where we just try things to see how they work

import spacy


# Trying to use spacy to do the work
nlp = spacy.load("en_core_web_md")

# The following is the list of items that we would like to remove from the text
remove = {

    "^":"^",
    



}
"&gt; a subreddit which focuses on Palestine, its people and culture    False. Israel hate is the sub's main focus. Just as the PLO was created in Cairo to destroy Israel, r/Palestine exists for circle-jerking about Israeli policy."
remove_list = [ "r/", "u/", ]

def remove_char(string:str ):
    if string in remove:
            # will add to the set the items in the 
        return True
    else:
        return False
# doing the 


# making the responce cleaner 
def responce_cleaner(string):
    """ 
    This function will take in a string and then will remove things such as the brackets
    or emojis.
    """
    remove_list = [ "r/", "u/", ]
    # making the doc with the spacy
    doc = nlp(string)
    theSet = set()
    # this is a list of things to add to the set at the end
    for i in range(len(doc)):
        if doc[i].text == "("  or doc[i].text == "&" and i < len(doc)-1:
            if doc[i +1].text == "https":
                # will remove everthing till we hit the next )
                index = string.find(")", start=i+1, )
                # now cutting out the slice
                string = string[:i] + string[index +1:]
                i = index
                continue
            else:
                remove_list += ["&gt;", "&lt;"]
            
                
        elif not doc[i].is_ascii or (doc[i].is_bracket and not doc[i].is_punct) or remove_char(doc[i].text):
            theSet.update(doc[i].text)
    theSet.update(remove_list)
    # now adding the list of the ones to remove if found
    
    for item in theSet:
        string = string.replace(item, "")
    return string
# then converting it back to a text

#b = [word.lower_ for word in v]




if __name__ == "__main__":

    # s = ["y", "I ", "[Wwant","to", "Say", "?"]
    # t = "Man I think that this is something that is awesome]!"
    v = "Are you..... Princess??? 😱😱😱😱😱😂😝"
    t =  "It's pretty great!      ~~lol no worries, not sarcasm. the name's just based off of the Echoes character~~"
    x = "もうすでに一回下って甲殻類アレルギーになったからね許してくれてもいいよね"
    z = "[This was the chosen flag in 1931, which is probably of better quality](https://commons.wikimedia.org/wiki/File:1931_Flag_of_India.svg)"
    q = "&gt; a subreddit which focuses on Palestine, its people and culture    False. Israel hate is the sub's main focus. Just as the PLO was created in Cairo to destroy Israel, r/Palestine exists for circle-jerking about Israeli policy."

    #print("Doing x ", responce_cleaner(x))
    #print(f"Doing v  {responce_cleaner(v)}")
    print(f"Doing z  {responce_cleaner(z)}")

    print(f"printing out the tokens of this &gt hi how are you?")
    doc = nlp("&gt hi how are you?")
    for token in doc:
        print(token)
