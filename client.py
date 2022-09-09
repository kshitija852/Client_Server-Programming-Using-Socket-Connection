""" Name : Kshitija Ganesh Shete , Student Id : 1001821653"""

import socket
import argparse

"""
     Reference : https://docs.python.org/3/library/argparse.html
"""
my_parser = argparse.ArgumentParser()

my_parser.add_argument('-lock',
                       type=int,
                       help="lock a file using index", nargs="?")
my_parser.add_argument('-unlock',
                       type=int,
                       help="unlock a file using index", nargs="?")
args = my_parser.parse_args()
"""
     Reference : https://www.geeksforgeeks.org/socket-programming-python/
"""
# Port on which to connect
port = 12340

# local computer IP address
host = '127.0.0.1'

# Creation of the socket object
soc = socket.socket()

# Making connection to the server
soc.connect((host, port))
to_send = "hello"

"""
     Reference : https://realpython.com/command-line-interfaces-python-argparse/
"""

# In command line interface it will take 'lock' and 'unlock' as instruction
if args.lock:
    to_send = "lock " + str(args.lock)
elif args.unlock:
    to_send = "unlock " + str(args.unlock)

"""
     Reference : https://stackoverflow.com/questions/37227176/how-to-send-a-message-from-client-to-server-in-python
"""
# To send a message from client to server A
soc.send(to_send.encode())


# Receiving the data from the server A
data = soc.recv(1024)

# Decoding the data received to get the data in the string form
print("The files present on Server A and Server B are:")
print(data.decode())

# closing the connection
soc.close()





