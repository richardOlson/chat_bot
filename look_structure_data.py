# This is the file where will read in the data to see what it looks like

import json

# making the dictionary that will hold the json files

list_of_rows = []
filler = "-------------------"
with open(r"C:\Users\porte\Richard_python\nlp_projects\chat_bot\RC_2018-05", ) as the_file:
    counter = 0
    for row in the_file:
        row = json.loads(row)
        list_of_rows.append(row)
        list_of_rows.append(filler)
        counter += 1
        if counter >= 2:
            break

print(list_of_rows)