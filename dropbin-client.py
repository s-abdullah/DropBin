import socket
import thread
import sys
import os
import time


# files = []; # list to store filenames
# metadata = []; # list for storing metadata of files to see when its modified

##CHECK TO UPdATE LIST AFTER CREATION OR DELETION AND KEEPP IT SYNCHRONISED!!!!!!!!!
# global x
x = 1024;
checker = 0;
selector = 0;
shfiles = [];
# x = 1;
def Initialization(socks):
	global x;
	# socks.send(str(len(os.listdir(os.getcwd()))))

	socks.send(str(len(shfiles)));
	ack4 = socks.recv(1024)
	# print ack4
	print "Number of files sucessfully conveyed!", ack4

	numFiles = int(ack4)

	for filename in shfiles: #os.listdir(os.getcwd()):
		# files.append(filename)

		if filename == "dropbin-client.py":
			# print 'PASSSINGGGGG'
			continue
		
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
		# global x
		while x > filesize:
			if x > filesize:
				# global x
				x = x - (x/2)
				print x
		

		while((condition*x) < filesize ):
			sentData = sfile.read(x)
			socks.send(sentData)
			condition = condition + 1
		# sentData = sfile.read(x)
		# socks.send(sentData)
		# global x
		x = 1024

		print 'File sent and closing...',filename
		sfile.close()

		ack3 = socks.recv(25) # acknowledgment for file process completion
		print ack3
		print "\n\n\n"

	# print 'Exited loop'
	ack4 = socks.recv(32) # acknowledgment for file process completion
	print ack4
	print "\n\n\n"
	# print 'EXITTIINNGGG'



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
	socks.send(str(len(created)))
	ack4 = socks.recv(1024)
	# print ack4
	print "Number of created files sucessfully conveyed!", ack4

	numFiles = int(ack4)

	for filename in created:

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
#=====================================================================================
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

def Updation(connection):
	global x
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
	connection.send('File sucessfully updated!')
	print "\n\n\n"
	print "File sucessfully updated!"
	print "\n\n\n"

def Deletion(connection):

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
			os.remove(filename)
		print 'File sucessfully deleted!', filename
		num = num + 1;
		print "\n\n\n"
	connection.send('All files Sucessfully Deleted!!!')
	print "All files Sucessfully Deleted!!!"
	print '\n\n\n'
#====================================================================================

def Monitor(ip,port,name):
	global checker;

	sock = socket.socket();
	sock.connect((ip,port));
	sock.send("M");
	##################
	sock.send(name);
	print "Monitor for user: ",name;
	while True:
		command = sock.recv(6);
		print command;
		print "\n\n\n"
		if command == "Create":
			checker = 1;

			time.sleep(1);
			print "Going Into Function!!!"
			Creation(sock);


			checker = 2;

		elif command == "Delete":
			checker = 1;
			time.sleep(1);
			print "Going Into Function!!!"
			Deletion(sock);


			checker = 2;


		# elif command == "Delete":
		# 	Deletion(socks);

