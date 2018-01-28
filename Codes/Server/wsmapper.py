## Maps Websocket messages to CIGI messages
# Propably not needed in this module anymore but just here to be sure
import time

# For taking screenshots in separate thread
import threading

# Insta s library for dealing with CIGI
import cigi_support_methods as host

# Our library to shorten some thing with CIGI
import cigi_helpers as helper

# For getting weather information
import helpers.weather as weather
from helpers.camera import *

# To store Websocket instances
connections = []

# Mapping for 3d objects
markers = {
    "restaurant" : 1000,
    "cafe"       : 1001,
    "bar"        : 1002
}

# Just testing the simple mutex in Python
#screenshot_lock = threading.Lock()

# This thread takes screenshots by calling some screenshotting program
class ScreenShotThread( threading.Thread ):
    # Needs the Websocket instance, which is calling and how many times to 
    #take a screenshot
    def __init__(self, wsock, updates = 10):
        self.ws = wsock
        self.updates = updates
        # Call parent
        threading.Thread.__init__(self)
    
    # Called whenever the thread is started
    def run( self ):
        print "Screenshot thread started"
        # Lock the screenshotting
        #screenshot_lock.acquire()
        try:
            for i in range(self.updates):
                helper.take_screenshot()
                # Wait for half second
                time.sleep(0.5)
                # Ask client to update itself
                self.ws.write_message("screenshotted")
        finally:
            #screenshot_lock.release()
            print "Screenshot thread finished"

# This class parses parametrized strings and calls approviate methods with 
#correct parameters
class WSMapper():
    # To save each clients image size to be used later
    img_sizex = 0
    img_sizey = 0

    # Need to know which websocket connection called
    def __init__(self, wsocket):
        self.ws = wsocket
        # Create Camera instance
        self.cam = Camera()
    
    ##@classmethod
    # This could be class method since SimCore handles only one camera entity
    def setposition(self, params):
        # Not the prettiest way to do in Python
        if len(params) == 2:
            self.cam.setposition(float(params[0]), float(params[1]))
        elif len(params) == 3: 
            self.cam.setposition(float(params[0]), float(params[1]), 
                float(params[2]))
        else:
            self.cam.setposition(float(params[0]), float(params[1]), 
                float(params[2]), float(params[3]), float(params[4]), 
                float(params[5]))
        # After setting position start screenshotting
        ScreenShotThread(self.ws).start()

    ##@classmethod
    # This was never used but could set camera angles
    def setcamera(self, params):
        if len(params) == 1:
            self.cam.setposition( pitch = float(params[0]) )
        else:
            self.cam.setposition( pitch = float(params[0]), 
                yaw = float(params[0]), roll = float(params[0]) )

    #Affects globally
    # Sets up weather based on given condition
    @classmethod
    def setweather(cls, params):
        weather.setweather(params[0])

    # Sets time to server time
    @classmethod
    def settime( cls, params ):
        host.set_currenttime()
    ##@classmethod
    # Call camera s move method
    def movecamera(self, params):
        self.cam.move(params[0])
        ScreenShotThread(self.ws,1).start()

    ##@classmethod
    # This could be made better by proving different markers for each user
    def createmarker(self, params):
        # Set up default type
        placetype = "cafe"
        # check if we can find the type from parameters
        if params[0] in markers:
            placetype = markers.get(params[0])

        # This might bug up if the place type is not in the parameters list
        if len(params) == 4:
            helper.createEntityAt( float(params[1]), float(params[2]), 
                placetype, float(params[3]))
        else:
            pass
            #createEntityAt( params[0], params[1], markers.get(params[2]), 
            #entID, entityalt = 150.0 )

    # This is the actual method used for creating markers by client input
    # Parameter is a string with latitude and longitude coordinates separated 
    # by a comma
    def multicreatemarkers(self, params):
        # First parameter here is the type of the place, which was not used
        params.pop(0)
       
        # Go through the list containing 
        #[lat,lng][lat,lng][lat,lng][lat,lng] items
        for coord in params:
            print( "FOO" )
            # Split each coord into two components
            coords = coord.split(',')
            # We manually restrict objects to be restaurants
            # Also, set direction of the models to be same as the camera
            helper.createEntityAt( float(coords[0]), float(coords[1]), 1000, 
                float(coords[2]),self.cam.getDirection()) 

    # This would be better if we truly supported multi-user environment.
    ##@classmethod
    # Check if object was clicked
    def clicked(self,params):
        # Get the screen coordinates
        scr_x = float(params[0])
        scr_y = float(params[1])

        # Range( angle ) for LOSQuery
        max_yangle = 32
        max_xangle = 40
        # It would be better to precalculate this
        scr_x = ((scr_x + self.img_sizex/2) / (self.img_sizex)) * 
        (max_xangle * 2) - max_xangle
        # Invert the y -axis
        scr_y = -(((scr_y + self.img_sizey/2) / (self.img_sizey)) * 
            (max_yangle * 2) - max_yangle)
        
        print str(scr_x) + " " + str(scr_y)
        
        # Do the query with given angle
        ret = helper.createLOSQuery(scr_x, scr_y)

        # Check the result
        if not ret.entityIdValid:
            if ret.valid:
                pass
                #helper.createEntityAt(ret.latitude, ret.longitude, 1004, 3,0 )
                #ScreenShotThread(self.ws,1).start()

        # If something was hit, then inform client
        if( ret.entityIdValid ):
            self.ws.write_message( "clicked: " + 
                helper.getEntityID(ret.entityId))

    # possibly no need to use separately - When thinking again, propably not
    # a good idea
    @classmethod
    def setimagesize(cls, params):
        # Set image size based on client feedback for screen to cigi conversion
        cls.img_sizex = float(params[0])
        cls.img_sizey = float(params[1])

