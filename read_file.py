# This is the file that is going to be used to make the table and then will also help with come of the 
# cleaning of the data.

import json
from  profanity_check import predict as profane_predict
import sqlite3


class Table_maker():

    def __init__(self, db:str, max_num_tokens:int =-1):
        self.cursor = self.get_connection_and_cursor(db)
        self.transaction = []
        self.max_num_tokens = max_num_tokens

    def get_connection_and_cursor(self, db:str):
        try:
            # getting the database that is the sqlite3
            self.connection =sqlite3.connect(db)
            # cursor
            cursor = self.connection.cursor()
            return cursor
        except Exception as e:
            print("Unable to make the database connection--", e)


    # the function to create the table that will hold the info of the speech.
    def create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXIXTS convos (
                parent_id text PRIMARY KEY NOT NULL,
                commnent_id text,
                body text,
                parent_comment text,
                score integer 
            )
            """
        )

    def build_table(self, file_path:str, file_buffer_size:int, clean=True, num_iter=-1, num_rows_inserted:int= -1):
        """
        This is the function that will build the table by running through the data and doing the things 
        that is needed to the data to get it ready to be entered into the database table.

        num_iter: integer This is how many iteration or row from the file you want to read.
        if the number is -1, then it will read all of the file.  If this parameter is used then 
        the "num_rows_inserted" should be left as the default of -1.

        num_rows_inserted:  integer This is the number of rows that will be inserted into the 
        table.  If this parameter is used then the "num_iter" should be left at default of -1.

        This function will insert a row if the comment has an acceptable score and also if th
        """
        counter = 0
        # This is the variable that is used to break out the the function after the number of iterations
        # that were asked for 
        # TODO need to create the breaking out when the number of iterations is reached
        
        with open(file_path, "rb", buffering=file_buffer_size) as f:
            for row in f:
                # checking to see if we need to get out of the function
                if counter >= num_iter and num_iter != -1:
                    return
                # to get out with the specified number of rows
                if num_rows >= num_rows_inserted:
                    return
                counter += 1 
                # get the row and build the transaction list to do the adding to the database
                body = self.get_data(row["body"], max_num_tokens=self.max_num_tokens)
                # need to have a comment that at least has a score of 2 and is a clean text
                if body == False and row["score"] >= 2:
                    # skipping all adding any of the text from this reddit file if 
                    # there is something wrong with the body of the text.
                    continue
                
                parent_id = row["parent_id"]
                commnent_id = row["id"]
                score = row["score"]
                # trying to find the parent comment and put that in the same one
                # if it can't find the parent comment then the function will return False
                parent_comment = self.find_parent_comment(row["parent_id"])

                # using the textual version of the false becuase this 
                # is going to be placed in the text for parent_comment
                if parent_comment == "False":
                    # if in here then we will need to make a row
                    # there is no parent comment
                    # TODO need to add to the transaction to make a row


                # checking to see if we are just going to update a row that is already present
                # in the database with a comment that is of a higher score
                result = find_comment_score(parent_id, score)
                if result:
                    # if in here the score of the current row is greater than another 
                    # that is already in the database with the same parent_id
                    self.update_prev_row(result, parent_id, comment_id, score, body, parent_comment)
                    continue
                
                
                

    def find_child_comment(self, pid:str):
        """
        This is the method to find a child comment.  It will
        do this by looking for comments that where the comment_id and the
        parent_id are not the same id.  This will mean that it is a child.
        This function will return the child_comment_id if found or will return
        False.
        """



                
    def find_parent_comment(self, the_parent_id:str):
        """
        This is the function that will find the parent comment when passed in a parent
        id.  This function will return text of the parent comment if it is found.  
        If it is not found then it will return False
        """
        # making of the sql string to find in the table
        sql_str = f"SELECT body in convos WHERE comment_id =  '{the_parent_id}' LIMIT 1; "
        # doing a try and a except block
        try:
            self.cursor.execute(sql_str)
            result = self.cursor.fetchone()[0]
            if result == None:
                return "False" # this will be place into the table of parent_comment
            return result

        except Exception as e:
            print("Exception finding parent comment --", e)
            return "False"

    # TODO need to make a function that will return the sql_string 
    # for finding with the parent_id, will determing what to select
    # will determing if the comment_id == the parent_id. 
    # Will determine if need an "and" with the where clause.
    
            

    def find_comment_score(self, the_score:int, pid:str):
        """
        This function will look for a comment (row) in the database 
        that has the id in the parent id and has a score that is 
        greater than the one that is passed in as a parameter.
        This function will return False if there is no comment that 
        has a lesser score.

        This function will return the comment_id of this row if 
        it exists.  This is to allow us to modify some of the data
        with the new data, that has a greater score.
        """
        # TODO need to fix the string checking to see if the parent comment is
        # Null or "False" -- this means that this comment
        # has not been tied to a parent comment
        sql_str f"SELECT comment_id, score   FROM convos WHERE parent_id = {pid}  AND parent_comment <> 'False'LIMIT 1;"

        self.cursor.execute(sql_str)
        result = self.cursor.fetchone()[0]
        # if there is no parent id then will return false
        if result == None:
            return False
        # checking to see if the score passed in is higher
        if result[1] > the_score:
            return False
        return comment_id
    

    def update_prev_row(self, prev_comment_id, parent_id, comment_id, score, body, parent_comment):
        """
        This is the method that will then put some data into the 
        row that is already in the database.  It is updating 
        with new data that has a higher score and is the child comment 
        """
        sql_str = f"UPDATE convos SET 'parent_id' =  {parent_id} 'comment_id' = {comment_id} 'score' = {score} "  \
            f"'body'={body} parent_comment={parent_comment}"  \
            f"WHERE comment_id = {prev_comment_id};" 
        try:
            self.cursor.execute(sql_str)
            self.connection.commit()
        except Exception as e:
            print("update_prev_row", e)


    def get_data(self, body:str, max_num_tokens:int):
        """ 
        This is the function that will clean the body of the text
        This fucntion will return false if the text has been deleted or removed.
        It will also return false if the text is not "clean" ie. profane type of text.
        This function will then also make all the qoutes be the same and will remove any new 
        line char or return char.

        This function also will check if there has been set a max amount of tokens if the 
        data is too large.  

        
        """
        if profane_predict([body])[0] == 1:
            # is a bad text
            return False
        if body == "[deleted]" or body == "[removed]":
            return False
        if len(body) < 1:
            # Means there is nothing really there
            return False
        if len(body.split()) > max_num_tokens and max_num_tokens != -1:  # -1 is no limit
            return False
        body = body.replace("\n", "  ").replace("\r", "  ")
        return body
        
            
