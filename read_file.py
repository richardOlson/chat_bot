# This is the file that is going to be used to make the table and then will also help with come of the 
# cleaning of the data.

import json
from  profanity_check.profanity_check import predict as profane_predict
from profanity_check.profanity_check import predict_prob
import sqlite3
from cleaner import text_cleaner
import os
import time


class Table_maker():
    """
        db: str:    The path to the database

        max_num_tokens: int: The maximum number of tokens that we will want to use
            if the number is -1 then no limit is placed on the number of tokens.
            The class will look at the length of the text and if it is too large it won't

        cut:    boolean:    This is only really used when max_num_tokens is not -1.  
                This flag is used to denote if the string lenght is longer than max_num_tokens
                then if this flag is set to True the program will cut the string to make it so that 
                it has upto the max num of tokens.  If left as false when using max_num_tokens, then 
                when a string is too large, the program will not add the row containing that string.
        
        """

    def __init__(self, db:str, max_num_tokens:int =-1, cut=False):
        
        self.cursor = self.get_connection_and_cursor(db)
        # The 3 transaction are used to make putting in the parents 
        # update will update the rows already found in the  many and then the children repsonces are put in
        self.parent_transaction = []
        self.child_transaction = []
        self.max_num_tokens = max_num_tokens
        self.file_pos = 0
        self.f = None
        self.cut = cut
        self.num_rows = 0

    def get_connection_and_cursor(self, db:str):
        
        try:
            # getting the database that is the sqlite3
            self.connection =sqlite3.connect(db)
            # cursor
            cursor = self.connection.cursor()
            return cursor
        except Exception as e:
            print("get_connection_and_cursor function error --", e)


    # the function to create the table that will hold the info of the speech.
    def create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS convos (
                id integer PRIMARY KEY,
                parent_id text NULL,
                comment_id text UNIQUE,
                child_responce text,
                parent_comment text,
                score integer 
            )
            """
        )

    def build_table_transaction(self, file_path:str, file_buffer_size:int, clean=True, 
                    num_iter=-1, num_rows_inserted:int= -1, filePos=0, trans_size=1000):

        """
        This is the same funcion as the build_table but is changed to how it will go about 
        building the table.
        It will put all the parents in in a execute many function.  In an effort to speed up 
        building the table.


        num_iter: integer This is how many iteration or row from the file you want to read.
        if the number is -1, then it will read all of the file.  If this parameter is used then 
        the "num_rows_inserted" should be left as the default of -1.

        num_rows_inserted:  integer This is the number of rows that will be inserted into the 
        table.  If this parameter is used then the "num_iter" should be left at default of -1.

        """
        # counter is a variable to count the number of iterations 
        counter = 0
        # num_rows is a variable to count the number of comment--responce rows are formed
        num_rows = 0
        # This is the global variable for the body of the text
        body = None
        iterVal = True

        with open(file_path, "r", buffering=file_buffer_size) as f:
            self.f = f
            # setting it to be able to go to a certain position when starting
            f.seek(filePos)
            while iterVal:

                row = f.readline()

                # checking to see if we have reached then end
                if not row:
                    self.file_pos = self.f.tell()
                    break

                row = json.loads(row)
                
                # checking to see if we need to get out of the function
                if counter >= num_iter and num_iter != -1:
                    break
                # to get out with the specified number of rows
                if num_rows >= num_rows_inserted and num_rows_inserted != -1:
                    break

                counter += 1 

                if counter % trans_size == 0:
                    # will now do the parent transactions here
                    self.insert_many_rows(self.parent_transaction)
                    # run through the child transactions

                    # will then do the other rows
                    self.run_though_children(self.child_transaction)

                    print(f"There have been {self.num_rows} rows created with pairs") 
                    print(f"The number of iterations is now at {counter}") 

                    


                if "body" in row:
                    # get the row and build the transaction list to do the adding to the database
                    body = self.get_data(row["body"], max_num_tokens=self.max_num_tokens, clean=clean)
                    # checking to the see if this is a parent comment
                    # checking to see if the link_id is matching the parent_id
                    if row["link_id"] == row["parent_id"] and body != False:
                    # in here means that the link and the parent id are the same so it is a top
                    # level comment.
                        # making it to inert many 
                        self.parent_transaction.append((row["parent_id"], row["id"], body, "None", row["score"]))
                        continue
                
                # need to have a comment that at least has a score of 2 and is a clean text
                if row["score"] >= 2 and body !=False:
                    parent_id = row["parent_id"]
                    comment_id = row["id"]
                    score = row["score"]
                
                    # putting the rest into a child_transaction
                    self.child_transaction.append((parent_id, comment_id, body,  score))
                else:
                    continue

            # The following is when we are out of the loop where we would read the file
            # doing the transactions if there are any left that haven't been done
            self.insert_many_rows(self.parent_transaction)
            # run through the child transactions

            # will then do the other rows
            self.run_though_children(self.child_transaction)

            print(f"There have been {self.num_rows} rows created with pairs") 
            print(f"The number of iterations is now at {counter}") 

            # setting the file position
            self.file_pos = f.tell()
                



    def build_table(self, file_path:str, file_buffer_size:int, clean=True, 
                    num_iter=-1, num_rows_inserted:int= -1, filePos=0):
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
        # counter is a variable to count the number of iterations 
        counter = 0
        # num_rows is a variable to count the number of comment--responce rows are formed
        num_rows = 0
        # This is the global variable for the body of the text
        body = None
        iterVal = True
        
        with open(file_path, "r", buffering=file_buffer_size) as f:
            self.f = f
            # setting it to be able to go to a certain position when starting
            f.seek(filePos)
            while iterVal:

                row = f.readline()

                # checking to see if we have reached then end
                if not row:
                    self.file_pos = self.f.tell()
                    break

                row = json.loads(row)
                
                # checking to see if we need to get out of the function
                if counter >= num_iter and num_iter != -1:
                    break
                # to get out with the specified number of rows
                if num_rows >= num_rows_inserted and num_rows_inserted != -1:
                    break

                counter += 1 

                if counter % 1000 == 0:
                    print(f"There have been {num_rows} rows created with pairs") 
                    print(f"The number of iterations is now at {counter}") 
                    # will now do the parent transactions here
                    # will then do the other 


                if "body" in row:
                    # get the row and build the transaction list to do the adding to the database
                    body = self.get_data(row["body"], max_num_tokens=self.max_num_tokens, clean=clean)
                    # checking to the see if this is a parent comment
                    # checking to see if the link_id is matching the parent_id
                    if row["link_id"] == row["parent_id"] and body != False:
                    # in here means that the link and the parent id are the same so it is a top
                    # level comment.
                        self.insert_row((row["parent_id"], row["id"], row["body"], "None", row["score"]))
                        
                        continue

                # need to have a comment that at least has a score of 2 and is a clean text
                if row["score"] >= 2 and body !=False:
                    parent_id = row["parent_id"]
                    comment_id = row["id"]
                    score = row["score"]
                    # checking to find if there is a parent comment

                    parent_comment = self.find_parent_comment(self.not_Full_name(parent_id))
                    if parent_comment != "False":
                        # has a parent comment --- this means there is a match for this comment
                        value = self.find_comment_score(score, parent_id)
                        if value:
                            # Will be either a 1 or True True meaning that has a comment id
                            if value != 1:
                                # need to replace the body text for the on that is in there
                                self.update_prev_row((parent_id, comment_id, score, body, parent_comment, value))
                                print("have updated a row")
                            else:
                                # no row with a parent id the same so will put this row in 
                                self.insert_row((parent_id, comment_id, body, parent_comment, score))
                                        
                            if parent_comment != "False":
                                num_rows += 1
                
                else:
                    
                    continue
                
                
            
                
            self.file_pos = self.f.tell() 
        
                
             

    def run_though_children(self, listOfTuples:list, ):
        """
        This is the function that will go through a bunch of rows
        from the "self.child_transaction" and will go through the
        list of the children and will put add them if needed to update
        or to insert a new row in the database.
        """
        for parent_id, comment_id, body,  score in listOfTuples:

            # Will check if the row has a parent comment in the database already if it does then
            # will put in parent_child_transaction list
            # If not then will be just added to the child_transaction list
            parent_comment = self.find_parent_comment(the_parent_id=self.not_Full_name(parent_id))
            
            if parent_comment != "False":
                # getting the value to see if this one has a better score than possible a row 
                # that is already in the database
                value = self.find_comment_score(the_score=score, pid=parent_id)

                if value:
                    # this means that the value is either 1 -- there is not a pairing already with the parent in 
                    # in the database.
                    # the parent comment is retruned if the current comment as a higher
                    # score than the child paired with the parent.
                    if value != 1:
                        self.update_prev_row((parent_id, comment_id, score, body, parent_comment, value)) 
                    else:
                        # in here we are inserting a new row because there has been no previous pairing 
                        # with the parent comment
                        self.insert_row((parent_id, comment_id, body, parent_comment, score))
                    if parent_comment != "False":
                        self.num_rows += 1
        # will now do the 
        # emptying of the child transaction
        self.child_transaction = []
                                                        
                
            
            
        
    def not_Full_name(self, id:str):
        """
        This is the function remove the prefix portion of the 
        full name of the id.  This is to make it be able to match the comment_id.

        Returns:    Will remove the prefix and return just the id.
        """
        id = id.split("_")
        if len(id) == 2:
            return id[1]
        else:
            return id[0]       
                
                

    def insert_many_rows(self, thelistofTuples:list):
        """
        This is the function that will insert multiple rows into the table at one time 
        with the execute_many function of sqlite3

        thelisofTuples:     This is the list of the rows that will be entered in together it is in the form
                            of a list of tuples where each tuple is a row that is entered into the table.
        """
        sql_string = """
                INSERT INTO convos (parent_id, comment_id, child_responce, parent_comment, score)
                VALUES(?,?,?,?,?)
        """
        try:
            self.cursor.executemany(sql_string, thelistofTuples)
            self.connection.commit()
            # making the list empty again
            self.parent_transaction = []
        except Exception as e:
            print("Inserting many did not work, -- ", e)

    
    def update_many_rows(self, thelisofTuples:list):
        """
        This is the function that will update many of the rows in the table with the 
        list of tuples that is passed in to the function.
        
        theListofTuples:    This is the list of the rows that are being passed in to be updated
        """
        sql = """
            UPDATE convos
            SET parent_id = ?,
                comment_id = ?,
                score = ?,
                child_responce = ?, 
                parent_comment = ?
                WHERE comment_id = ?
        """
        try:
            self.cursor.executemany(sql, thelisofTuples)
            self.connection.commit()
        except Exception as e:
            print("The updating of multiple rows did not work ---> ",e )

                
    def insert_row(self, the_row:tuple):
        """
        This funtion will try to insert the row into the table 
        """
        sql_str = """
            INSERT INTO convos (parent_id, comment_id, child_responce, parent_comment, score)
            VALUES(?,?,?,?,?)
        
        """
        try:
            self.cursor.execute(sql_str, the_row)
            self.connection.commit()
        except Exception as e:
            print("The row insert did not work--->", e)
            


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
        If it is not found then it will return FALSE
        """
        # making of the sql string to find in the table
        sql_str = f"SELECT child_responce FROM convos WHERE comment_id =  '{the_parent_id}' LIMIT 1; "
        # doing a try and a except block
        try:
            self.cursor.execute(sql_str)
            result = self.cursor.fetchone()
            if result == None:
                return "False" # this will be place into the table of parent_comment
                print("Did not find the parent comment for this comment")
            return result[0]

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

        :returns:   False -- the score is less than the row score already in the database.  
                   "1"  is returned if -- Cannot find any row in the database that has been added already
                    comment_id -- the comment_id of the row in the database
        """
        
        sql_str = f"SELECT score, comment_id   FROM convos WHERE parent_id = '{pid}' LIMIT 1;"

        
        self.cursor.execute(sql_str)
        result = self.cursor.fetchone()

        # if there is no parent id then will return false
        if result == None:
            return 1
        
        # checking to see if the score passed in is higher
        if result[0] > the_score:
            return False
        return result[1]
    

    def update_prev_row(self, the_tuple:tuple):
        """
        This is the method that will then put some data into the 
        row that is already in the database.  It is updating 
        with new data that has a higher score and is the child comment 
        """

        sql_str = """ 
                UPDATE convos
                SET parent_id = ?,
                comment_id = ?,
                score = ?,
                child_responce = ?, 
                parent_comment = ?
                WHERE comment_id = ?
                """
                    
        
        try:
            self.cursor.execute(sql_str, the_tuple)
            self.connection.commit()
        except Exception as e:
            print("update_prev_row  --", e)


    def get_data(self, body:str, max_num_tokens:int, clean=True):
        """ 
        This is the function that will clean the body of the text
        This fucntion will return false if the text has been deleted or removed.
        It will also return false if the text is not "clean" ie. profane type of text.
        This function will then also make all the qoutes be the same and will remove any new 
        line char or return char.

        This function also will check if there has been set a max amount of tokens if the 
        data is too large.  

        
        """
        if clean:
            if predict_prob([body])[0] > .6: # higer than this is considered a bad text
                # is a bad text
                return False
        if body == "[deleted]" or body == "[removed]":
            return False
        if len(body) < 2: # want it to have more than just one letter
            # Means there is nothing really there
            return False
        
        if len(body.split()) > max_num_tokens and max_num_tokens != -1:  # -1 is no limit
            if self.cut:
                bodyList = body.split()
                bodyList = bodyList[:max_num_tokens + 1]
                # if user wants to return the string cut to the size of less than the 
                # max_num_tokens then cut is true and in here will cut the string.
        
            else:
                return False
        # now doing the cleaning of the text to remove emoji and other things not wanted in the text
        body = text_cleaner(body)
        if len(body) < 1:
            return False
        return body
        
        
            

if __name__ == "__main__":

    path_for_reddit = os.path.join(os.path.dirname(__file__), "..",  "chat_bot_data/reddit4.db")
    # getting the class
    t = Table_maker(path_for_reddit)
    t.create_table()

    # the path to the data
    file_path = r"C:\Users\porte\Richard_python\nlp_projects\chat_bot_data\RC_2017-07"
    # now doing the reading in the data
    start = time.time()
    t.build_table_transaction(file_path, file_buffer_size=1000, num_iter=35000, filePos=0, trans_size=1500)
    end = time.time()
    print(f"The file position is {t.file_pos}")
    print(f"The program took {end - start} seconds")