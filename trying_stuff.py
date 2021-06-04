# just a file to try things

import pandas as pd
import os
from pathlib import Path
import re


# printing out the working directory 
print(f"The currrent dirctory is --> {os.getcwd()}")

def get_yoda_corpus():
    theHomePath = str(Path.home())
    # know making it to the path
    fullPath = os.path.join(theHomePath, "Downloads", "yoda/yoda-corpus.csv")
    # Changing the directory
    # os.chdir(theHomePath)
    # printing out the new directory 
    # print(f"This is the new directory ---> {os.getcwd()}")
    df = pd.read_csv(fullPath)
    return df




# seeing how this will work
from itertools import chain

# Let's define our contexts and special tokens
persona = [["i", "like", "playing", "football", "."],
           ["i", "am", "from", "NYC", "."]]
history = [["hello", "how", "are", "you", "?"],
           ["i", "am", "fine", "thanks", "."]]
reply = ["great", "to", "hear"]
bos, eos, speaker1, speaker2 = "<bos>", "<eos>", "<yoda>", "<other_speakers>"

def build_inputs(persona, history, reply):
    
    # Build our sequence by adding delimiters and concatenating
    sequence = [[bos] + list(chain(*persona))] + history + [reply + [eos]]
    sequence = [sequence[0]] + [ [speaker2 if (len(sequence)-i) % 2 else speaker1] + s
                                for i, s in enumerate(sequence[1:])]
    # Build our word, segments and position inputs from the sequence
    words = list(chain(*sequence))                          # word tokens
    segments = [speaker2 if i % 2 else speaker1             # segment tokens
                for i, s in enumerate(sequence) for _ in s]
    position = list(range(len(words)))                      # position tokens
    return words, segments, position, sequence

words, segments, position, sequence = build_inputs(persona, history, reply)

# >>> print(sequence)  # Our inputs looks like this:
# [['<bos>', 'i', 'like', 'playing', 'football', '.', 'i', 'am', 'from', 'NYC', '.'],
#  ['<speaker1>', 'hello', 'how', 'are', 'you', '?'],
#  ['<speaker2>', 'i', 'am', 'fine', 'thanks', '.'],
#  ['<speaker1>', 'great', 'to', 'hear', '<eos>']]

# this is a function that will get the history and speakers
def get_speakers(speakerList, theInt):
  """
  This will place the speaker for each time that someone has spoken
  """
  theDict = {
      "YODA":"<yoda>",
      "paddington":"<pad>", 
      "other":"<other_speakers>"
  }
  if speakerList[theInt] in theDict:
    return theDict[speakerList[theInt]]
  else:
    return "<other_speakers>"
# This is building with the reversed dataframe

# These are the words -- ['<bos>', 'i', 'like', 'playing', 'football', '.', 'i', 'am', 'from', 'NYC', '.', '<speaker1>', 'hello', 'how', 'are', 'you', '?', '<speaker2>', 'i', 'am', 'fine', 'thanks', '.', '<speaker1>', 'great', 'to', 'hear', '<eos>']
# These are the segments -- ['<speaker1>', '<speaker1>', '<speaker1>', '<speaker1>', '<speaker1>', '<speaker1>', '<speaker1>', '<speaker1>', '<speaker1>', '<speaker1>', '<speaker1>', '<speaker2>', '<speaker2>', '<speaker2>', '<speaker2>', '<speaker2>', '<speaker2>', '<speaker1>', '<speaker1>', '<speaker1>', '<speaker1>', '<speaker1>', '<speaker1>', '<speaker2>', '<speaker2>', '<speaker2>', '<speaker2>', '<speaker2>']
# These are the positions--  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
# These are the sequences -- [['<bos>', 'i', 'like', 'playing', 'football', '.', 'i', 'am', 'from', 'NYC', '.'], ['<speaker1>', 'hello', 'how', 'are', 'you', '?'], ['<speaker2>', 'i', 'am', 'fine', 'thanks', '.'], ['<speaker1>', 'great', 'to', 'hear', '<eos>']]


