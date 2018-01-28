# CAmera class for viewport related things
import cigi_support_methods as host
import cigi_helpers as helper
import math

class Camera():
    # Set up initial values
    def __init__( self, lat = 61.497978, lng = 23.764931, height = 120.0, pitch = -20, yaw = 0, roll = 0):
        self.lat = lat
        self.lng = lng
        self.height = height
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll

    # Update position
    def setposition( self, lat = None, lng = None, height = None, pitch = None, yaw = None, roll = None ):
        self.lat = lat or self.lat
        self.lng = lng or self.lng
        self.height = height or self.height
        self.pitch = pitch or self.pitch
        self.yaw = yaw or self.yaw
        self.roll = roll or self.roll
        
        # Do the actual movement
        self.setmyposition()        

    # Move to given direction
    def move(self, direction):
        print direction
        if direction == "forward":
            # Based on GUI.py. Basic Pythagora s math
            self.lat += math.cos(math.radians(self.yaw)) / 1000
            self.lng += 2 * math.sin(math.radians(self.yaw))/1000
        elif direction == "backward":
            self.lat -= math.cos(math.radians(self.yaw)) / 1000
            self.lng -= 2 * math.sin(math.radians(self.yaw))/1000

        # Set the camera angle to view left or right
        elif direction == "left":
            self.yaw = self.yaw - 10
        elif direction == "right":
            self.yaw = self.yaw + 10
        # Predefined altitudes
        elif direction == "tosky":
            self.height = 120
            self.pitch = -20
        elif direction == "street":
            self.height = 10
            self.pitch = 0
        
        # Stay inside ranges
        if self.yaw > 350:
            self.yaw = 0
        elif self.yaw < 0:
            self.yaw = 350

        print str( self.lat ) + " " + str( self.lng )
        # Update actual position
        self.setmyposition()

    # Just a getter
    def getDirection(self):
        return self.yaw

    # This does the actual call through CIGI
    def setmyposition(self):
        # Make sure user is above ground
        offset = 90 #helper.createHOTQuery(self.lat, self.lng)
        #print offset
        host.set_position(self.lat, self.lng, self.height + offset, self.pitch, self.yaw, self.roll )
