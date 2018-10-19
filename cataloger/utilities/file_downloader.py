#Referencing https://erlerobotics.gitbooks.io/erle-robotics-python-gitbook-free/telnet_and_ssh/sftp_file_transfer_over_ssh.html

import functools
import paramiko
from tempfile import TemporaryFile
import requests
from urllib.parse import urlparse

class AllowAnythingPolicy(paramiko.MissingHostKeyPolicy):
    def missing_host_key(self, client, hostname, key):
        return

class file_downloader():
    def download_temp(url,sftp_username=None,sftp_password=None):
        try:
            #It then attempts to parse the url with the urllib library.
            parsed_url = urlparse(url)
        except:
            #If it fails, it sends a message back.
            raise Exception('The provided url is not in a recognized format.')
        #If the file doesn't end with a supported type, it throws an error.
        if not parsed_url.path.lower().endswith(('.csv','.xlsx','.json')):
            raise Exception('The provided URL does not point to a supported file type.')
        if parsed_url.scheme.lower() == 'https':
             return file_downloader.__https_file_downloader(url)
        elif parsed_url.scheme.lower() == 'sftp':
             return file_downloader.__sftp_file_downloader(parsed_url,sftp_username,sftp_password)
        else:
            raise Exception('The provided URL does not use a https nor a sftp schema.')

    def __https_file_downloader(url):
        #takes in a given url and downloads the file into a temporary file.
        #Assumes https since there is a single input into the method.
        try:
            with TemporaryFile() as output:
                #attempts to open the file using the url.
                file = requests.get(url, stream=True)
                #writes the file into the temporary file in chunks.
                for chunk in file.iter_content(chunk_size = 1024):
                    output.write(chunk)
                #returns the start of the file before returning the temporary file.
                output.seek(0)
                return output
        except:
            #if there is any errors in the above process, it doesn't return anything to signify the failure.
                return None

    def __sftp_file_downloader(parsed_url,sftp_username,_sftp_password):
        #Assumes sftp if sftp_* inputs into the method aren't None.
        #The format of the URL for sftp is sftp://[host]:[port]/[path to file] which is defined in the Uniform Resource Identifier schemes.
        #https://www.iana.org/assignments/uri-schemes/prov/sftp
        try:
            #Attempts to open a connection to the sftp server.
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(AllowAnythingPolicy())
            if parsed_url.port is not None:
                client.connect(hostname= parsed_url.hostname,port=parsed_url.port, username=sftp_username,password = sftp_password)
            else:
                client.connect(hostname= parsed_url.hostname, username=sftp_username,password = sftp_password)
            #Creates a temporary file and attempts to open the file using the given file path. It then copies it into the temporary file.
            sftp = client.open_sftp()
            fileObject = sftp.file(parsed_url.path[1:],'rb')
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