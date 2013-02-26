#!/usr/bin/python

# AV Amp Control Client Code
# Version: 0.1.1
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
# This is a netcat client and calls the server at host & port as specified in the avc.config file or defaults to 3333.
# If no host is specified it exits with an error.
# It takes the command line parameters and passes them to the server.
# It then exits
#

import sys
import os
import ConfigParser
import subprocess

#CONFIG_FILE = "/etc/.avc.conf" ;
CONFIG_FILE = "/home/pjr/workspace/MMS_2_RS232_Control/src/avc_C.conf" ;

port = "3333" ;
host = "" ;

try:
	fconf = open(CONFIG_FILE, 'r');
except IOError :
	#Config file does not exist so exit
	conf = "FALSE";
	print "avcc_client: Error: Config file not found" ;
	sys.exit(1);
else:
	#Config file exist so use it
	print "avcc_client: Config file found" ;
	conf = "TRUE";
	config = ConfigParser.ConfigParser() ;
	config.read(CONFIG_FILE) ;
	port = config.get("Client", "PORT") ;
	host = config.get("Client", "HOST")  ;
	print "avcc_client: From config file, PORT = ", port, " HOST = ", host ;

if port == "":
	#Config file found but port not specified so set
	port = "3333" ;
if host == "" :
	print "avcc_client: Error: no host IP specified" ;
	sys.exit(1);

#NCSERVER = "192.168.1.23" ; 
NCSERVER = host ;

parms = " ".join(sys.argv[1:]) ;
#                                                                                                                                                                                                                               
# Get the commands from the slice passed as the first argument
# and form them into a string
NC = "echo " + parms + "|" + "netcat " + NCSERVER + " " + port + " -q 0" ;

print "avcc_client: netcat server call is: " + NC ;

cmd = NC;
# Now call the netcat sever
try:
	retcode = subprocess.call(cmd, shell=True)
	if retcode < 0:
		print >>sys.stderr, "avcc_client: Child was terminated by signal", -retcode
	else:
		print >>sys.stderr, "avcc_client: Child returned", retcode
except OSError, e:
	print >>sys.stderr, "avcc_client: Execution failed:", e
#os.system (NC) ;

# Finished, exit
sys.exit(0) ;





