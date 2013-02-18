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

This is experimental code at this time.
