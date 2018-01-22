import socket
import thread
import os
import sys
import time
import shutil

# global x
x = 1024;
database = {};#rememebr to global
deleted = {};
unassigned = [];
# mirror = 0;
shared = {};#rememebr to global
ushared = {};
monitors = {};#remeber the extra thread of every user against thier usernames
# x = 1;
path = os.getcwd();
def Initialization(connection,name):
	global x;
	global shared;
	global ushared;
	mirror = 0;
	sharer = 0;
	shfiles = [];
	sentList = [];

	numFiles = connection.recv(1024)
	print numFiles
	connection.send(numFiles)
	
	num = 1
	numFiles = int(numFiles)

	while num < numFiles:
		
		filename = connection.recv(1024)
		print filename
		connection.send(filename); #recevies filename
		sentList.append(filename);

		filesize = connection.recv(1024)
		print filesize
		connection.send(filesize)

		filesize = long(filesize)
		condition = 0

		rfile = open(filename ,"wb" ) #wb means write in binary
		# global x
		while x > filesize:
			if x > filesize:
				# global x
				x = x - (x/2)
				print x

		print "Starting writing process..."
		while ((condition*x) < filesize ):
			recData = connection.recv(x)
			rfile.write(recData)
			condition = condition + 1
		# recData = connection.recv(x)
		# rfile.write(recData)
		# global x
		x = 1024
		
		print "Writing process ended!!"	

		print 'File received and saving...',filename
		rfile.close()


		if filename == "Sharefile.dropbin.txt":
			sharer = 1;
			print "THERE BE SHARING!!!"
			with open(filename,"r") as f:
				for line in f:
					filer = line.split()
					filer.append(name)
					# print filer
					shared[filer[0]] = filer[1:]
			print "\n\n\n"
			print shared;
			print "\n\n\n"

		if filename == "Selectfile.dropbin.txt":
			#store info about sharing files between same users
			mirror = 1;
			selecter = open("Selectfile.dropbin.txt","r");
			shfiles = (selecter.read()).split()
			print shfiles;
			print "\n\n\n"
			print "SELECTOR!!!"
			selecter.close();
			# while True:
			# 	mirror = 1;
		# else:
			# mirror = 0;##mirror from client side, this is useless for now

		connection.send('File sucessfully written!')
		print "File sucessfully written!"
		print "\n\n\n"
		num = num + 1
	# print 'Exiting loop'
	#####PUTS SHARED FILES IN THEIR DRECOIRES ON THE SERVER END


	if mirror == 1:
		# put files in the other blah shit
		print "NORHING TO SEE HERE....."
		shfiles.append("Selectfile.dropbin.txt");
		if sharer == 1:
			shfiles.append("Sharefile.dropbin.txt");
		if monitors.has_key(name):
			mappend = monitors[name];
			mappend.extend(shfiles);
			monitors[name] = mappend;
		else:
			monitors[name] = shfiles; 

	elif mirror == 0:
		# mirrorD = os.listdir(os.getcwd());
		# mirrorD = sentList;
		# getfrom = database[name];
		# idnumber = -1;
		# for xtuple in getfrom:
		# 	if xtuple[0] == connection:
		# 		idnumber = xtuple[1];
		# 		mirrorD.append(idnumber)
		# mirrorD = list(reversed(mirrorD));
		if monitors.has_key(name):
			mappend = monitors[name];
			mappend.extend(sentList);
			monitors[name] = mappend;
		else:
			monitors[name] = sentList; 

	if sharer == 1:
		src = os.getcwd();
		for key in shared.keys():
			# print key;
			# print "\n\n\n"
			if os.path.isfile(str(key)):
				# print "Hallelujah"
				srcf = os.path.join(src,key);
				for user in shared[key]:
					if user != name:
						if ushared.has_key(user):
							val = ushared[user];
							if key in val:
								continue
							else:
								val.append(key)
								ushared[user] = val;
						else:
							ushared[user] = [key];


						os.chdir(path);

						if not os.path.exists(user):
							os.makedirs(user)
						dest = os.path.join(path,user);
						shutil.copy(srcf,dest);
						os.chdir(src);

	# print shared
	print ushared
	print "\n\n\n"
	#
	connection.send('All files Sucesfully Backed up!!')
	print "All files Sucesfully Backed up!!"
	print '\n\n\n'
	# print 'EXITINGGGGGG'



