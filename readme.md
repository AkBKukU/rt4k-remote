# RT4K Remote

This is a very simple python script for controlling a Retrotink 4k Pro over 
serial through a web interface. It mimicks the remote entirely as an image
allowing the user to click the buttons to send the commands.

## Usage

When launching the script you can provide a serial port for the RT4k as well as
an IP address and port on your computer to listen on. By default after running
the script you can find the remote at: http://127.0.0.1:5002/ . You can dock
this page in OBS to directly control the RT4k from there once the script is 
running.

## Script Help

	$ ./rt4k-remote.py -h
	usage: rt4k-remote [-h] [-i IP] [-p PORT] [-s SERIAL] ...

	Web page remote for serial control of RT4K

	positional arguments:
	other

	options:
	-h, --help           show this help message and exit
	-i, --ip IP          Web server listening IP
	-p, --port PORT      Web server listening IP
	-s, --serial SERIAL  Serial port


## Installation

You will need Python3 and the `pyserial` and `flask` modules installed in order
to use this. It has only been tested on linux.
