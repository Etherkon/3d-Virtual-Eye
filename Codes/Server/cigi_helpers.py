import os
from cigi_support_methods import *
import cigi_support_methods as support

# Camera object has been previously created ( id 0 )
# To check if weve already created the entity
entities = set([0])
# Array to store ids in order theyre created
entityids = [0]

# Creates entity on given position
def createEntityAt( lat, lng, objectID, entID, direction = 0, 
    entityalt = 150.0 ):
    print "Creating entity: " + str(entID)
    # Set up symbols
    UDPSock = support.UDPSock
    ec = support.ec
    ig = support.ig
    addr_send = support.addr_send
    entityalt = entityalt #+ createHOTQuery(lat, lng)
    #sleep(10)
    # create another entity or use previously created
    entity_1 = cigi_packet_classes.EntityControl(entID)
    
    # Set the parameters and turn the entity by 90 degrees
    entity_1.set(lat,lng,entityalt,0,0,direction-90,1,objectID)
    # Send CIGI packet
    UDPSock.sendto(ig.pack()+entity_1.pack(),addr_send)

    # Append new id into list. -- Not tested
    if entID not in entities:
        entityids.append(entID)
        entities.add(entID)

#    sleep(60)    

# Gets entity ID based on its creation number
def getEntityID( creationid ):
    # Actually not tested during project
    return entityids[creationid]


#Mo-#     +y -z      
#ni-#       \I
#tor#    +x--*--(-x)   Viewer  ## So +x is into monitor
#   #        I\
#   #       +z -y

# Craetes Line-of-Sight Query - based on example given by Insta
def createLOSQuery(offset_y = 0, offset_z = 0, offset_x = 0):

    UDPSock = support.UDPSock
    ec = support.ec
    ig = support.ig
    addr_send = support.addr_send

    # Create line of sight vector query
    los_vec = cigi_packet_classes.lineOfSightVectorRequest()
    los_vec.losId = 1
    los_vec.requestType = 1 # 1 = extended
    los_vec.responseCoordinateSystem = 0 # geodetic
    los_vec.sourcePointCoordinateSystem = 1 # geodetic
    los_vec.sourceLatitude = 0 #offset_x
    los_vec.sourceLongitude = 0 # offset_y
    los_vec.sourceAltitude = 0#offset_z
    los_vec.azimuth = offset_y
    los_vec.elevation = offset_z
    los_vec.minimumRange = 10
    los_vec.maximumRange = 5000
    los_data = los_vec.pack()
    print "Created LOS request"
    print "Source lat: " + str(los_vec.sourceLatitude)
    print "Source lon: " + str(los_vec.sourceLongitude)
    print "Source alt: " + str(los_vec.sourceAltitude)
    print "Source azimuth: " + str(los_vec.azimuth)
    print "Source pitch: " + str(los_vec.elevation) + "\n"

    
    # Create los response packet
    loser = cigi_packet_classes.lineOfSightExtendedResponse()
    
    # Send query
    UDPSock.sendto(ig.pack()+ec.pack()+los_data,addr_send)

    
    # Wait for response
    while 1:
        UDPSock.sendto(ig.pack()+ec.pack(), addr_send)
        data = wait_sync() # "data" contains IG return values

        # -- LOS response received? --
        ret, ret_data = cigi_packet_classes.analyse_data(data, 105)
        if ret:
            loser.unpack(ret_data)
            print "LosID: " + str(loser.losId)
            if loser.losId == 1:
                print "LOS response received"
                print "Lat: " + str(loser.latitude)
                print "Lon: " + str(loser.longitude)
                print "Alt: " + str(loser.altitude)
                print "Range: " + str(loser.range) + " meters"
                if loser.entityIdValid == 1:
                    print ("Entity: " + str(loser.entityId ))
                    print ("valid: " + str( loser.valid ))
                    print ("evalid: " + str( loser.entityIdValid ))
                    print ("visible: " + str( loser.visible ))
                    print ("red: " + str( loser.red ))
                    print ("mat: " + str( loser.materialCode ))
                break
                
        else:
            pass
            #print "Waiting for response..."
    return loser

# Create Height-of-Terrain query on given point.
# Based on createLOSQuery
def createHOTQuery(lat, lng):
    UDPSock = support.UDPSock
    ec = support.ec
    ig = support.ig
    addr_send = support.addr_send

    # Create Height of Terrain query
    hotq = cigi_packet_classes.hatHotRequest()
    hotq.hatHotId = 1
    hotq.requestType = 1 # HAT = 0, HOT = 1, HAT&HOT = 2
    hotq.coordinateSystem = 0 # Geodetic = 0, Entity = 1
    hotq.updatePeriod = 0
    hotq.entityId = 0
    hotq.latitude = lat
    hotq.longitude = lng
    hotq.altitude = 0
    hot_data = hotq.pack()

    # Send query
    UDPSock.sendto(ig.pack()+ec.pack()+hot_data,addr_send)

    hotanswer = cigi_packet_classes.hatHotResponse()

    # Wait for response
    while 1:
        UDPSock.sendto(ig.pack()+ec.pack(), addr_send)
        data = wait_sync() # "data" contains IG return values

        # -- HOT response received? --
        ret, ret_data = cigi_packet_classes.analyse_data(data, 102)
        if ret:
            hotanswer.unpack(ret_data)
            print "HotID: " + str(hotanswer.hatHotId)
            if hotanswer.hatHotId == 1 and hotanswer.valid:
                return hotanswer.height

    print( "No answer")


# Takes screenshot using screenshot program
def take_screenshot():
    os.system("take_screenshot.exe")