def prep_inputs_internal(persona, history, reply, speakers = None):
  # this is the inner function that is used to create the 
  # inputs
  # making the sequences first
  # the flag
  
  # making the history a list of list
  history = [h.split() for h in history]

  # making the reply split with the punctuation
  reply = reply.split()
  
  sequence = [[bos] + list(chain(*persona))] + history + [reply + [eos]]
  
  # adding who is talking at each of the points
  yoda, speaker2, pad = "<yoda>", "<other_speakers>", "<pad>"
  
  if speakers != None: # speakers is a list of the speakers that are in the dataframe
    sequence = [sequence[0]] + [[get_speakers(speakers, i )] + s  for i, s in enumerate(sequence[1:])]
  
  # now making the words where everything will be in a single list
  words = list(chain(*sequence))
  
  # building the postion indexes
  # all those that are the persona will have the integer of 0
  the_hist_flag = True  
  theInt = 0
  position = []
  for element in words:
    if the_hist_flag:
        if element in [yoda, speaker2, pad]:
            the_hist_flag = False
        else:
            position.append(0)
            continue
    theInt += 1
    position.append(theInt)
  
  # making the list of speaker tokens
  # theList = [yoda for _ in sequence[0]]

  # for i, s, in enumerate(sequence[1:]):
  #   for _ in s:
  #     theSpeaker = get_speakers(speakers, i)
  #     theList.append(theSpeaker)
  speaker = [yoda for _ in sequence[0]] + [get_speakers(speakers, i) for i, s in enumerate(sequence[1:]) for _ in s]
  # not using the below portion
  
  # speaker = [speaker2 if i % 2 else yoda for i, s in enumerate(sequence) for _ in s]
  return sequence, words, position, speaker

# This is how we are going to prepare the dataset to be the right way
def prepare_inputs(persona: list, history= None, reply= None, dataframe=None):
  # words: -- want to make the sequences where the words is a long list with all the words.
  # speaker -- will be a list of the who is saying what. The element of the speaker will in the same position 
    # as the words
  # position -- this is a list of the where the element is in the words
  # sequence -- this is  a list of list where the inner lists are each of the sentances
  # if the dataframe is present then will cycle through the dataframe row by row
  # and will make the yoda data
  if isinstance(dataframe, pd.DataFrame):
    # doing a loop through each of the rows
    # will be saving the file to the home directory
    # getting the rows from the function prep_inputs_internal
    sequence, words, position, speakers = None, None, None, None
    file_pointers = ["./sequence", "./words", "./position", "./speaker"]

    
    
    for row in dataframe.iterrows():
      # making the history, speakers, words, and the reply
      speakers = row[1].tolist()[:7]

      history = row[1].tolist()[8:-1]
      
      speaker_reply = row[1].tolist()[7:8]
      reply = row[1].tolist()[-1]

      # putting all the speakers in one long list
      speakers = speakers + speaker_reply
      # prep_inputs_internal(persona, history, reply):
      sequence, words, position, speakers = prep_inputs_internal(persona, history, reply, speakers)

      v = [sequence, words, position, speakers]
      # looping through the file pointers
      breakpoint()
      for i, pointer in enumerate(file_pointers):
        # calling the function prepare_intputs_internal
        file_pointer = open(pointer,  mode="ab",  ) 
        if i == 0:
          
          val = "_".join(v[i]) 
          val = val.join(",")
        else:
          val = v[i].join(",")

        file_pointer.write(val)
    

# making the new df that contains the context
def make_new_df(df, reply_at_end= True):
    df = df.copy()
    # now will run through the df and will pull out the text of the last 7 in context
    rows = []
    n = 7
    # find the yoda text in the dataframe
    # will then then go back at least 7
    # need to be of the same scene
    # will add the name of the speaker to the 
    # context column.
    # Will pad those that that don't have enough speakers in the 
    # scene to do 7 -- will put the name of the speaker as paddington for 
    # these.
    for i in range(len(df.index)):
      # outer loop will loop through the whole dataframe
      if df["character"][i] == "YODA":
        scene = df['scene'][i] # getting the scene that all the conversations need to be in
        # going into the inner
        row = []
        speakers = [] # this will be to make the columns that will contain the speaker 
                      # for each of the contexts
        prev = i -n -1
        for j in range(i, prev, -1):
          if j >= 0 and df["scene"][j] == scene: # making sure that the conversations are in the same scene
            row.append(df["text"][j])
            speakers.append(df['character'][j])
        # now will need to find out the length of the 
        if len(row) < 8:
          # need to do some paddington
          row = row + (["pad"] * (8 - len(row)))
          speakers = speakers + (["paddington"] * (8 - len(speakers)))
        row = row + speakers
        
        # option if we want the reply to be and the end of the dataframe instead of at the front of the
        # dataframe
        if reply_at_end:
          row.reverse()

        rows.append(row)

    # beginning of the columns that will be used to make the datafame columns
    columns = ["reply", "saying"]
    # using the same option to make the columns in reversed order to have the reply at the end of the
    # dataframe
    if reply_at_end:
      columns.reverse()
      columns = ["context/" + str(i) for i in range(n-1, 0,  -1)] + columns
      # putting in the reversed of who is speaking 
      columns = [col + "__ " + "speaker" for col in columns] + columns
    
    else:
      # making the full columns -- using 5 of the columns
      columns = columns + ["context/" + str(i) for i in range(n-1)]
      # now making the columns -- for the speakers
      columns = columns + [col + "__" + "speaker" for col in columns]
    # now will make the dataframe
    new_df = pd.DataFrame(rows, columns=columns)

    return new_df