#====================================================================================
def main():
	global checker;
	global selector;
	global shfiles;
	files = []; # list to store filenames
	metadata = []; # list for storing metadata of files to see when its modified
	nfiles = []	#list of cirrent files


	socks = socket.socket();
	# portNo = input('Enter Port Number: ')
	# ipAdd = raw_input('Enter IP Address: ')

	# print portNo
	# print ipAdd # PUT relevant constraintions for checking correctness of ip address and port

	if len(sys.argv) != 4:
		print "Invalid Inputs!\nExiting..."
		sys.exit();

	portNo = int(sys.argv[2]);
	ipAdd = sys.argv[1];
	username = sys.argv[3];


	print 'Connecting...'
	socks.connect((ipAdd,portNo)); # takes one argument as tuple
	socks.send("U");
	thread.start_new_thread((Monitor),(ipAdd,portNo,username));
	#=========================
	#make new thread for recceiveing files from the server

	#=========================


	# username = raw_input('\n\n\nPlease Enter Username: ');
	socks.send(username);
	acku = socks.recv(1024);
	print 'Following User has logged in: ',acku
	print '\n\n\n'


	# print shfiles;
	for filename in os.listdir(os.getcwd()):
		if filename == "Selectfile.dropbin.txt":
			print "FOUND SELECTOR"
			selector = 1;
			selecter = open("Selectfile.dropbin.txt","r");
			shfiles = (selecter.read()).split();
			shfiles.append("Selectfile.dropbin.txt");
			shfiles.append("dropbin-client.py");
			selecter.close();
	print "SELECTOR FILES: "
	print shfiles;

	for filename in os.listdir(os.getcwd()):
		if filename == "Sharefile.dropbin.txt":
			if selector == 1:
			# selecter = open("Selectfile.dropbin.txt","r");
			# shfiles = (selecter.read()).split();
				shfiles.append("Sharefile.dropbin.txt");

	if selector == 0:
		shfiles.extend(os.listdir(os.getcwd()));

	# print shfiles;
	numFiles = len(os.listdir(os.getcwd()));
	# numFiles = len(shfiles) #len(os.listdir(os.getcwd()))

	for filename in shfiles: #os.listdir(os.getcwd()):
		nfiles.append(filename)
		files.append(filename)
		metadata.append((filename,os.stat(filename).st_mtime))


	socks.send('Initial')
	op = socks.recv(1024)
	print op

	Initialization(socks);




	while True:
		if checker == 0:
			if selector == 0:
				#
				#
				#
				# socks.send("NOOO!!!")
				# redund = socks.recv(7);
				# print "REDUNDANCY",redund;
				# first checking for creation
				# print "At the start AGAIN!!!"
				time.sleep(2);# delay so that complete operations are read/ gave problem with delteion, detected less deletetions
				if ( len(os.listdir(os.getcwd())) > numFiles):
					print "FILE CREATED!!"
					# numFiles = len(os.listdir(os.getcwd())) # updating number of files

					del nfiles[:];
					for filename in os.listdir(os.getcwd()): #creating list of current files
						nfiles.append(filename)


					print files
					print nfiles
					created = list(set(nfiles) - set(files)) # set operation to see which file is deleted wont work other way around
					print created

					# socks.send(username);
					# acku = socks.recv(1024);
					# print 'Following User : ',acku

					socks.send('Create')
					op = socks.recv(1024)
					print op

					Create(socks,created);

					numFiles = len(os.listdir(os.getcwd())) # updating number of files

					del files[:];# deleting elements 
					del metadata[:];# deleting elements 
					for filename in os.listdir(os.getcwd()):
						files.append(filename)
						metadata.append((filename,os.stat(filename).st_mtime))

					# print files[0]


				# second checking for file deletion
				if ( len(os.listdir(os.getcwd())) < numFiles):
					print "FILE DELETED!!"
					# numFiles = len(os.listdir(os.getcwd())) # updating number of files
					
					del metadata[:];# deleting elements 
					del nfiles[:];
					for filename in os.listdir(os.getcwd()): #creating list of current files
						nfiles.append(filename)
						metadata.append((filename,os.stat(filename).st_mtime))


					deleted = list(set(files) - set(nfiles)) # set operation to see which file is deleted, wont work other way around
					print deleted
					

					# socks.send(username);
					# acku = socks.recv(1024);
					# print 'Following User : ',acku

					socks.send('Delete')
					op = socks.recv(1024)
					print op
					
					Delete(socks,deleted);

					numFiles = len(os.listdir(os.getcwd())) # updating number of files
					# files = nfiles # updating list/does not make a difference
					del files[:];# deleting elements 
					del metadata[:];# deleting elements 
					for filename in os.listdir(os.getcwd()):
						files.append(filename)
						metadata.append((filename,os.stat(filename).st_mtime))
		 
				# Third check for updates using last modified in metadata of file
				for filename in os.listdir(os.getcwd()): #creating list of current files
					for i,prevfilename in enumerate(metadata):#to get data and also modifiy the list

						if (str(prevfilename[0]) == str(filename)):

							if prevfilename[1] != os.stat(filename).st_mtime:
			
								metadata[i] = (filename,os.stat(filename).st_mtime);

								# socks.send(username);
								# acku = socks.recv(1024);
								# print 'Following User : ',acku

								socks.send('Update')
								op = socks.recv(1024)
								print op

								Update(socks,filename)

				##=================================checking for shared files
				# time.sleep(1);
				# notice = socks.recv(1);
				# print notice;
				# # socks.send(notice);
				# if notice == "N":
				# 	continue
				# elif notice == "Y":
				# 	command = socks.recv(6);
				# 	print command;
				# 	if command == "Create":
				# 		Creation(socks);

				# 		numFiles = len(os.listdir(os.getcwd())) # updating number of files

				# 		del files[:];# deleting elements 
				# 		del metadata[:];# deleting elements 
				# 		for filename in os.listdir(os.getcwd()):
				# 			files.append(filename)
				# 			metadata.append((filename,os.stat(filename).st_mtime))



				# 	elif command == "Delete":
						# 		Deletion(socks);

			if selector == 1:
				print "SELECTOOOOORRR"
				time.sleep(2);# delay so that complete operations are read/ gave problem with delteion, detected less deletetions
				if ( len(os.listdir(os.getcwd())) > numFiles):
					print "FILE CREATED!!"
					# numFiles = len(os.listdir(os.getcwd())) # updating number of files

					del nfiles[:];
					for filename in os.listdir(os.getcwd()): #creating list of current files
						nfiles.append(filename)


					print files
					print nfiles
					created = list(set(nfiles) - set(files)) # set operation to see which file is deleted wont work other way around
					print created

					# socks.send(username);
					# acku = socks.recv(1024);
					# print 'Following User : ',acku

					socks.send('Create')
					op = socks.recv(1024)
					print op

					Create(socks,created);

					numFiles = len(os.listdir(os.getcwd())) # updating number of files


					del files[:];# deleting elements 
					del metadata[:];# deleting elements 
					for filename in os.listdir(os.getcwd()):
						files.append(filename)
						metadata.append((filename,os.stat(filename).st_mtime))

					print files[0]


				# second checking for file deletion
				if ( len(os.listdir(os.getcwd())) < numFiles):
					print "FILE DELETED!!"
					# numFiles = len(os.listdir(os.getcwd())) # updating number of files
					dshfiles = []
					for filename in os.listdir(os.getcwd()):
						if filename in shfiles:
							dshfiles.append(filename);
					del metadata[:];# deleting elements 
					del nfiles[:];
					for filename in dshfiles: #os.listdir(os.getcwd()): #creating list of current files
						nfiles.append(filename)
						metadata.append((filename,os.stat(filename).st_mtime))


					deleted = list(set(files) - set(nfiles)) # set operation to see which file is deleted, wont work other way around
					print deleted
					

					# socks.send(username);
					# acku = socks.recv(1024);
					# print 'Following User : ',acku
					if bool(deleted):
						if "Selectfile.dropbin.txt" in deleted:
							socks.send('Delete')
							op = socks.recv(1024)
							print op
							
							Delete(socks,deleted);
							for dname in deleted:
								if dname in shfiles:
									shfiles.remove(dname);
							selector = 0;

							shfiles = os.listdir(os.getcwd());
							socks.send('Initial')
							op = socks.recv(1024)
							print op

							Initialization(socks);
							# numFiles = len(shfiles) #len(os.listdir(os.getcwd())) # updating number of files
							numFiles = len(shfiles) #len(os.listdir(os.getcwd())) # updating number of files
							# files = nfiles # updating list/does not make a difference
							del files[:];# deleting elements 
							del metadata[:];# deleting elements 
							for filename in shfiles: #os.listdir(os.getcwd()):
								files.append(filename)
								metadata.append((filename,os.stat(filename).st_mtime))

						else:
							socks.send('Delete')
							op = socks.recv(1024)
							print op
							
							Delete(socks,deleted);
							for dname in deleted:
								shfiles.remove(dname);

							numFiles = len(shfiles) #len(os.listdir(os.getcwd())) # updating number of files
							# files = nfiles # updating list/does not make a difference
							del files[:];# deleting elements 
							del metadata[:];# deleting elements 
							for filename in shfiles: #os.listdir(os.getcwd()):
								files.append(filename)
								metadata.append((filename,os.stat(filename).st_mtime))
		 
				# Third check for updates using last modified in metadata of file
				for filename in shfiles: #os.listdir(os.getcwd()): #creating list of current files
					for i,prevfilename in enumerate(metadata):#to get data and also modifiy the list

						if (str(prevfilename[0]) == str(filename)):

							if prevfilename[1] != os.stat(filename).st_mtime:
			
								metadata[i] = (filename,os.stat(filename).st_mtime);

								# socks.send(username);
								# acku = socks.recv(1024);
								# print 'Following User : ',acku

								socks.send('Update')
								op = socks.recv(1024)
								print op

								Update(socks,filename)

		elif checker == 2:
			numFiles = len(shfiles); #len(os.listdir(os.getcwd())) # updating number of files

			del files[:];# deleting elements 
			del metadata[:];# deleting elements 
			for filename in shfiles: #os.listdir(os.getcwd()):
				files.append(filename)
				metadata.append((filename,os.stat(filename).st_mtime))
			checker = 0;


	socks.close();
	print 'closing...'


if __name__ == '__main__':
	main();