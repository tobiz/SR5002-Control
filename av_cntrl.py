#!/usr/bin/python

# Name:       av_cntrl.py
# Version:    0.1.1

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
# Simple py-serial program to send control codes to RS232 port of the
# Maranatz SR5002.
# Sends a py-serial command to the RS232 port for each argument
# If a config file exists then configuration data is used from this file and
# it runs as a client to a network server.
#
# This is used on the client side with a config file
# On the server side without a config file

import serial
import sys
import time
import ConfigParser
import os

#
#Check whether the av amp control config file exists, avc.conf.
#If it does use the IP address from config as that for the server.
#If not the assume this is running on machine connected to the AV amp
#via the usb port.
#Format of the config file is:
# [Driver]
#     DRIVER: Y|N {If Y then use USB0, if N then call specified local client}
#    USBDEVICE: usb device to be used
#    WAIT: S. S is time in seconds to wait for a response
#     USBDEV: USB device to be used by driver
#     RS232 control values and defaults
#     BAUDRATE: baudrate = 9600
#     RTSCTS: rtscts = 0
#     XONXOFF: xonxoff = 0
#     REP_MODE: repr_mode = 0
#     RDTMOUNT: rdtmout = 0.5
# [Client]
#     HOST: <host_name>|<host_IP>
#     PORT: <port_number_server_uses>
#     CLIENT: <file_name_to_be_called_as_client_end>
# [Server]
#     PORT: <port_number_to_listen_on> Default = 3333
#     USE_P: Y|N Y, specify "-p" on netcat call
#     TMP: <file_name_of_temporary_file>



CONFIG_FILE = "/etc/avc.conf" ;
try:
  fconf = open(CONFIG_FILE, 'r');
except IOError :
  #Config file does not exist, this is a major error - exit
  conf = "FALSE";
  print "ERROR: av_cntrl.py. Config file not found" ;
  sys.exit(1);

#Config file exist so use it
print "av_cntrl.py. Config file found" ;
conf = "TRUE";
# Parse the config file andd extract the data
config = ConfigParser.SafeConfigParser() ;
config.read(CONFIG_FILE) ;
#
# Get values from config file
#
driver = "Y"
try:
    driver = config.get("Driver", "DRIVER")
except ConfigParser.NoOptionError :
    driver = "Y"
if driver == "Y":
    #
    # Called as a Driver
    #
    try:
        baudrate = config.get("Driver", "BAUDRATE");
    except ConfigParser.NoOptionError :
        baudrate = 9600;

    try:
        rtscts = config.get("Driver", "RTSCTS");
    except ConfigParser.NoOptionError :
        rtscts = 0;

    try:
        xonxoff = config.get("Driver", "XONXOFF");
    except ConfigParser.NoOptionError :
        xonxoff = 9600;

    try:
        repr_mode = config.get("Driver", "REP_MODE");
    except ConfigParser.NoOptionError :
        repr_mode = 9600;
    
    try:
        rdtmout = config.get("Driver", "RDTMOUNT");
    except ConfigParser.NoOptionError :
        rdtmout = 0.5;

    # If config file includes a WAIT time then use that else default to 0.3 secs
    try:
        wait_s = config.get("Driver", "WAIT") ;
        wait_t = float(wait_s) ;
        print "Wait time is: ";
        print wait_t ;
        print " secs";
    except ConfigParser.NoOptionError :
        # wait time defaults to 0.3 secs
        wait_t = 0.3 ;
    
    try:
        usb_dev = config.get("Driver", "USBDEV")
    except ConfigParser.NoOptionError :
        print "av_cntrl: No USB port specified for Driver, Exit"
        exit(1)
# Not sure host and port are needed here?
if config.has_section("Client"):
    print "av_cntrl: Client Section found"
    try:
        host = config.get("Client", "HOST") ;
    except ConfigParser.NoOptionError :
        print "av_cntrl: HOST for server not specified, failure, exit"
        exit(1)
        
    try:
        port = config.get("Client", "PORT")  ;
    except ConfigParser.NoOptionError :
        print "av_cntrl: PORT not specified, default to 3333"
        port = 3333
        
    try:
        client = config.get("Client", "CLIENT") ;
    except ConfigParser.NoOptionError :
        print "av_cntrl: CLIENT not specified, failure, exit"
        exit(1)
        
    print "From config file, HOST = ", host, " PORT = ", port, " CLIENT = ", client, " DRIVER = ", driver
            
def av_cntrl (data):
    rtn = 1
    if driver == "N" :
        #
        # Configured to call as Client
        #
        print "av_cntrl: Driver = N"
        rtn = call_as_client (data)
    elif driver == "Y":
        #
        # Configured to call as Driver
        #
        print "av_cntrl: Driver = Y"
        rtn = call_as_driver (data)
    return (rtn)
    
def call_as_client (data):
    # Prog to call is made from client prog name plus all parameters passed to this command
    print "Configured to use as a Client so use Client command" ;
    #CMD = client + " " + " ".join(sys.argv[1:]) ;
    #CMD = client + " " + " ".join(data[1:]) ;;
    CMD = client + " " + data
    print "Client called as: " + CMD;
    # Now execute the command to call the client which will communicate with the server
    os.system(CMD);
    #sys.exit(0);
    return(0)
                
def call_as_driver (data):
    #
    # Called as a Driver so get the driver RS232 values from config file
    #
    print "Configured as a Driver so use USB port on this machine"
    usb_dev = config.get("Driver", "USBDEV") ;
    if usb_dev == "" :
        print "ERROR: av_contrl.py. No usb device specified so exit" ;
        sys.exit(1) ;
    else :
        print "av.cntrl.py. USB device is: " + usb_dev ;
    print "av_cntrl.py: param data = " 
    print data
    params = data.split()
    nos_params = len(params)
    #print "av_cntrl: params after split = " + str(params)
    #print "av_cntrl: nos params = " + str(len(params))
    # Now call the local driver on USB0
    

    #                                                                                                                                                                                                                               
    # Get the commands from the parameter list and send them one by one
    #


    #
    # Uncomment these to work
    #
    #ser=serial.Serial(usb_dev, baudrate, rtscts=rtscts, xonxoff=xonxoff, timeout=rdtmout);
    #ser.open() ;

    for i in range (0, nos_params):
       #cmd = '@' + sys.argv[i] + '\r' 
       cmd = '@' + params[i] + '\r'
       print 'Cmd=' + cmd ;    
       #print 'Before write' , time.time() ;
       #rtn = ser.write(cmd);
       #print 'After write' , time.time() ;
       time.sleep(wait_t) ;    
       #print 'Before read' , time.time() ;
       #rd = ser.read(size=8) ;    
       #print 'After read' , time.time() ;
       #print 'rtn=' , rtn ;
       #print 'read rtn=' , rd ;

    #ser.close() ;
    #sys.exit(0) ;
    return(0)

#
# Just for testng the above
#
if __name__ == "__main__":
    #cmd = " \"SUR:0J\"" + " \"SPK:3\"" + " \"SPK:2\"" + " \"DCT:12\""
    cmd = sys.argv[1:]
    print "av_cntrl-1: cmd = " 
    print cmd
    parms = " ".join(cmd)
    #print "parms = " + parms
    print "av_cntrl-1 TEST: Called with: " + parms
    av_cntrl(parms)
