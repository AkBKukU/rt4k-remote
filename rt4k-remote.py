#!/usr/bin/env python3

# Python System
import argparse
import datetime
import sys
import os
import json
from pprint import pprint
import asyncio
import signal
from multiprocessing import Process

# External Modules
try:
    import serial
    import serial.tools.list_ports

    def serialByName(name):

        # Lazy wrap both
        if "/dev/" in name:
            return name

        for port in serial.tools.list_ports.comports():
            if port[1] == name:
                return port[0]
except Exception as e:
    print("Need to install Python module [pyserial]")
    sys.exit(1)

class WebInterface(object):
    try:
        # External Modules
        from flask import Flask
        from flask import Response
        from flask import request
        from flask import send_file
        from flask import redirect
        from flask import make_response
        from flask import send_from_directory
    except Exception as e:
            print("Need to install Python module [flask]")
            sys.exit(1)
    """Web interface for managing rips

    """

    def __init__(self,ip,port,serial,split):

        self.host_dir=os.path.realpath(__file__).replace(os.path.basename(__file__),"")
        self.app = self.Flask("Retrotink 4k Remote")
        self.app.logger.disabled = True
        #log = logging.getLogger('werkzeug')
        #log.disabled = True

        # Static content
        self.app.static_folder=self.host_dir+"http/static"
        self.app.static_url_path='/static/'

        # Define routes in class to use with flask
        self.app.add_url_rule('/','home', self.index)
        # Define routes in class to use with flask
        self.app.add_url_rule('/command','command', self.command,methods=["POST"])

        self.host = ip
        self.port = port
        self.serial = serial
        self.toggle = not split



    async def start(self):
        """ Run Flask in a process thread that is non-blocking """
        print("Starting Flask")
        self.web_thread = Process(target=self.app.run,
            kwargs={
                "host":self.host,
                "port":self.port,
                "debug":False,
                "use_reloader":False
                }
            )
        self.web_thread.start()

    def stop(self):
        """ Send SIGKILL and join thread to end Flask server """
        if hasattr(self, "web_thread") and self.web_thread is not None:
            self.web_thread.terminate()
            self.web_thread.join()
        if hasattr(self, "rip_thread"):
            self.rip_thread.terminate()
            self.rip_thread.join()


    def index(self):
        """ Simple class function to send HTML to browser """
        return f"""
<style>
.clearButton {{
    background-color: rgba(0, 0, 0, 0);
}}
</style>
<body style="background-color:#111;">
<script type="text/javascript" src="/static/update.js"> </script>
<div style="position: relative;">
<img id="image" src="/static/RetroTINK-4K_Remote.png" style="width: 100%; height: auto;">
    <a onclick="command(event)" ><div name="pwr on" class="clearButton"  style="position: absolute; left: 17%; top:7%; width: 18%; height: 2.5%;"></div></a>
    <a onclick="command(event)" ><div name="remote pwr" class="clearButton"  style="position: absolute; left: 17%; top:9.5%; width: 18%; height: 2.5%;"></div></a>

    <a onclick="command(event)" ><div name="remote input" class="clearButton"  style="position: absolute; left: 39%; top:7%; width: 12%; height: 2%;"></div></a>
    <a onclick="command(event)" ><div name="remote output" class="clearButton"  style="position: absolute; left: 55%; top:7%; width: 12%; height: 2%;"></div></a>
    <a onclick="command(event)" ><div name="remote scaler" class="clearButton"  style="position: absolute; left: 70%; top:7%; width: 12%; height: 2%;"></div></a>

    <a onclick="command(event)" ><div name="remote sfx" class="clearButton"  style="position: absolute; left: 39%; top:10.3%; width: 12%; height: 2%;"></div></a>
    <a onclick="command(event)" ><div name="remote adc" class="clearButton"  style="position: absolute; left: 55%; top:10.3%; width: 12%; height: 2%;"></div></a>
    <a onclick="command(event)" ><div name="remote prof" class="clearButton"  style="position: absolute; left: 70%; top:10.3%; width: 12%; height: 2%;"></div></a>

    <a onclick="command(event)" ><div name="remote prof1" class="clearButton"  style="position: absolute; left: 17%; top:14%; width: 18%; height: 3%;"></div></a>
    <a onclick="command(event)" ><div name="remote prof2" class="clearButton"  style="position: absolute; left: 41%; top:14%; width: 18%; height: 3%;"></div></a>
    <a onclick="command(event)" ><div name="remote prof3" class="clearButton"  style="position: absolute; left: 64%; top:14%; width: 18%; height: 3%;"></div></a>

    <a onclick="command(event)" ><div name="remote prof4" class="clearButton"  style="position: absolute; left: 17%; top:18.3%; width: 18%; height: 3%;"></div></a>
    <a onclick="command(event)" ><div name="remote prof5" class="clearButton"  style="position: absolute; left: 41%; top:18.3%; width: 18%; height: 3%;"></div></a>
    <a onclick="command(event)" ><div name="remote prof6" class="clearButton"  style="position: absolute; left: 64%; top:18.3%; width: 18%; height: 3%;"></div></a>

    <a onclick="command(event)" ><div name="remote prof7" class="clearButton"  style="position: absolute; left: 17%; top:22.6%; width: 18%; height: 3%;"></div></a>
    <a onclick="command(event)" ><div name="remote prof8" class="clearButton"  style="position: absolute; left: 41%; top:22.6%; width: 18%; height: 3%;"></div></a>
    <a onclick="command(event)" ><div name="remote prof9" class="clearButton"  style="position: absolute; left: 64%; top:22.6%; width: 18%; height: 3%;"></div></a>

    <a onclick="command(event)" ><div name="remote prof10" class="clearButton"  style="position: absolute; left: 17%; top:26.6%; width: 18%; height: 3%;"></div></a>
    <a onclick="command(event)" ><div name="remote prof11" class="clearButton"  style="position: absolute; left: 41%; top:26.6%; width: 18%; height: 3%;"></div></a>
    <a onclick="command(event)" ><div name="remote prof12" class="clearButton"  style="position: absolute; left: 64%; top:26.6%; width: 18%; height: 3%;"></div></a>

    <a onclick="command(event)" ><div name="remote menu" class="clearButton"  style="position: absolute; left: 18%; top: 31.5%; width: 16%; height: 4.5%;"></div></a>
    <a onclick="command(event)" ><div name="remote back" class="clearButton"  style="position: absolute; left: 65%; top: 31.5%; width: 16%; height: 4.5%;"></div></a>
    <a onclick="command(event)" ><div name="remote diag" class="clearButton"  style="position: absolute; left: 18%; top: 45%; width: 16%; height: 4.5%;"></div></a>
    <a onclick="command(event)" ><div name="remote stat" class="clearButton"  style="position: absolute; left: 65%; top: 45%; width: 16%; height: 4.5%;"></div></a>

    <a onclick="command(event)" ><div name="remote up" class="clearButton"  style="position: absolute; left: 37%; top: 33%; width: 25%; height: 4.5%;"></div></a>
    <a onclick="command(event)" ><div name="remote down" class="clearButton"  style="position: absolute; left: 37%; top: 43.7%; width: 25%; height: 4.5%;"></div></a>

    <a onclick="command(event)" ><div name="remote left" class="clearButton"  style="position: absolute; left: 23%; top: 37%; width: 16%; height: 7%;"></div></a>
    <a onclick="command(event)" ><div name="remote right" class="clearButton"  style="position: absolute; left: 60%; top: 37%; width: 16%; height: 7%;"></div></a>

    <a onclick="command(event)" ><div name="remote ok" class="clearButton"  style="position: absolute; left: 41.5%; top: 38.5%; width: 16%; height: 4.5%;"></div></a>

    <a onclick="command(event)" ><div name="remote pause" class="clearButton"  style="position: absolute; left: 41.5%; top: 52%; width: 16%; height: 4.5%;"></div></a>
    <a onclick="command(event)" ><div name="remote safe" class="clearButton"  style="position: absolute; left: 41.5%; top: 57.7%; width: 16%; height: 4.5%;"></div></a>

    <a onclick="command(event)" ><div name="remote gain" class="clearButton"  style="position: absolute; left: 18%; top:51.5%; width: 18%; height: 3%;"></div></a>
    <a onclick="command(event)" ><div name="remote genlock" class="clearButton"  style="position: absolute; left: 63.5%; top:51.5%; width: 18%; height: 3%;"></div></a>
    <a onclick="command(event)" ><div name="remote phase" class="clearButton"  style="position: absolute; left: 18%; top:59.5%; width: 18%; height: 3%;"></div></a>
    <a onclick="command(event)" ><div name="remote buffer" class="clearButton"  style="position: absolute; left: 63.5%; top:59.5%; width: 18%; height: 3%;"></div></a>

    <a onclick="command(event)" ><div name="remote res4k" class="clearButton"  style="position: absolute; left: 17%; top:64.7%; width: 13%; height: 2.5%;"></div></a>
    <a onclick="command(event)" ><div name="remote res1080p" class="clearButton"  style="position: absolute; left: 34.5%; top:64.7%; width: 13%; height: 2.5%;"></div></a>
    <a onclick="command(event)" ><div name="remote res1440p" class="clearButton"  style="position: absolute; left: 51.5%; top:64.7%; width: 13%; height: 2.5%;"></div></a>
    <a onclick="command(event)" ><div name="remote res480p" class="clearButton"  style="position: absolute; left: 69%; top:64.7%; width: 13%; height: 2.5%;"></div></a>

    <a onclick="command(event)" ><div name="remote res1" class="clearButton"  style="position: absolute; left: 17%; top:68.9%; width: 13%; height: 2.5%;"></div></a>
    <a onclick="command(event)" ><div name="remote res2" class="clearButton"  style="position: absolute; left: 34.5%; top:68.9%; width: 13%; height: 2.5%;"></div></a>
    <a onclick="command(event)" ><div name="remote res3" class="clearButton"  style="position: absolute; left: 51.5%; top:68.9%; width: 13%; height: 2.5%;"></div></a>
    <a onclick="command(event)" ><div name="remote res4" class="clearButton"  style="position: absolute; left: 69%; top:68.9%; width: 13%; height: 2.5%;"></div></a>

    <a onclick="command(event)" ><div name="remote aux1" class="clearButton"  style="position: absolute; left: 17%; top:77.2%; width: 13%; height: 2.5%;"></div></a>
    <a onclick="command(event)" ><div name="remote aux2" class="clearButton"  style="position: absolute; left: 34.5%; top:77.2%; width: 13%; height: 2.5%;"></div></a>
    <a onclick="command(event)" ><div name="remote aux3" class="clearButton"  style="position: absolute; left: 51.5%; top:77.2%; width: 13%; height: 2.5%;"></div></a>
    <a onclick="command(event)" ><div name="remote aux4" class="clearButton"  style="position: absolute; left: 69%; top:77.2%; width: 13%; height: 2.5%;"></div></a>

    <a onclick="command(event)" ><div name="remote aux5" class="clearButton"  style="position: absolute; left: 17%; top:81.5%; width: 13%; height: 2.5%;"></div></a>
    <a onclick="command(event)" ><div name="remote aux6" class="clearButton"  style="position: absolute; left: 34.5%; top:81.5%; width: 13%; height: 2.5%;"></div></a>
    <a onclick="command(event)" ><div name="remote aux7" class="clearButton"  style="position: absolute; left: 51.5%; top:81.5%; width: 13%; height: 2.5%;"></div></a>
    <a onclick="command(event)" ><div name="remote aux8" class="clearButton"  style="position: absolute; left: 69%; top:81.5%; width: 13%; height: 2.5%;"></div></a>
</div>
</body>
"""



    def command(self):
        data = self.request.get_json()

        ser = serial.Serial(self.serial,115200,timeout=30,parity=serial.PARITY_NONE,)
        pprint(data)
        if self.toggle and "pwr" in data['cmd']:
            data['cmd'] = "remote pwr\npwr on\n"
        # Send command
        ser.write( bytes(data['cmd']+"\n",'ascii',errors='ignore') )
        return "sure"


