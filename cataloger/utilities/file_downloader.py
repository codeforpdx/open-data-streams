from tempfile import TemporaryFile
import requests

#takes in a given url and downloads the file into a temporary file. 
#Assumes https since there is a single input into the method.
def file_downloader(url):
    try:
        with TemporaryFile as output:
            #attempts to open the file using the url.
            file = requests.get(url, stream=True)
            #writes the file into the temporary file in chunks.
            for chunk in file.iter_content(chunk_size = 1024):
                output.write(chunk)
            #returns the start of the file before returning the temporary file.
            file.seek(0)
            return output
    except:
        #if there is any errors in the above process, it doesn't return anything to signify the failure.
        return None

#Assumes sftp since there is three inputs into the method.
#Currently in the implementation process.
def file_downloader(url,username,password):
    return None
