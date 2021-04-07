# This is the file that will be used to make a zip file
# of whatever file that is passed into it.

import os
from zipfile import ZipFile, ZIP_BZIP2, ZIP_LZMA, ZIP_STORED
import bz2
import lzma
from pathlib import Path
import sqlite3



data_path = os.path.join(os.path.dirname(__file__), "..", "chat_bot_data/reddit4.db")
save_to_path = os.path.join(os.path.dirname(__file__), "..", "chat_bot_data/r4lmza.zip")
path_to_extract_to = os.path.join(os.path.dirname(__file__), "..", "chat_bot_data")

def compress_file(file_to_compress_path:str, compress_to_path:str, compression_style: int):

    with ZipFile(compress_to_path, mode="w", compression=compression_style) as zip:
        # string = file_to_compress_path.split("/")[-1]
        zip.write(file_to_compress_path)



# This is the function that is used to uncompress the file
def uncompress_file(extract_to: str = None, unZip_from: str = None, compression_style:int = ZIP_STORED):
    thePath = Path(extract_to)
    
    
    with ZipFile(unZip_from, mode="r", compression=compression_style) as zip:
        # making so that the member is just the last part just being the 
        # name of the file.
        mem = zip.namelist()
        mem = mem[0].split("/")[-1]
        
        zip.extractall(path=extract_to)




# Function that will take either the paren or the child's
# comments and will make a file with them as binary.
# This is to make the file to be able to upload into google colab
def make_comment_file(theSql, comment_file, index):
    """
    The sql is taken in and then the comments are put in a file

    Index:  The index is the index found in the row to the comment that is wanted 
            to be put in a file.
    """
    theFile =  open(comment_file, mode="wb")

    # opening the sql
    # doing the connection
    try:
        conneciton = sqlite3.connect(theSql)
        cursor = conneciton.cursor()
    except Exception as e:
        print(f"The connection could not be made, ---> {e}")
    # looping through the rows
    sql_string = """
        SELECT * FROM convos;
    """
    
    newLine = "\n".encode()
    for row in cursor.execute(sql_string):
        parent = row[index].encode()
        
        theFile.write(parent)
        theFile.write(newLine)
        

    
# function that will be used to read the file
def read_file(thefile, num_lines=-1):
    with open(thefile, "rb") as f:
        counter = 0
        line = f.readline()
        while(line):
            if counter == num_lines:
                break
            
            line = line.decode()
            print(f"This the is line of the file ---> {line}")
            line = f.readline()
            counter += 1
            
            





if __name__ == "__main__":


    # # files that we will compress
    file_to_compress = os.path.join(os.path.dirname(__file__), "..", "chat_bot_data/parent")
    save_compressed_file_path = os.path.join(os.path.dirname(__file__), "..", "chat_bot_data/parent_zipped.zip")

    # path to extract to 
    path_to_extract_to = os.path.join(os.path.dirname(__file__), "..", "chat_bot_data")


    # # trying the compression first
    compress_file(file_to_compress_path=file_to_compress, compress_to_path=save_compressed_file_path, 
                     compression_style=ZIP_LZMA)

    print(f"Done with the compression of the file")

    # # doing the extraction
    # uncompress_file(extract_to=path_to_extract_to, unZip_from=save_compressed_file_path, compression_style=ZIP_LZMA)
    # print("Have finished the uncompression")
    # with ZipFile(save_compressed_file_path) as f:
    #     f.namelist()
    #     breakpoint( )
    #     print("The file is now here")
    #     if f:
    #         print("hey")


    # This is the code to write something to a file of just the parent or the child
    # sql_file = os.path.join(os.path.dirname(__file__), "..", "chat_bot_data/reddit4.db")
    # file_to_save = os.path.join(os.path.dirname(__file__), "..", "chat_bot_data/child")

    # make_comment_file(theSql=sql_file, comment_file=file_to_save, index=3)

    # print("Done reading the file and making it")

    # # doing the reading of few lines of the code
    # read_file(file_to_save, num_lines=5)