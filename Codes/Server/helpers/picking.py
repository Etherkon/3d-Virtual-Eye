# This was initially thought to be used for clicking image to 
# CIGI conversion

# CIGI packets and methods
import cigi_support_methods as host
from cigi_helpers import *

# Takes screen coordinates and translates them
# and returns resulting entity if found
def projection_conversion( screen_x, screen_y ):
    ret = createLOSQuery( screen_x, screen_y )
    if not ret.valid:
        print "Into the space"
        return False
    elif not ret.entityIdValid:
        print "clicked at: " + str(screen_x) + " " + str(screen_y)
        print "on: " + str(ret.latitude) + " " + str(ret.longitude)
        #createEntityAt( ret.latitude, ret.longitude, 1000, 12,50 )
    else:
        #createEntityAt( ret.latitude, ret.longitude, 1004, 13,150 )        
        print( ret.entityId )
        return ret.entityId

##def set_testposition( lat=61.49, lng=23.77, height=250, pitch=-90, yaw=0, roll=0 ):
##    host.ec.set( lat, lng, height, roll, pitch, yaw )
##    host.UDPSock.sendto(host.ig.pack()+host.ec.pack(),host.addr_send)
##    host.sleep(120)
##
##host.create_cigi()
##host.set_default_situation()
##set_testposition(61.495, height=500)
##projection_conversion( 32.5,32.5 )



