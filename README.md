# DropBin
A network application that automatically replicates and synchronizes files across multiple systems simultaneously.
This basically means a directory that exists in multiple locations and is kept in sync to be a perfect mirror. If a file is added or removed from one place, this change is replicated to all locations. A client application run on local machines and "watches" the directory for changes and "tells" the server when they happen. Similarly, server "watches" its own copy of the directory for any changes and "tells" the clients when they happen. In this fashion the directory on the server and its copies on your local machines are kept in sync.

## dropbin-client.py
● Runs as python dropbin-client.py <server-ip> <server-port>

● Registers itself with the server

● Uploads all the files in its dropbin directory to the server

● Monitors its local dropbin directory for changes such as:

○ If a new file is created in local dropbin directory it gets synced with the remote directory

○ If a file is deleted from the local dropbin directory its remote copy is also deleted

○ If a file in the local dropbin directory is updated, its remote copy at the server is also updated

## dropbin-server.py
● Runs as python dropbin-server.py <port>

● Listens for connection requests from clients

● Keep track of the client’s files in a directory and perform necessary updates to these files (adds, deletes,
updates etc)
