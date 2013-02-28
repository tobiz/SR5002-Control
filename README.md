SR5002-Control
==============

A set of programs and files for network control of a Marantz SR5002 AV Amplifier.
These comprise of:
- an interface program which receives commands for a Marantz SR5002 which is RS232 connected to a remote (ie networked) server
- a client program which receives commands from the interface program and sends them to the remote server
- a server program which receives commands from the client program and sends them to the locally, ie RS232 connected Marantz SR5002
- a configuration file which is used by the above

Therefore the commands destined for the the SR5002 do not have to originate on the computer to which the SR5002 is RS232 connected. (Note, it is of course possible for this to be achieved by the client and server components being co-hosted).

It is envisage that the server would be run on an ultra small low power computer such as a Raspberry Pi but the system does not demand this.

This repository has two examples of the configuration file, one for use with the client avc_C.conf, the other avc_S.conf for use with the server.  The .conf file has to be edited for use in a real application.

There currently is no installation method for this code, I'm working on this. As a result it has to be done by copying the files to /usr/bin for the code and /etc for the config files.

The repository now includes Eclipse Project files and pydev   

This is experimental code at this time.