def Updation(connection,name):

	global x
	global ushared;

	filename = connection.recv(1024)
	print filename
	connection.send(filename)

	filesize = connection.recv(1024)
	print filesize
	connection.send(filesize)

	filesize = long(filesize)
	condition = 0

	rfile = open(filename ,"wb" ) #wb means write in binary


	while x > filesize:
		if x > filesize:
			# global x
			x = x - (x/2)
			print x

	print "Starting updating process..."
	while ((condition*x) < filesize ):
		recData = connection.recv(x)
		rfile.write(recData)
		condition = condition + 1

	# global x
	x = 1024

	print "Updating process ended!!"	

	print 'Updates received and saving...',filename


	rfile.close()

	c = os.getcwd();
	src = os.path.join(c,filename); 
	if shared.has_key(filename):
		users = shared[filename];
		for uname in users:
			if uname != name:
				pather = os.path.join(path,uname);
				shutil.copy(src,pather);
				if ushared.has_key(uname):
					fileN = ushared[uname];
					if filename in fileN:
						continue
					else:
						fileN.append(filename);
						ushared[uname] = fileN;
				else:
					ushared[uname] = [filename];

	connection.send('File sucessfully updated!')
	print "\n\n\n"
	print "File sucessfully updated!"
	print "\n\n\n"




def Deletion(connection,name):
	global deleted;
	global ushared;# check if update queued for any delted file
	global shared;

	numFiles = connection.recv(1024)
	print numFiles
	connection.send(numFiles)

	num = 1
	numFiles = int(numFiles)

	while num <= numFiles:
		filename = connection.recv(1024)
		print filename
		connection.send(filename)
		if os.path.isfile(filename):
			os.remove(filename);
		print 'File sucessfully deleted!', filename
		num = num + 1;
		print "\n\n\n"

		utli = "Sharefile.dropbin.txt";
		dList = [];
		src = os.getcwd();

		if shared.has_key(filename):
			if os.path.isfile(utli):
				reader = open(utli,"r");
				with reader as f:
					for line in f:
						filer = line.split();
						if filer[0] != filename:
							dList.extend(line);
				reader.close();

				reader = open(utli,"w");
				for x in dList:
					reader.write(x);
				reader.close();
				if ushared.has_key(name):
					lister = ushared[name];
					lister.append(utli);
					ushared[name] = lister;
				else:
					ushared[name] = [utli];

			for users in shared[filename]:
				if users != name:
					dest = os.path.join(path,users);
					os.chdir(path);
					os.chdir(dest);
					os.remove(filename);

					if ushared.has_key(users):
						val = ushared[users]
						if filename in val:
							val.remove(filename);
							ushared[users] = val;

					if deleted.has_key(users):
						lister = deleted[users];
						lister.append(filename);
						deleted[users] = lister;
					else:
						deleted[users] = [filename]; #Check for multiple!!!!

					if os.path.isfile(utli):
						reader = open(utli,"r");
						with reader as f:
							for line in f:
								filer = line.split();
								if filer[0] != filename:
									dList.extend(line);
						reader.close();

						reader = open(utli,"w");
						for x in dList:
							reader.write(x);
						reader.close();

						if ushared.has_key(users):
							lister = ushared[users];
							lister.append(utli);
							ushared[users] = lister;
						else:
							ushared[users] = [utli];


			os.chdir(path);
			del shared[filename];
			# if ushared.has_key(name):
			# 	lister = ushared[name];
			# 	lister.append(utli);
			# 	ushared[name] = lister;
			# else:
			# 	ushared[name] = [utli];




	connection.send('All files Sucessfully Deleted!!!')
	print "All files Sucessfully Deleted!!!"
	print '\n\n\n'



def Creation(connection):
	global x
	numFiles = connection.recv(1024)
	print numFiles
	connection.send(numFiles)

	num = 1
	numFiles = int(numFiles)

	while num <= numFiles:
		filename = connection.recv(1024)
		print filename
		connection.send(filename)

		filesize = connection.recv(1024)
		print filesize
		connection.send(filesize)

		filesize = long(filesize)
		condition = 0

		rfile = open(filename ,"wb" ) #wb means write in binary

		while x > filesize:
			if x > filesize:
				# global x
				x = x - (x/2)
				print x


		print "Starting writing process..."
		while ((condition*x) < filesize ):
			recData = connection.recv(x)
			rfile.write(recData)
			condition = condition + 1

		# global x
		x = 1024

		print "Writing process ended!!"	

		print 'File received and saving...',filename
		rfile.close()
		connection.send('File sucessfully written!')
		print "File sucessfully written!"
		print "\n\n\n"
		num = num + 1

	connection.send('All files Sucessfully created!!!')
	print "All files Sucessfully created!!!"
	print '\n\n\n'

#=========================================================================================