# making a function that will get some of the speech of yoda that is found in the 
# narrator text
def markfixingYodaSpeech(df):
  """
  This function will return a list of the indexes that need to be looked at to decide
  what is to be done to fix the text.  Some times the text of Yoda is in the narrators text.
  
  """
  #df = df.copy()
  theList = []

  for index, row in df.iterrows():
    if row["character"] == "YODA" and index != 0:
      # checking the row above to see if it doesn't end 
      yoda_text = str(row["text"])
      if not yoda_text.endswith(".") and not yoda_text.endswith("?") and not yoda_text.endswith("!"):
        # if it does not end with a period it is possible that 
        # some of Yodas text in in the person (character) that is speaking next.
        theList.append(index)

  return theList


def fixString(s: str):
  """
  This function will return the string
  """
  # this is to remove all the parenthesis and what is in them 
  theList = re.findall(r"\(.*?\)", s, )
  if theList:
    for l in theList:
      s = s.replace(l, "")
  # will now remove the ... and replace it with a comma
  s = s.replace("...", " ,")

  # putting spaces between the punctuation
  theList = re.findall(r"(\.?\??\,?\!?)", s)
  if theList:
    for l in theList:
      if l:
        for theChar in l:
          s = s.replace(theChar, " " + theChar + " ")
  # will now remove places where there are extra spaces
  s = s.replace("  ", " ")
  # will now make everything in lowercase
  s = s.lower()
  
  return s
  



if __name__ == "__main__":

    the_persona = [
               ["yoda", "my", "name", "is","."],
               ["small", "am", "i", "and", "green", "."],
               ["feel", "the", "force", "i", "do", "."], 
              ["control", "our", "fears", "we", "must", "or", "to", "the", "dark", "side", "we", "will", "go", "."],
               ["hard",  "to", "see", "the", "dark", "side", "is", "."]
               
]

    the_history = [
               ["i", "will", "try", "to", "do", "what", "you", "say", "master", "yoda", "."],
               ["do",  "or",  "do", "not", ".",   "there",  "is",  "no",  "try", "."],
               ["you", "are", "so", "small", "how", "do" ,"you", "have", "so", "much", "power", "?"]

    ]

    # getting the yoda dataframe
    df = get_yoda_corpus()
    n_df = df.copy()


    # fixing the speech of the Yoda
    fixList = markfixingYodaSpeech(n_df)

    # fixing the list that is given
    # This is the fixing of the Yoda speech
    n_df.at[343, "text"] = "Strong am I with the Force... but not that strong! Twilight is upon me and soon night must fall." 
    n_df.at[367, "text"] = "Remember, a Jedi's strength flows from the Force.  But beware.  Anger, fear, aggression. The dark side are they.  Once you start down the dark path, forever will it dominate your destiny."
    n_df.at[369, "text"] = "Luke...Luke...Do not...Do not underestimate the powers of the Emperor, or suffer your father's fate, you will. Luke, when gone am I (cough), the last of the Jedi will you be. Luke, the Force runs strong in your  family."

    # fixing the characters that should be just YODA
    n_df.loc[n_df['character'] == "YODA\t\t (gathering all his strength)"] = "YODA"
    n_df.loc[n_df['character'] == 'YODA\t (shakes his head)'] = "YODA"
    n_df.loc[n_df['character'] == 'YODA\t (tickled, chuckles)'] = "YODA"

    # cleaning the text of the dataframe
    n_df["text"] = n_df["text"].apply(fixString)

    # removing the rows where the character is the narrator
    n_df = n_df[n_df['character'] != "narrator"]
    # now resetting the index of the df
    n_df.reset_index(inplace=True)

    breakpoint()
    # making the new df
    n_df = make_new_df(n_df)

    # prepare inputs
    prepare_inputs(history=the_history, persona=the_persona, dataframe=n_df)


    

    print(n_df)