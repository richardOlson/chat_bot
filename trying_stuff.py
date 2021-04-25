# just a file to try things

import pandas as pd
import os
from pathlib import Path

# printing out the working directory 
print(f"The currrent dirctory is --> {os.getcwd()}")


theHomePath = str(Path.home())
# know making it to the path
fullPath = os.path.join(theHomePath, "Downloads", "yoda/yoda-corpus.csv")
# Changing the directory
# os.chdir(theHomePath)
# printing out the new directory 
# print(f"This is the new directory ---> {os.getcwd()}")



df = pd.read_csv(fullPath)

n = 7
# this is the list that will hold all the rows
rows = []
for i in range(n, len(df.index)):
    row = []
    prev = i -1 -n
    
    for j in range(i, prev, -1):
        row.append(df["text"][j])
    # then adding the row to the rows list
    rows.append(row)

# now going to make the dataframe that will have the past 7 reponces
columns  = ["saying", "responce"]

# building the columns
columns = columns + ["context/" + str(i) for i in range(n-1)]

# making the new dataframe
new_df = pd.DataFrame(rows, columns=columns)

breakpoint()
print(new_df.head(5))
    