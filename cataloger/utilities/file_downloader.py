#Referencing https://erlerobotics.gitbooks.io/erle-robotics-python-gitbook-free/telnet_and_ssh/sftp_file_transfer_over_ssh.html

import functools
import paramiko
from tempfile import TemporaryFile
import requests

class AllowAnythingPolicy(paramiko.MissingHostKeyPolicy):
    def missing_host_key(self, client, hostname, key):
        return

def file_downloader(url,sftp_username=None,sftp_password=None):
    if sftp_username and sftp_password:
        #Assumes sftp if sftp_* inputs into the method aren't None.
        #The format of the URL for sftp is sftp://[host]//[path to file]
        try:
            #Attempts to split the URL into 3 parts, the "sftp:" part, the name of the host, and the path to the file.
            splintered_url = url.split("//")

            #Attempts to open a connection to the sftp server.
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(AllowAnythingPolicy())
            client.connect(splintered_url[1], username=sftp_username,password = sftp_password)

            #Creates a temporary file and attempts to open the file using the given file path. It then copies it into the temporary file.
            sftp = client.open_sftp()
            fileObject = sftp.file(splintered_url[2],'rb')
            temp_file = TemporaryFile()
            for chunk in fileObject.xreadlines():
                temp_file.write(chunk)
            
            #Closes the connection to the server and navigates back to the top of the file before returning the temporary file.
            client.close()
            temp_file.seek(0)
            return temp_file
        except:
            #if there is an error in the above process, it doesn't retuan anything to signify the failure.
            return None
    else:
        #takes in a given url and downloads the file into a temporary file.
        #Assumes https since there is a single input into the method.
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
