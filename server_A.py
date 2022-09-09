""" Name : Kshitija Ganesh Shete , Student Id : 1001821653"""

import socket
import os
import datetime
import portalocker
from dirsync import sync
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# Setting the path variable to the path where the Directory A is present
path = 'C:\Dslab\Directory_A\\'

locked_files = []

sourcepath = 'C:\Dslab\Directory_A\\'

targetpath = 'C:\Dslab\Directory_B\\'


# This function is used to perform the exclusive lock by using portalocker.LOCK_Ex
def lock(file_name):
    os.chmod(sourcepath + "\\" + file_name, 0o444)
    locked_files.append(file_name)

# This function is used to unlock the file
def unlock(file_name):
    os.chmod(sourcepath + "\\" + file_name, 0o777)
    locked_files.remove(file_name)

# For Fetching the file name from index
def get_file_name_from_index(index):

    dira = os.listdir(sourcepath)
    for i in dira:
        file_index = dira.index(i)
        if file_index == index:
            return str(i)



# Creation of the empty list
list1 = []

"""
     Reference : https://www.geeksforgeeks.org/socket-programming-python/
"""

# Creation of the socket object
soc = socket.socket()

host = '127.0.0.1'

port = 12340

# To assign the IP address and the port number to the socket object
soc.bind((host, port))

print("The Socket got binded at the address:", host, " ", port)

# Putting the socket into the listening mode to check for incoming connection requests
soc.listen(10)

print("Socket is listening to the connection made by:", host, " ", port)

# Defining sourcepath and targetpath

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
            sync(sourcepath, targetpath, 'sync')
        # Event when Modifications are made to the file
        elif event.event_type == 'modified':
            print("File has been modified in Server-B - % s." % eventfileName)
            if eventfileName not in locked_files:
               sync(sourcepath, targetpath, 'sync')
        # Event when file gets deleted
        elif event.event_type == 'deleted':
            delete_file_name = targetpath + "\\" + eventfileName
            if os.path.exists(delete_file_name):
                os.remove(delete_file_name)
                print("File has been deleted in Server-B - % s." % eventfileName)
            else:
                print(delete_file_name + " - This file was not found or was deleted from another server instance")
            sync(sourcepath, targetpath, 'sync')

observer = Observer()
event_handler = Handler()
observer.schedule(event_handler, sourcepath, recursive=False)
observer.start()

# As there can be many clients who send request to the server.
# So while true loop is used.
while True:
    list1.clear()

    # Accepting an incoming connection request and storing the socket returned by accept()
    clientConnection, clientAddress = soc.accept()

    print("Got connection from:", clientAddress)
    print("\n")

    # It gets the instruction from client
    client_msg = clientConnection.recv(2048).decode()
    print(client_msg)

    if client_msg.startswith("lock "):
        # Fetching the index to store the index into metadata
        file_name = get_file_name_from_index(int(client_msg.split(" ")[1]))
        print(file_name)
        # It will lock if the instruction from client is to lock
        lock(file_name)
    elif client_msg.startswith("unlock "):

        file_name = get_file_name_from_index(int(client_msg.split(" ")[1]))
        print(file_name)
        # It will unlock if the instruction from client is to unlock
        unlock(file_name)


    """
     Reference : https://stackoverflow.com/questions/54688687/how-to-synchronize-two-folders-using-python-script
          """
    # For synchronization of two folders
    sync(sourcepath, targetpath, 'sync')

    """ Reference:
         https://www.geeksforgeeks.org/how-to-print-all-files-within-a-directory-using-python/
    """
    # Storing the files present into the Directory A into listfiles
    listfiles = os.listdir(path)

    for i in listfiles:
        ind = listfiles.index(i)
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

        str1 = "-" + '['+str(listfiles.index(i))+']' + " " + str(i) + "  " + str(fileData.st_size) + " bytes" + "  " + str(date1)

        file_name = str1.split(' ')[1]
        if file_name in locked_files:
            str1 = str1 + " <locked>"

        # To store the data of each file into the list
        list1.append(str1)

    """
       Reference : https://www.geeksforgeeks.org/python-program-to-convert-a-list-to-string/
    """
    # Converting the list into string in order to send it to the Client
    # As list can not be encoded so converting to string
    dictA = "\n".join(list1)

    print("The files in directory A are:")
    print(dictA)

    print("\n")

    soc1 = socket.socket()

    # Defining the port on which Server A will connect
    port1 = 12530

    host1 = '127.0.0.1'

    # Connecting to the Server
    soc1.connect((host1, port1))

    # Receiving the data send by the Server
    data = soc1.recv(1024)

    # Decoding the data send by the Server
    data1 = (data.decode())

    # Combining the directory A and directory B files
    finalList = dictA

    """
   Reference : https://www.w3schools.com/python/ref_list_sort.asp 
    """


    def function(fin1):
        return (fin1.split(' ')[0])


    """
        reference : https://www.w3schools.com/python/ref_string_split.asp
    """
    # Converting the string to list
    fin = finalList.split('\n')

    # Performing the sorting on list based on index[0] as it contains the file name

    fin.sort(key=function)

    fin = fin[0:]

    final = "\n".join(fin)

    soc1.close()

    # Sending the sorted files from Directory A and Directory B to the Client
    clientConnection.send(final.encode())

    # Closing the connection made to the Client
    clientConnection.close()