def Update(socks,filename):
	global x
	socks.send(filename)
	ack1 = socks.recv(1024) # acknowledgment for filenmae receival
	# print ack1
	print "Filename sucessfully sent!" , ack1
	# e1024it()


	socks.send(str(os.path.getsize(filename)))
	ack2 = socks.recv(1024)
	# print ack2
	print "Filesize sucessfully sent!" , ack2


	filesize = (os.path.getsize(filename));
	condition = 0;

	sfile = open(filename , "rb") #rb means read in binary

	while x > filesize:
		if x > filesize:
			# global x
			x = x - (x/2)
			print x


	while((condition*x) < filesize ):
		sentData = sfile.read(x)
		socks.send(sentData)
		condition = condition + 1

	# global x
	x = 1024;


	print 'File sent and closing...',filename
	sfile.close()
	print "\n\n\n"
	ack3 = socks.recv(25) # acknowledgment for file process completion
	print ack3
	print "\n\n\n"

def Delete(socks,deleted):


	socks.send(str(len(deleted)))
	ack4 = socks.recv(1024)
	# print ack4
	print "Number of deleted files sucessfully conveyed!", ack4

	numFiles = int(ack4)

	for filename in deleted:

		socks.send(filename)
		ack1 = socks.recv(len(filename)) # acknowledgment for filenmae receival
		# print ack1
		print "Filename sucessfully sent!" , ack1
		print "\n\n\n"
	ack3 = socks.recv(32) # acknowledgment for file process completion
	print ack3
	print "\n\n\n"

def Create(socks,created):

	global x
	# global ushared;

	socks.send(str(len(created)))
	ack4 = socks.recv(1024)
	# print ack4
	print "Number of created files sucessfully conveyed!", ack4




	# print os.getcwd();
	# for filename in os.listdir(os.getcwd()):
	# 	print filename;



	numFiles = int(ack4)

	for filename in created:

		socks.send(filename)
		ack1 = socks.recv(1024) # acknowledgment for filenmae receival
		# print ack1
		print "Filename sucessfully sent!" , ack1
		# e1024it()
		# x = 0
		# while True:
		# 	x = 1;

		socks.send(str(os.path.getsize(filename)))
		ack2 = socks.recv(1024)
		# print ack2
		print "Filesize sucessfully sent!" , ack2


		filesize = (os.path.getsize(filename));
		condition = 0;

		while x > filesize:
			if x > filesize:
				# global x
				x = x - (x/2)
				print x


		sfile = open(filename , "rb") #rb means read in binary

		while((condition*x) < filesize ):
			sentData = sfile.read(x)
			socks.send(sentData)
			condition = condition + 1

		# global x
		x = 1024;

		print 'File sent and closing...',filename
		sfile.close()

		ack3 = socks.recv(25) # acknowledgment for file process completion
		print ack3
		print "\n\n\n"

	ack4 = socks.recv(32) # acknowledgment for file process completion
	print ack4
	print "\n\n\n"




#==========================================================================================

def MainThread(connection,address):
	global database;
	global ushared;
	global unassigned;

	print "New thread created for the following address: ", address
	# print path

	os.chdir(path);
	username = connection.recv(1024)
	print username;

	if database.has_key(username):##keeping track of users in a dictionary, value = list of connections adn address
		# print username," has also logged from the following: ",database[username];
		print "ANOTHER SAME USER!!!!"
		print "\n\n\n"
		just = database[username];
		number = len(just)+1;
		just.append((connection,number));
		database[username] = just #((database[username]).append((connection,(len(database[username])+1))))
		unassigned.append((username,number));
	else:
		print "New User!!!"
		database[username] = [(connection,1)];
		unassigned.append((username,1));
	print database;
	print "\n\n\n"



	connection.send(username)
	if not os.path.exists(username):
		
		os.makedirs(username)
	os.chdir(username)
	myPath = os.getcwd();
	# operation = connection.recv(7)
	# print operation
	# connection.send(operation)

	# if operation == 'Initial':
	# 	print 'Invokes the following operation: ', operation

	# 	os.chdir(myPath)

	# 	Initialization(connection,username)

	# 	os.chdir(path);


	while True:
		# print "At the start AGAIN!!!"
		#receving operation to be e1024ecuted
		operation = connection.recv(7)
		print operation
		connection.send(operation)

		if operation == 'Initial':
			print 'Invokes the following operation: ', operation

			os.chdir(myPath)
	
			Initialization(connection,username)

			os.chdir(path);

		if (operation == 'Create'):
			print 'Invokes the following operation: ', operation

			os.chdir(myPath)

			Creation(connection)

			os.chdir(path);

		if (operation == 'Update'):
			print 'Invokes the following operation: ', operation

			os.chdir(myPath)

			Updation(connection,username)

			os.chdir(path);

		if operation == 'Delete':
			print 'Invokes the following operation: ', operation

			os.chdir(myPath)

			Deletion(connection,username)

			os.chdir(path);
		
		# print database;
		# print "\n\n\n"
		if operation == '':
			print "BYE BYE"
			break;

		# print "\n\n\n"
		# print ushared;
		# print "\n\n\n"

		# if ushared.has_key(username):
		# 	print "YES!!!"
		# 	connection.send("Y");
		# 	# what = connection.recv(1);
		# 	# print what;
		# 	connection.send("Create");
		# 	files = ushared[username];
		# 	# numF = len(files);
		# 	print "Sncy with server started!!"
		# 	print "Shared files: ",files;


		# 	os.chdir(myPath)
		# 	Create(connection,files);
		# 	os.chdir(path)

		# 	del ushared[username];
		# else:
		# 	print "NO!!!"
		# 	connection.send("N");
			# what = connection.recv(1);
			# print what;	

		#
		#

