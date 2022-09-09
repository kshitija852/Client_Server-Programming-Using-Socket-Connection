
""" Name : Kshitija Ganesh Shete , Student Id : 1001821653"""

import os
import socket
import datetime
from dirsync import sync
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Setting the path variable to the path where the Directory B is present
path = 'C:\Dslab\Directory_B\\'

# Creation of empty list
list1 = []

"""
     Reference : https://www.geeksforgeeks.org/socket-programming-python/
"""

# Creation of the socket object
soc = socket.socket()

port = 12530

host = '127.0.0.1'

# To assign the IP address and the port number to the socket object
soc.bind((host, port))

print("The Socket got binded at the address:", host, " ", port)

# Putting the socket into the listening mode to check for incoming connection requests
soc.listen(10)

print("Socket is listening !!!")

# Defining the source path and target path
sourcepath = 'C:\Dslab\Directory_B\\'

targetpath = 'C:\Dslab\Directory_A\\'

"""
     Reference : https://www.geeksforgeeks.org/create-a-watchdog-in-python-to-look-for-filesystem-changes/
"""
# To check any modifications like create,delete files on any of the directories
class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        strObject = event.src_path
        indexOfLastSlash = strObject.rfind('\\') + 1
        eventfileName = strObject[indexOfLastSlash:]

        if event.is_directory:
            return None
        # Event when New file gets created
        elif event.event_type == 'created':
            print("File has been created in Server-B - % s." % eventfileName)
        # Event when Modifications are made to the file
        elif event.event_type == 'modified':
            print("File has been modified in Server-B - % s." % eventfileName)
        # Event when file gets deleted
        elif event.event_type == 'deleted':
            delete_file_name = targetpath + "\\" + eventfileName
            if os.path.exists(delete_file_name):
                os.remove(delete_file_name)
                print("File has been deleted in Server-B - % s." % eventfileName)
            else:
                print(delete_file_name + " - This file was not found or was deleted from another server instance")


observer = Observer()
event_handler = Handler()
observer.schedule(event_handler, sourcepath, recursive=False)
observer.start()

# As there can be many clients who send request to the server.
# So while true loop is used.
while True:
    """
          Reference : https://stackoverflow.com/questions/54688687/how-to-synchronize-two-folders-using-python-script
    """
    # Performing the synchronization of Directory B and Directory A
    sync(sourcepath, targetpath, 'sync')

    # Accepting an incoming connection request and storing the socket returned by accept()
    serveraConnection, serveraAddress = soc.accept()

    print("Got connection from:", serveraAddress)
    print("\n")

    """ Reference:
         https://www.geeksforgeeks.org/how-to-print-all-files-within-a-directory-using-python/
    """
    # Storing the files present into the Directory B into listfiles
    listfiles = os.listdir(path)

    for i in listfiles:
        path1 = path + str(i)

        """
      Reference : https://www.geeksforgeeks.org/python-os-stat-method/
        """
        # To get the status of the file os.stat() is used
        fileData = os.stat(path1)

        """
    Reference : https://timestamp.online/article/how-to-convert-timestamp-to-datetime-in-python
        """
        # The date returned by os.stat() is not in readable format
        # To make it readable
        date1 = datetime.datetime.fromtimestamp(fileData.st_mtime).strftime('%m-%d-%y-%H:%M')

        str1 = "-" + str(i) + "  " + str(fileData.st_size) + " bytes" + "  " + str(date1)

        # To store the data of each file into the list
        list1.append(str1)

    """
       Reference : https://www.geeksforgeeks.org/python-program-to-convert-a-list-to-string/
    """
    # Converting the list into string in order to send it to the Server A
    # As list can not be encoded so converting to string
    dictB = " \n".join(list1)

    print("The files present in directory B are:")

    print(dictB)

    print("\n")

    # Sending the files that are present in the directory B to the Server A
    serveraConnection.send(dictB.encode())

    # Closing the connection with the Server A
    serveraConnection.close()


























