# This is the file that will read the cornell data into a data base
# The end result is to get the it into a format of parent comment
#  and then child responce

import os
import sqlite3
# used to make sure that the data is clean and not bad data
from profanity_check import predict as profane_predict

class Cornell_reader():

    
    sep = "+++$+++" # the separator used in the files
    movie_conv_path = os.path.join(os.path.curdir, "..",  "cornell movie-dialogs/movie_conversation.txt")
    movie_lines_path = os.path.join(os.path.curdir, "..", "cornell movie-dialogs/movie_lines.txt")
    db = os.path.join(os.path.curdir, "..", "movie_lines.db")

    def connect(self):
        """
        method to connect the databases
        """
        self.con = sqlite3.connect("movie_lines.db")
        self.cursor = con.cursor()
        return cursor

    def create_table(con=None, cursor=None):
        """
        Used to connect and then make the table if it is not created
        """
        # doing a connection for the database 
        # this will overwrite the connection that may have already been formed

        try:
            self.con = sqlite3.connect("movie_lines.db")
            self.cursor = self.con.cursor()
        except Exception as e:
            print(f"The connection did not work ---{e}")

        sql_string = """
                CREATE TABLE IF NOT EXISTS  movlines (
                    id integer PRIMARY KEY,
                    line_id text, 
                    person text, 
                    line text

                )
        """
        cursor.execute(sql_string)


    def insert_into(self, listTuples:list):
        """
        Function that will insert the list of tuples 
        into the table of movie lines
        """
        sql_string = """
            INSERT INTO movie_lines (line_id, person, line)
            VALUES(?,?,?)
        """
        self.cursor.execute(sql_string, listTuples)
        self.con.commit()


    def fill_table(self,):
        """
        Function to fill the table of the lines in the movie
        """
        count = 1000
        table_list = []
        # opening the file and then doing the filling of the data
        with open(movie_lines_path, "r", buffering=1000) as f:
            for i in range(count):
                line = f.readline()
                if not line:
                    self.insert_into(table_list)
                table_list.append((line[0], line[3], line[4]))


    def read_cornell(self,):
        """
        This is the function that is used to read in the data to make 
        further make the database of the conversation pairs of the 
        movie data
        """
        f = open(movie_lines_path, "r",)

        with open(movie_conv_path, "r")as convs:
            conv_line = convs.readline()
            # going through the conversations
            lineList = conv_line.split(sep=sep)



if __name__ == "__main__":
    print(movie_conv_path)
    print(movie_lines_path)

    