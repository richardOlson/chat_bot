# This is the file where will read in the data to see what it looks like

import json

# making the dictionary that will hold the json files

list_of_rows = []

with open(r"C:\Users\porte\Richard_python\nlp_projects\chat_bot_data\RC_2018-05", ) as the_file:
    counter = 0
    for row in the_file:
        row = json.loads(row)
        # id = row["id"]
        # parent_id = row['parent_id']
        # parent_id = parent_id.split("_")[1]
        
        # if id == parent_id:
        print(row, "\n\n\n\n")
        # list_of_rows.append(row)
        # list_of_rows.append(filler)
        counter += 1
        if counter >= 10:
            break

# print(list_of_rows)