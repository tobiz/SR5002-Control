#!/usr/bin/python

# AV Amp Control Server Code
# Version: 0.1
# Date: 2013-02-12
#
# Copyright (C) 2012 P.J.Robinson
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# This is a netcat server on port as specified in avc.conf or defaults to 3333.
# It reads its stdin and sends it to the driver specified in avc.conf. If no drivers is specified
# it exits with an error. 
# Each 'request' to the server sends all stdin to the specified driver. 
# If the data received on stdin contains "STOP" then this program terminates. Note anything after "STOP" supplied
# as a command is ignored.
#
# Exit 0: Success, input commands processed
# Exit 1: Error, server not started, reason in log
# Exit 2: STOP command found in input, server stopped

#import serial
import sys
#import time
#import string
import os
import ConfigParser
import subprocess
import logging

CONFIG_FILE = "/etc/avc.conf" ;
port = "3333" ;
tmp = "/tmp/avc.txt" ;
driver = "" ;

#
# Set up logging. This results in program name in output 
#
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)  
 
EXITCODE = 0 ;

try:
	fconf = open(CONFIG_FILE, 'r');
except IOError :
	#Config file does not exist so use defaults
	conf = "FALSE";
	print "Config file not found" ;
	logger.error('Config file not found. Exit')
	sys.exit(1) ;
else:
	#Config file exist so use it
	print "avcc_server.py. Config file found" ;	
	conf = "TRUE";
	config = ConfigParser.ConfigParser() ;
	config.read(CONFIG_FILE) ;
try:
	port = config.get("Server", "PORT") ;
except ConfigParser.NoOptionError :
	print "avcc_server: PORT not specified, default to 3333"
	port = 3333
	
try:
	tmp = config.get("Server", "TMP")  ;
except ConfigParser.NoOptionError :
	print "avcc_serer: TMP not specified, default to /tmp/avc.txt"
	tmp = "/tmp/avc.txt"
	
try:
	driver = config.get("Server", "DRIVER") ;
	
except ConfigParser.NoOptionError :
	print "avcc_server: DRIVER not specifed, Error, exit"
	exit(1)

	
print "avcc_server: From config file, PORT = ", port, " TMP = ", tmp, " DRIVER = ", driver ;



# netcat sends all data it receives on stdout to a temporary file
# PJR use -p option on Raspberry Pi
try:
	USE_P = config.get("Server", "USE_P")
except ConfigParser.NoOptionError :
	print "avcc_server: USE_P not specified, Error, exit"
	exit(1)

if USE_P == "Y" or USE_P == "y":
	p_opt = "-p "
elif USE_P == "N" or USE_P == "n":
	p_opt = " "
else:
	print "avcc_server: USE_P not specified, Error, exit"
	exit(1)
NC = "netcat -l " + p_opt + port + " > " + tmp	

SR5002CMD = driver ;
#STOP command stops the server
STOPCMD = "STOP" ;
#
#These two commands are for the future, the send WoL and shutdown
#
WAKECMD = "WAKE" ;
SLEEPCMD = "SLEEP" ;

# netcat server is started and waits to receive data.
print "Starting Server\n" ;
#Set it such that the cycle starts
nc_cmd = NC
input1 = "";
while input1 != STOPCMD :
	print "avcc_server: command waiting on input is: ", NC ;
	logger.info('Server waiting on command input')
	try:
		retcode = subprocess.call(nc_cmd, shell=True)
		if retcode < 0:
			print >>sys.stderr, "avcc_server: Child was terminated by signal", -retcode
		else:
			print >>sys.stderr, "avcc_server: Child returned", retcode
	except OSError, e:
					print >>sys.stderr, "avcc_server: Execution failed:", e
	#retcode = os.system (NC) ;
	if retcode != 0 :
		# system call failed so exit
		print "avcc_server: Netcat command failed. Exit, code " + str(retcode);
		EXITCODE = retcode ;
		break ;
	
	# netcat server has received some input and has written it to temporary file
	# from stdout
	# Open temporary file for reading.
	# File should have 1 line with all the SR5002 commands on it separated by space
	sr5002cmd = SR5002CMD ;
	print "avcc_server: Received data" ;
	fd = open(tmp, 'r') ;
	fdata = fd.readline() ;
	if fdata.count("STOP") != 0 : 
		#Split the line into commands before a STOP command and the STOP command
		stndcmds, stopcmd = fdata.split("STOP");
		if stndcmds != "" :
			#Commands not null
			print "avcc_server: Standard cmds are: ", stndcmds, "STOP cmd was found" ;
			sr5002cmd = sr5002cmd + " " + stndcmds ;
			# Now run the command
			print "avcc_server: Call is: ", sr5002cmd, " and STOP server" ;
			try:
				retcode = subprocess.call(sr5002cmd, shell=True)
				if retcode < 0:
					print >>sys.stderr, "avcc_server: Child was terminated by signal", -retcode
				else:
					print >>sys.stderr, "avcc_server: Child returned", retcode
			except OSError, e:
					print >>sys.stderr, "avcc_server: Execution failed:", e
			#os.system (sr5002cmd)
		print "avcc_server: STOP command found so exit server" ;
		EXITCODE = 2 ;
		break ; 
	else :
		#No STOP command found so just run the commands
		sr5002cmd = sr5002cmd + " " + fdata ;
		print "avcc_server: Call does not include STOP: ", sr5002cmd ;
		try:
			retcode = subprocess.call(sr5002cmd, shell=True)
			if retcode < 0:
				print >>sys.stderr, "avcc_server: Child was terminated by signal", -retcode
			else:
				print >>sys.stderr, "avcc_server: Child returned", retcode
		except OSError, e:
				print >>sys.stderr, "avcc_server: Execution failed:", e
		#os.system (sr5002cmd)	


# Now delete the temporary file
RMFILE = "rm " + tmp ;
os.system (RMFILE) ;

# Finish, exit
sys.exit(EXITCODE) ;




