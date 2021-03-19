# This is the file where we just try things to see how they work






# The following is the list of items that we would like to remove from the text
remove = {

    "^":"^",
    "[":"[",
    "]":"]", 
    "\r":"\r",
    "\n":"\n", 
    
    



}
"&gt; a subreddit which focuses on Palestine, its people and culture    False. Israel hate is the sub's main focus. Just as the PLO was created in Cairo to destroy Israel, r/Palestine exists for circle-jerking about Israeli policy."
remove_list = [ "r/", "u/", "*" ]

def remove_char(string:str ):
    if string in remove:
            # will add to the set the items in the 
        return True
    else:
        return False
# doing the 




def cutting(front:tuple, back:tuple, string:str):
    """
    This is the funtion that will do the cutting of the string and then
    will return the string with the cut out of it
    """
    
   
    string = string[front[0]:front[1]] + string[back[0]: back[1]]
    return string



# making the responce cleaner 
def text_cleaner(string):
    """ 
    This function will take in a string and then will remove things such as the brackets
    or emojis.
    """
    remove_list = [ "r/", "u/", ]
    # This is the flag that when true means that need to cut out the https region
    cut_flag = False
    # These are the cut points to cut the string this is to remove the https region
    front = None
    back = None
    theSet = set()
    # this is a list of things to add to the set at the end
    for i in range(len(string)):
        
        if string[i] == "("  or string[i] == "&" and i < len(string)-1:
            if string[i +1: i+6] == "https":
                # will remove everthing till we hit the next )
                index = string.find(")", i+1 )
                if index != -1:
                    # setting up the cutting flac an the cuts
                    cut_flag = True
                    front = (0,i)
                    back = (index,len(string)-1)
                    if index == len(string)-1:
                        break
                    continue
            else:
                if string[i:i+4] == "&gt;":
                    remove_list += ["&gt;"]
                elif string[i:i+4] == "&lt;":
                    remove_list += ["&lt;"]
            
               
        elif not string[i].isascii() or remove_char(string[i]):
            theSet.update(string[i])
    theSet.update(remove_list)
    if cut_flag:
        # now doing the cutting
        string = cutting(front=front, back=back, string=string)
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
    a = "ok that makes more sense &lt;3"
    b = "r/wholesomeouija"

    print("Doing x ", text_cleaner(x))
    print(f"Doing v  {text_cleaner(v)}")
    print(f"Doing z  {text_cleaner(z)}")
    print(f"Doing a  {text_cleaner(a)}")
    print(f"Doing b {text_cleaner(b)}")

    # print(f"printing out the tokens of this &gt hi how are you?")
    # doc = nlp("&gt hi how are you?")
    # for token in doc:
    #     print(token)