#==========================================================================================
def MonitorThread(connection,adddress):
	global ushared;
	global deleted;
	global monitors;
	global unassigned;


	# print "\n\n\n"
	# print ushared
	# print "\n\n\n"

	nme = connection.recv(20);
	print "Monitor thread Sucessfully created for: ",nme

	idnumber = -1;
	time.sleep(1);
	if unassigned[0][0] == nme:
		print "PAIRING BEING DONE!!!"
		idnumber = unassigned[0][1];
		print idnumber;
		print "\n\n\n"
		removal = unassigned[0];
		unassigned.remove(removal);

	couple = (nme,idnumber);
	print couple;
	active = 1;#len(database[nme]);
	length = len(monitors[nme]);
	while True:
		time.sleep(1);

		# if len(database[nme]) > 1:
		if (active != len(database[nme]))|(length != len(monitors[nme])): #monitors.has_key(nme):
			length = len(monitors[nme]);
			connection.send("Create");
			# print ushared;
			files = monitors[nme];
			# numF = len(files);
			print "Sncy with server started!!"
			print "Shared files: ",files;
			os.chdir(path);
			os.chdir(nme);
			myPath = os.getcwd();
			
			time.sleep(1);
			os.chdir(myPath)
			Create(connection,files);
			os.chdir(path)
			active = len(database[nme]);
			# del monitors[nme];
			print monitors;

		if ushared.has_key(nme):
			print "YES!!!"
			# connection.send("Y");
			# what = connection.recv(1);
			# print what;
			connection.send("Create");
			print ushared;
			files = ushared[nme];
			# numF = len(files);
			print "Sncy with server started!!"
			print "Shared files: ",files;

			os.chdir(path);
			os.chdir(nme);
			myPath = os.getcwd();
			
			time.sleep(1);
			os.chdir(myPath)
			Create(connection,files);
			os.chdir(path)

			del ushared[nme];
			print "\n\n\n"
			print ushared
			print "\n\n\n"
		elif deleted.has_key(nme):
			connection.send("Delete");
			# print ushared;
			files = deleted[nme];
			# numF = len(files);
			print "Sncy with server started!!"
			print "Shared files: ",files;
			os.chdir(path);
			os.chdir(nme);
			myPath = os.getcwd();
			
			time.sleep(1);
			os.chdir(myPath)
			Delete(connection,files);
			os.chdir(path)

			del deleted[nme];
			print "\n\n\n"
			print deleted
			print "\n\n\n"
		# else:
		# 	print "NO!!!"
		# 	connection.send("N");
		# 	what = connection.recv(1);
		# 	print what;	
#==========================================================================================
def exitFunction():
	while True:

		x = raw_input('Press c to EXIT!!!');
		if x == 'c':
			os._exit(0);

#==========================================================================================
def main():

	socks = socket.socket();
	# portNo = input('Enter Port Number: ')
	# serverIP = socket.gethostname();


	# print portNo	# PUT relevent conditions to check for correcness of port number
	# print serverIP
	# print len(sys.argv)
	if len(sys.argv) != 2:
		print "Invalid Inputs!\nExiting..."
		sys.exit();

	portNo = int(sys.argv[1]);

	socks.bind(('0.0.0.0',portNo)); #takes one argument as tuple
	print 'Socket binded'

	socks.listen(10);
	print 'Listening...'

	thread.start_new_thread((exitFunction),());

	while True:

		print 'Waiting for clients...\n\n'
		
		connection,address = socks.accept(); # accepting connection; connection is a new socket for communication adn adrres is a tuple of port and ip
		print 'A client has connected!', address
		print "\n\n\n"
		identity = connection.recv(1);
		print "IDENTITY OF CONNECTION: ", identity
		print "\n\n\n"
		if identity == "U":
			print "Main thread invoked..."
			thread.start_new_thread((MainThread),(connection,address)); #creating new thread for the client 
		elif identity == "M":
			print  "Monitort thread invoked..."
			thread.start_new_thread((MonitorThread),(connection,address));
		# e1024it()


	socks.close();
	print 'Closing...'


if __name__ == '__main__':
	main();