# ------ Async Server Handler ------

global loop_state
global server
loop_state = True
server = None


async def asyncLoop():
    """ Blocking main loop to provide time for async tasks to run"""
    print('Blocking main loop')
    global loop_state
    while loop_state:
        await asyncio.sleep(1)


def exit_handler(sig, frame):
    """ Handle CTRL-C to gracefully end program and API connections """
    global loop_state
    print('You pressed Ctrl+C!')
    loop_state = False
    server.stop()


# ------ Async Server Handler ------



async def startWeb(ip,port,serial,split):

    # Internal Modules
    global server
    server = WebInterface(ip,port,serial,split)

    """ Start connections to async modules """

    # Setup CTRL-C signal to end programm
    signal.signal(signal.SIGINT, exit_handler)
    print('Press Ctrl+C to exit program')

    # Start async modules
    L = await asyncio.gather(
        server.start(),
        asyncLoop()
    )



def main():
    """ Execute as a CLI and process parameters

    """
    rt4k_serial=serialByName("FT232R USB UART - FT232R USB UART")
    # Setup CLI arguments
    parser = argparse.ArgumentParser(
                    prog="rt4k-remote",
                    description='Web page remote for serial control of RT4K',
                    epilog='')
    parser.add_argument('-i', '--ip', help="Web server listening IP", default="0.0.0.0")
    parser.add_argument('-p', '--port', help="Web server listening IP", default="5002")
    parser.add_argument('-s', '--serial', help="Serial port", default=rt4k_serial)
    parser.add_argument('-S', '--serial-names', help="List serial port names", action='store_true')
    parser.add_argument('-l', '--split', help="Split power button instead of toggle", action='store_true')
    parser.add_argument('other', help="", default=None, nargs=argparse.REMAINDER)
    args = parser.parse_args()

    if args.serial_names:
        for port in serial.tools.list_ports.comports():
            if port[1] != "n/a":
                print( port[0]+":"+port[1] )
        sys.exit(0)


    # Run web server
    asyncio.run(startWeb(args.ip,args.port,args.serial,args.split))
    sys.exit(0)



if __name__ == "__main__":
    main()
