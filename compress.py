# This is the file that will be used to make a zip file
# of whatever file that is passed into it.

import os
from zipfile import ZipFile, ZIP_BZIP2, ZIP_LZMA, ZIP_STORED
import bz2
import lzma



data_path = os.path.join(os.path.dirname(__file__), "..", "chat_bot_data/r3.db")
save_to_path = os.path.join(os.path.dirname(__file__), "..", "chat_bot_data/rcopy.zip")
path_to_extract_to = os.path.join(os.path.dirname(__file__), "..", "chat_bot_data")

def compress_file(file_to_compress_path:str, compress_to_path:str, compression_style: int):

    with ZipFile(save_to_path, mode="w", compression=compression_style) as zip:
        zip.write(file_to_compress_path)



# This is the function that is used to uncompress the file
def uncompress_file(extract_to: str = None, unZip_from: str = None, compression_style:int = ZIP_STORED):
    with ZipFile(unZip_from, mode="r", compression=compression_style) as zip:
        zip.extractall(path_to_extract_to)





if __name__ == "__main__":
    # trying the compression first
    # compress_file(file_to_compress_path=data_path, compress_to_path=save_to_path, compression_style=ZIP_BZIP2)

    # doing the extraction
    uncompress_file(extract_to=path_to_extract_to, unZip_from=save_to_path, compression_style=ZIP_BZIP2)
    print("Have finished the uncompression")

    # print(f"This is the path {path_to_extract_to}")
