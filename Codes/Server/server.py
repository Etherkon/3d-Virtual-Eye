# The old server supporting POST method and parametrization
import sys
import os
import cgi
import urlparse
import BaseHTTPServer
import threading

import random
import math

from cigi_support_methods import *
import cigi_support_methods as host

import picking

# Derive HTTPServer
class RequestHandler( BaseHTTPServer.BaseHTTPRequestHandler ):
    markerID = 1
    # HTTP header
    def do_HEAD(self):
        print "HEAD"
        # Client should not change view
        self.send_response(204)

    # What to do for GET query - not used
    def do_GET(self):
        print "GET"
        self.do_HEAD()
        # Only get single values for each key
        query = dict(urlparse.parse_qsl(urlparse.urlparse(self.path).query))
        set_position(float(query['lat']), float(query['lng']), float(query['height']))
        
    # The actual POST query processing
    def do_POST(self):
        print "POST"
        # Send HTTP HEAD
        self.do_HEAD()
        # Parse the header file
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        
        # Try to get the values
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers.getheader('content-length'))
            # Preserve again only single values for each key
            postvars = dict(cgi.parse_qsl(self.rfile.read(length), keep_blank_values=1))
        else:
            postvars = {}
        print ctype,postvars

        # Check if we ve the correct keys
        if postvars.has_key('type'):
            # Creating markers for restaurants asked
            if postvars['type']=="RESTAURANTS":
                # Adding the restaurants
                print postvars['objects'].split(";")
                for i in postvars['objects'].split(";"):
                    if len(i) != 0:
                        print "adding new objects"
                        coordinate=i.split(",")
                        createEntityAt( float(coordinate[0]), float(coordinate[1]), 1000, self.markerID )
                        self.markerID=self.markerID+1
                        print "Object added, used markerID:" + str(self.markerID)
                self.markerID=0
                
            else:
                # Putting the camera to the correct coordinates
                # Default values
                height = 250
                pitch = -20
                yaw = 0
                roll = 0

                # Check POST parameters
                if postvars.has_key('height'):
                    height = float(postvars['height'])
                if postvars.has_key('pitch'):
                    pitch = float(postvars['pitch'])
                if postvars.has_key('yaw'):
                    yaw = float(postvars['yaw'])
                if postvars.has_key('roll'):
                    roll = float(postvars['roll'])
                        
                # Do stuff
                setposition(float(postvars['lat']), float(postvars['lng']), height, pitch, yaw, roll)

# Set camera position and start screenshotting
def setposition(lat, lng, height=250, pitch=0, yaw=0, roll=0):
    host.set_position(lat, lng, height, pitch, yaw, roll)
    #take_screenshot()
    ScreenShotThread().start()
#    for i in range(360):
#        host.ec.yaw += 1
#        host.UDPSock.sendto(host.ig.pack()+host.ec.pack(),host.addr_send)
#        host.wait_sync()
    print "finish"


def take_screenshot():
    os.system("take_screenshot.exe")

class ScreenShotThread( threading.Thread ):
    def run( self ):
        print "Screenshot thread started"        
        for i in range(10):
            os.system("take_screenshot.exe")
            time.sleep(0.5)

        
if __name__ == '__main__':
    print "Setting CIGI"
    host.create_cigi()
    host.set_default_situation()
    set_currenttime()
    server_ = BaseHTTPServer.HTTPServer
#    t = threading.Timer(0.5, take_screenshot)
#    t.start()

#    scr = ScreenShotThread()
#    scr.start()
    httpd = server_(('', 3001 ), RequestHandler )
    try:
        print "Starting server, use ctrl-C to stop."
        httpd.serve_forever()
    except KeyboardInterrupt:
        print "Got ^C, closing server"
    httpd.server_close()

    print "Shutting down CIGI"
    host.UDPSock.close()
    
    
    
