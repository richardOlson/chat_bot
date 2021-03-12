# This is the file that will read the cornell data into a data base
# The end result is to get the it into a format of parent comment
#  and then child responce

import os
import sqlite3
# used to make sure that the data is clean and not bad data
from profanity_check.profanity_check import predict_prob
import ast


# "C:\Users\porte\Richard_python\nlp_projects\chat_bot\cornell movie-dialogs corpus"
class Cornell_reader():

    
    sep = "+++$+++" # the separator used in the files
    movie_conv_path = os.path.join(os.path.dirname(__file__), "cornell movie-dialogs corpus/movie_conversations.txt")
    movie_lines_path = os.path.join(os.path.dirname(__file__), "cornell movie-dialogs corpus/movie_lines.txt")
    db = os.path.join(os.path.dirname(__file__), "movies.db")

    def connect(self):
        """
        method to connect the databases
        """
        self.con = sqlite3.connect(self.db)
        self.cursor = self.con.cursor()
        return self.cursor

    def create_table(self, con=None, cursor=None):
        """
        Used to connect and then make the table if it is not created
        """
        # doing a connection for the database 
        # this will overwrite the connection that may have already been formed

        try:
            self.con = sqlite3.connect(self.db)
            self.cursor = self.con.cursor()
        except Exception as e:
            print(f"The connection did not work ---{e}")

        sql_string = """
                CREATE TABLE IF NOT EXISTS  movie_line_convos (
                    id integer PRIMARY KEY,
                    line_id text, 
                    person text, 
                    line text

                )
        """
        self.cursor.execute(sql_string)
        
        print("Made the table")


    def insert_into(self, listTuples:list):
        """
        Function that will insert the list of tuples 
        into the table of movie lines
        """
        sql_string = """
            INSERT INTO movie_line_convos (line_id, person, line)
            VALUES(?,?,?);
        """
        self.cursor.executemany(sql_string, listTuples)
        self.con.commit()
        print("added convos to the table")


    def fill_table(self,):
        """
        Function to fill the table of the lines in the movie
        """
        count = 1000
        table_list = []
        # opening the file and then doing the filling of the data
        with open(self.movie_lines_path, "r", buffering=1000) as f:
            while True:
                for _ in range(count):
                    line = f.readline()
                    if not line: # checking for the end of the file
                        self.insert_into(table_list)
                        return
                    # splitting the line
                    line = line.split(sep=self.sep)
                    # cleaning the white space
                    line_id = line[0].strip()
                    person= line[3].strip()
                    text = line[4].strip()
                    
                    # trying to make sure that we will only use those lines that are clean
                    if predict_prob([text])[0] < .6:
                        table_list.append((line_id, person, text))
                # after loading 1000 of the lines then we will call the method to insert the lines
                self.insert_into(table_list)
                # creating a new empty table_list
                table_list = []



    def read_cornell(self,):
        """
        This is the function that will make the pairs of the cornell data movie lines
        """
        

        with open(self.movie_conv_path, "r")as convs:
            conv_line = convs.readline()
            # going through the conversations
            lineList = conv_line.split(sep=self.sep)
            # getting the list of the lines from the string
            lineList = lineList[3]
            lineList = lineList.replace("\n", "")
            lineList = lineList.strip()
            lineList = ast.literal_eval(lineList)
            breakpoint()
            print("made it")



if __name__ == "__main__":
    
    corn = Cornell_reader()
    corn.connect()
    corn.read_cornell()