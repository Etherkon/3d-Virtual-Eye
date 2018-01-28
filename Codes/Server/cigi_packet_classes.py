# coding=utf-8
# This contains code from Insta as it was.

import struct

class EntityControl():
    def __init__(self, entityId = 0):
        self.format = "BBHBBBBHHfffddd"

        self.packetId = 2
        self.size = 48

        self.entityId = entityId
        self.entityState = 0
        self.attachState = 0
        self.collisionDetectionEnable = 0
        self.inheritAlpha = 0
        self.groundOceanClamp = 0
        self.animationDirection = 0
        self.animationLoopMode = 0
        self.animationState = 0
        self.alpha = 0
        self.entityType = 0
        self.parentId = 0
        self.roll = 0
        self.pitch = 0
        self.yaw = 0
        self.latitude = 0
        self.longitude = 0
        self.altitude = 0

       
    def set(self, lat = "NA",lon = "NA",alt = "NA",roll = "NA",pitch = "NA",yaw = "NA",state = "NA",entityType = "NA"):
        if lat != "NA":
            self.latitude = lat
        if lon != "NA":
            self.longitude = lon
        if alt != "NA":
            self.altitude = alt
        if roll != "NA":
            self.roll = roll
        if pitch != "NA":
            self.pitch = pitch
        if yaw != "NA":
            self.yaw = yaw
        if state != "NA":
            self.entityState = state
        if entityType != "NA":
            self.entityType = entityType

    def pack(self):
        if struct.calcsize(self.format) != self.size:
            print "*** Error in EntityControl packet format: ", struct.calcsize(self.format), " vs ", self.size

        return struct.pack(self.format,
            # rivi 1
            self.packetId, self.size, self.entityId,
            # rivi 2
            (self.entityState & 0x03) | ((self.attachState & 0x01) << 2) | ((self.collisionDetectionEnable & 0x01) << 3) | ((self.inheritAlpha & 0x01) << 4) | ((self.groundOceanClamp & 0x03) << 5),
            (self.animationDirection & 0x01) | ((self.animationLoopMode & 0x01) << 1) | ((self.animationState & 0x03) << 2),
            self.alpha, 0,
            # rivi 3
            self.entityType, self.parentId,
            # loput
            self.roll,
            self.pitch,
            self.yaw,
            self.latitude,
            self.longitude,
            self.altitude
            )

    def unpack(self, data):
        byte1 = 0
        byte2 = 0
        reserved = 0
        packetId = 0
        size = 0

        # rivi 1
        (packetId, size, self.entityId,
        # rivi 2
        byte1, byte2, self.alpha, reserved,
        # rivi 3
        self.entityType, self.parentId,
        # loput
        self.roll,
        self.pitch,
        self.yaw,
        self.latitude,
        self.longitude,
        self.altitude) = struct.unpack(self.format, data)

        # print struct.unpack(self.format, data)

        self.entityState = byte1 & 0x03
        self.attachState = (byte1 >> 2) & 0x01
        self.collisionDetectionEnable = (byte1 >> 3) & 0x01
        self.inheritAlpha = (byte1 >> 4) & 0x01
        self.groundOceanClamp = (byte1 >> 5) & 0x03

        self.animationDirection = byte2 & 0x01
        self.animationLoopMode = (byte2 >> 1) & 0x01
        self.animationState = (byte2 >> 2) & 0x03

        if packetId != self.packetId:
            print "*** Error in EntityControl packet id: ", packetId, " vs ", self.packetId
        if size != self.size:
            print "*** Error in EntityControl packet id: ", size, " vs ", self.size

           
class IGControl():
    def __init__(self):
        self.format = "BBBBBBHIIII"

        self.packetId = 1
        self.size = 24

        self.majorVersion = 3
        self.databaseNumber = 0
        self.minorVersion = 2
        self.IGMode = 1 
        self.timestampValid = 1
        self.extrapolationEnable = 0
        self.magicNumber = 0
        self.hostFrameNumber = 1
        self.timestamp = 0
        self.lastIGFrameNumber = 0


    def pack(self):
        self.hostFrameNumber += 1
        
        if struct.calcsize(self.format) != self.size:
            print "*** Error in IGControl packet format: ", struct.calcsize(self.format), " vs ", self.size

        return struct.pack(self.format,
            # rivi 1
            self.packetId, self.size, self.majorVersion, self.databaseNumber,
            # rivi 2
            (self.IGMode & 0x01) | ((self.timestampValid & 0x01) << 2) | ((self.extrapolationEnable & 0x01) << 3) | ((self.minorVersion & 0x0f) << 4), 0, self.magicNumber,
            # loput
            self.hostFrameNumber, self.timestamp, self.lastIGFrameNumber, 0)

    def unpack(self, data):
        byte1 = 0
        byte2 = 0
        reserved = 0
        magic = 0
        packetId = 0
        size = 0

        # rivi 1
        (packetId, size, self.majorVersion, self.databaseNumber,
        # rivi 2
        byte1, reserved, magic,
        # loput
        self.hostFrameNumber, self.timestamp, self.lastIGFrameNumber, reserved) = struct.unpack(self.format, data)
        
        # print struct.unpack(self.format, data)
        self.IGMode = byte1 & 0x03
        self.timestampValid = (byte1 >> 2) & 0x01
        self.extrapolationEnable = (byte1 >> 3) & 0x01
        self.minorVersion = (byte1 >> 4) & 0x0f
        
        if packetId != self.packetId:
            print "*** Error in IGControl packet id: ", packetId, " vs ", self.packetId
        if size != self.size:
            print "*** Error in IGControl packet id: ", size, " vs ", self.size

 
class atmosphereControl():
    def __init__(self):
        self.format = "BBBBfffffff"

        self.packetId = 10
        self.size = 32
        
        self.atmosphericModelEnable = 0
        self.globalHumidity = 0
        self.globalAirTemperature = 0
        self.globalVisibilityRange = 0
        self.globalHorizontalWindSpeed = 0
        self.globalVerticalWindSpeed = 0
        self.globalWindDirection = 0
        self.globalBarometricPressure = 0
                        
    def pack(self):
    
        if struct.calcsize(self.format) != self.size:
            print "*** Error in atmosphereControl packet format: ", struct.calcsize(self.format), " vs ", self.size

        return struct.pack(self.format,
            # rivi 1
            self.packetId, self.size, (self.atmosphericModelEnable & 0x01), self.globalHumidity,
            # loput
            self.globalAirTemperature,
            self.globalVisibilityRange,
            self.globalHorizontalWindSpeed,
            self.globalVerticalWindSpeed,
            self.globalWindDirection,
            self.globalBarometricPressure, 0 )
            
class positionRequest():
    def __init__(self):
        self.format = "BBHBBH"

        self.packetId = 27
        self.size = 8
        
        self.objectId = 0
        self.articulatedPartId = 0
        self.updateMode = 0
        self.objectClass = 0
        self.coordinateSystem = 0
                        
    def pack(self):
    
        if struct.calcsize(self.format) != self.size:
            print "*** Error in positionRequest packet format: ", struct.calcsize(self.format), " vs ", self.size

        return struct.pack(self.format,
            # rivi 1
            self.packetId, self.size, self.objectId,
            # rivi 2
            self.articulatedPartId, (self.updateMode & 0x01) | ((self.objectClass & 0x07) << 1) | ((self.coordinateSystem & 0x03) << 4), 0)

    def unpack(self, data):
        byte1 = 0
        reserved = 0
        packetId = 0
        size = 0

        # rivi 1
        (packetId, size, self.objectId,
        # rivi 2
        self.articulatedPartId, byte1, reserved) = struct.unpack(self.format, data)
        
        # print struct.unpack(self.format, data)
        self.updateMode = byte1 & 0x01
        self.objectClass = (byte1 >> 1) & 0x07
        self.coordinateSystem = (byte1 >> 4) & 0x03

        if packetId != self.packetId:
            print "*** Error in positionRequest packet id: ", packetId, " vs ", self.packetId
        if size != self.size:
            print "*** Error in positionRequest packet id: ", size, " vs ", self.size            

            
class positionResponse():
    def __init__(self):
        self.format = "BBHBBHdddffff"

        self.packetId = 108
        self.size = 48
        
        self.objectId = 0
        self.articulatedPartId = 0
        self.objectClass = 0
        self.coordinateSystem = 0
        self.latitude = 0
        self.longitude = 0
        self.altitude = 0
        self.roll = 0
        self.pitch = 0
        self.yaw = 0
                        

    def unpack(self, data):
        byte1 = 0
        reserved = 0
        packetId = 0
        size = 0

        # rivi 1
        (packetId, size, self.objectId,
        # rivi 2
        self.articulatedPartId, byte1, reserved,
        # loput
        self.latitude,
        self.longitude,
        self.altitude,
        self.roll,
        self.pitch,
        self.yaw,
        reserved) = struct.unpack(self.format, data)
        
        # print struct.unpack(self.format, data)
        
        self.objectClass = byte1 & 0x07
        self.coordinateSystem = (byte1 >> 3) & 0x03

        if packetId != self.packetId:
            print "*** Error in positionResponse packet id: ", packetId, " vs ", self.packetId
        if size != self.size:
            print "*** Error in positionResponse packet id: ", size, " vs ", self.size
            
            
class lineOfSightSegmentRequest():
    def __init__(self):
        self.format = "BBHBBHddddddIBBH"

        self.packetId = 25
        self.size = 64

        self.losId = 0

        self.requestType = 0
        self.sourcePointCoordinateSystem = 0
        self.destinationPointCoordinateSystem = 0
        self.responseCoordinateSystem = 0
        self.destinationEntityIdValid = 0
        
        self.alphaThreshold = 0
        self.entityId = 0
        self.sourceLatitude = 0
        self.sourceLongitude = 0
        self.sourceAltitude = 0
        self.destinationLatitude = 0
        self.destinationLongitude = 0
        self.destinationAltitude = 0
        self.materialMask = 0
        self.updatePeriod = 0
        self.destinationEntityId = 0
                
    def pack(self):
    
        if struct.calcsize(self.format) != self.size:
            print "*** Error in lineOfSightSegmentRequest packet format: ", struct.calcsize(self.format), " vs ", self.size

        return struct.pack(self.format,
            # rivi 1
            self.packetId, self.size, self.losId,
            # rivi 2
            (self.requestType & 0x01) | ((self.sourcePointCoordinateSystem & 0x01) << 1) | ((self.destinationPointCoordinateSystem & 0x01) << 2) | ((self.responseCoordinateSystem & 0x01) << 3 ) | ((self.destinationEntityIdValid & 0x01) << 4 ), self.alphaThreshold, self.entityId,
            # loput
            self.sourceLatitude,
            self.sourceLongitude,
            self.sourceAltitude,
            self.destinationLatitude,
            self.destinationLongitude,
            self.destinationAltitude,
            self.materialMask,
            self.updatePeriod, 0, self.destinationEntityId)

    def unpack(self, data):
        byte1 = 0
        byte2 = 0
        reserved = 0
        magic = 0
        packetId = 0
        size = 0

        # rivi 1
        (packetId, size, self.losId,
        # rivi 2
        byte1, self.alphaThreshold, self.entityId,
        # loput
        self.sourceLatitude,
        self.sourceLongitude,
        self.sourceAltitude,
        self.destinationLatitude,
        self.destinationLongitude,
        self.destinationAltitude,
        self.materialMask,
        self.updatePeriod, 
        reserved, 
        self.destinationEntityId) = struct.unpack(self.format, data)
        
    
        # print struct.unpack(self.format, data)
            
        self.requestType = byte1 & 0x01
        self.sourcePointCoordinateSystem = (byte1 >> 1) & 0x01
        self.destinationPointCoordinateSystem = (byte1 >> 2) & 0x01
        self.responseCoordinateSystem = (byte1 >> 3) & 0x01
        self.destinationEntityIdValid = (byte1 >> 4) & 0x01
    
        if packetId != self.packetId:
            print "*** Error in lineOfSightSegmentRequest packet id: ", packetId, " vs ", self.packetId
        if size != self.size:
            print "*** Error in lineOfSightSegmentRequest packet id: ", size, " vs ", self.size            
            

class lineOfSightVectorRequest():
    def __init__(self):
        self.format = "BBHBBHffffdddIBBBB"

        self.packetId = 26
        self.size = 56

        self.losId = 0
        self.responseCoordinateSystem = 0
        self.sourcePointCoordinateSystem = 0
        self.requestType = 0
        self.alphaThreshold = 0
        self.entityId = 0
        self.azimuth = 0
        self.elevation = 0
        self.minimumRange = 0
        self.maximumRange = 0
        self.sourceLatitude = 0
        self.sourceLongitude = 0
        self.sourceAltitude = 0
        self.materialMask = 0
        self.updatePeriod = 0
                
    def pack(self):
    
        if struct.calcsize(self.format) != self.size:
            print "*** Error in lineOfSightVectorRequest packet format: ", struct.calcsize(self.format), " vs ", self.size

        return struct.pack(self.format,
            # rivi 1
            self.packetId, self.size, self.losId,
            # rivi 2
            (self.requestType & 0x01) | ((self.sourcePointCoordinateSystem & 0x01) << 1) | ((self.responseCoordinateSystem & 0x01) << 2), self.alphaThreshold, self.entityId,
            # loput
            self.azimuth,
            self.elevation,
            self.minimumRange,
            self.maximumRange,
            self.sourceLatitude,
            self.sourceLongitude,
            self.sourceAltitude,
            self.materialMask,
            self.updatePeriod, 0, 0, 0)

    def unpack(self, data):
        byte1 = 0
        byte2 = 0
        reserved = 0
        magic = 0
        packetId = 0
        size = 0

        # rivi 1
        (packetId, size, self.losId,
        # rivi 2
        byte1, self.alphaThreshold, self.entityId,
        # loput
        self.azimuth,
        self.elevation,
        self.minimumRange,
        self.maximumRange,
        self.sourceLatitude,
        self.sourceLongitude,
        self.sourceAltitude,
        self.materialMask,
        self.updatePeriod,
        reserved, reserved, reserved) =  struct.unpack(self.format, data)
        
        # print struct.unpack(self.format, data)
                
        self.requestType = byte1 & 0x01
        self.sourcePointCoordinateSystem = (byte1 >> 1) & 0x01
        self.responseCoordinateSystem = (byte1 >> 2) & 0x01
    
        if packetId != self.packetId:
            print "*** Error in lineOfSightVectorRequest packet id: ", packetId, " vs ", self.packetId
        if size != self.size:
            print "*** Error in lineOfSightVectorRequest packet id: ", size, " vs ", self.size    

            
class lineOfSightResponse():
    def __init__(self):
        self.format = "BBHBBHd"

        self.packetId = 104
        self.size = 16

        self.losId = 0
        self.valid = 0
        self.entityIdValid = 0
        self.visible = 0
        self.hostFrameNumber = 0
        self.responseCount = 0
        self.entityId = 0
        self.range = 0
                        

    def unpack(self, data):
        byte1 = 0
        byte2 = 0
        reserved = 0
        magic = 0
        packetId = 0
        size = 0

        # rivi 1
        (packetId, size, self.losId,
        # rivi 2
        byte1, self.responseCount, self.entityId,
        # loput
        self.range) = struct.unpack(self.format, data)
                
        # print struct.unpack(self.format, data)
        self.valid = byte1 & 0x01
        self.entityIdValid = (byte1 >> 1) & 0x01
        self.visible = (byte1 >> 2) & 0x01
        self.hostFrameNumber = (byte1 >> 4) & 0xf
    
        if packetId != self.packetId:
            print "*** Error in lineOfSightResponse packet id: ", packetId, " vs ", self.packetId
        if size != self.size:
            print "*** Error in lineOfSightResponse packet id: ", size, " vs ", self.size    

class lineOfSightExtendedResponse():
    def __init__(self):
        self.format = "BBHBBHddddBBBBIII"

        self.packetId = 105
        self.size = 56

        self.losId = 0
        self.valid = 0
        self.entityIdValid = 0
        self.rangeValid = 0
        self.visible = 0
        self.hostFrameNumber = 0
        self.responseCount = 0
        self.entityId = 0
        self.range = 0
        self.latitude = 0
        self.longitude = 0
        self.altitude = 0
        self.red = 0
        self.green = 0
        self.blue = 0
        self.alpha = 0
        self.materialCode = 0
        self.azimuth = 0
        self.elevation = 0
                        

    def unpack(self, data):
        byte1 = 0
        byte2 = 0
        reserved = 0
        magic = 0
        packetId = 0
        size = 0

        # rivi 1
        (packetId, size, self.losId,
        # rivi 2
        byte1, self.responseCount, self.entityId,
        # loput
        self.range,
        self.latitude,
        self.longitude,
        self.altitude,
        self.red,
        self.green,
        self.blue,
        self.alpha,
        self.materialCode,
        self.azimuth,
        self.elevation) = struct.unpack(self.format, data)
                
        # print struct.unpack(self.format, data)
        
        self.valid = byte1 & 0x01
        self.entityIdValid = (byte1 >> 1) & 0x01
        self.rangeValid = (byte1 >> 2) & 0x01
        self.visible = (byte1 >> 4) & 0x01
        self.hostFrameNumber = (byte1 >> 4) & 0xf
    
        if packetId != self.packetId:
            print "*** Error in lineOfSightExtendedResponse packet id: ", packetId, " vs ", self.packetId
        if size != self.size:
            print "*** Error in lineOfSightExtendedResponse packet id: ", size, " vs ", self.size    
            
            
            
class ViewDef():
    def __init__(self):
        self.format = "BBHBBBBffffff"

        self.packetId = 21
        self.size = 32

        self.viewId = 0
        self.groupId = 0
        self.nearEnable = 0
        self.farEnable = 0
        self.leftEnable = 0
        self.rightEnable = 0
        self.topEnable = 0
        self.bottomEnable = 0
        self.mirrorMode = 0
        self.pixelReplicationMode = 0
        self.projectionType = 0
        self.reorder = 0
        self.viewType = 0
        self.near = 0
        self.far = 0
        self.left = 0
        self.right = 0
        self.top = 0
        self.bottom = 0
        
        

    def pack(self):
        if struct.calcsize(self.format) != self.size:
            print "*** Error in ViewDef packet format: ", struct.calcsize(self.format), " vs ", self.size

        return struct.pack(self.format,
            # rivi 1
            self.packetId, self.size, self.viewId,
            # rivi 2
            self.groupId, (self.nearEnable & 0x01) | ((self.farEnable & 0x01) << 1) | ((self.leftEnable & 0x01) << 2) | ((self.rightEnable & 0x01) << 3) | ((self.topEnable & 0x01) << 4) | ((self.bottomEnable & 0x01) << 5) | (( self.mirrorMode & 0x03) << 6),        
            (self.pixelReplicationMode & 0x07) | (( self.projectionType & 0x01)  << 3) | (( self.reorder & 0x01)  << 4) | (( self.viewType & 0x07)  << 5), 0,
            # loput
            self.near,
            self.far,
            self.left,
            self.right,
            self.top,
            self.bottom)

    def unpack(self, data):
        byte1 = 0
        byte2 = 0
        reserved = 0
        packetId = 0
        size = 0

        # rivi 1
        (packetId, size, self.viewId,
        # rivi 2
        self.groupId, byte1, byte2, reserved,
        # loput
        self.near,
        self.far,
        self.left,
        self.right,
        self.top,
        self.bottom) = struct.unpack(self.format, data)
        
        #print struct.unpack(self.format, data)
        self.nearEnable = byte1 & 0x01
        self.farEnable = (byte1 >> 1) & 0x01
        self.leftEnable = (byte1 >> 2) & 0x01
        self.rightEnable = (byte1 >> 3) & 0x01
        self.topEnable = (byte1 >> 4) & 0x01
        self.bottomEnable = (byte1 >> 5) & 0x01
        self.mirrorMode = (byte1 >> 6) & 0x03
        self.pixelReplicationMode = byte2 & 0x07
        self.projectionType = (byte2 >> 3) & 0x01
        self.reorder = (byte2 >> 4) & 0x01
        self.viewType = (byte2 >> 5) & 0x07
            
    
        if packetId != self.packetId:
            print "*** Error in ViewDef packet id: ", packetId, " vs ", self.packetId
        if size != self.size:
            print "*** Error in ViewDef packet id: ", size, " vs ", self.size


class ViewControl():
    def __init__(self):
        self.format = "BBHBBHffffff"

        self.packetId = 16
        self.size = 32

        self.viewId = 0
        self.groupId = 0
        self.xOffsetEnable = 0
        self.yOffsetEnable = 0
        self.zOffsetEnable = 0
        self.rollEnable = 0
        self.pitchEnable = 0
        self.yawEnable = 0
        self.entityId = 0
        self.xOffset = 0
        self.yOffset = 0
        self.zOffset = 0
        self.roll = 0
        self.pitch = 0
        self.yaw = 0
        
    

    def pack(self):
        if struct.calcsize(self.format) != self.size:
            print "*** Error in ViewControl packet format: ", struct.calcsize(self.format), " vs ", self.size

        return struct.pack(self.format,
            # rivi 1
            self.packetId, self.size, self.viewId,
            # rivi 2
            self.groupId, (self.xOffsetEnable & 0x01) | ((self.yOffsetEnable & 0x01) << 1) | ((self.zOffsetEnable & 0x01) << 2) | ((self.rollEnable & 0x01) << 3) | ((self.pitchEnable & 0x01) << 4) | ((self.yawEnable & 0x01) << 5), self.entityId,
            # loput
            self.xOffset,
            self.yOffset,
            self.zOffset,
            self.roll,
            self.pitch,
            self.yaw)

    def unpack(self, data):
        byte1 = 0
        byte2 = 0
        reserved = 0
        packetId = 0
        size = 0

        # rivi 1
        (packetId, size, self.viewId,
        # rivi 2
        self.groupId, byte1, self.entityId,
        # loput
        self.xOffset,
        self.yOffset,
        self.zOffset,
        self.roll,
        self.pitch,
        self.yaw)  = struct.unpack(self.format, data)
        
        #print struct.unpack(self.format, data)
        self.xOffsetEnable = byte1 & 0x01
        self.yOffsetEnable = (byte1 >> 1) & 0x01
        self.zOffsetEnable = (byte1 >> 2) & 0x01
        self.rollEnable = (byte1 >> 3) & 0x01
        self.pitchEnable = (byte1 >> 4) & 0x01
        self.yawEnable = (byte1 >> 5) & 0x01
        
        if packetId != self.packetId:
            print "*** Error in ViewControl packet id: ", packetId, " vs ", self.packetId
        if size != self.size:
            print "*** Error in ViewControl packet id: ", size, " vs ", self.size
            

            
class hatHotRequest():
    def __init__(self):
        self.format = "BBHBBHddd"

        self.packetId = 24
        self.size = 32

        self.hatHotId = 0
        self.requestType = 0
        self.coordinateSystem = 0
        self.updatePeriod = 0
        self.entityId = 0
        self.latitude = 0
        self.longitude = 0
        self.altitude = 0

    def pack(self):
        if struct.calcsize(self.format) != self.size:
            print "*** Error in HatHotRequest packet format: ", struct.calcsize(self.format), " vs ", self.size

        return struct.pack(self.format,
            # rivi 1
            self.packetId, self.size, self.hatHotId,
            # rivi 2
            (self.requestType & 0x03) | (( self.coordinateSystem & 0x01) << 2), self.updatePeriod, self.entityId,
            # loput
            self.latitude,
            self.longitude,
            self.altitude)

    def unpack(self, data):
        byte1 = 0
        byte2 = 0
        reserved = 0
        packetId = 0
        size = 0

        # rivi 1
        (packetId, size, self.hatHotId,
        # rivi 2
        byte1, self.updatePeriod, self.entityId,
        # loput
        self.latitude,
        self.longitude,
        self.altitude) = struct.unpack(self.format, data)
        
        #print struct.unpack(self.format, data)
        self.requestType = byte1 & 0x03
        self.coordinateSystem = (byte1 >> 2) & 0x01
        
        if packetId != self.packetId:
            print "*** Error in HAT/HOT request packet id: ", packetId, " vs ", self.packetId
        if size != self.size:
            print "*** Error in HAT/HOT request id: ", size, " vs ", self.size            
            

class hatHotResponse():
    def __init__(self):
        self.format = "BBHBBBBd"

        self.packetId = 102
        self.size = 16

        self.hatHotId = 0
        self.hostFrameNumber = 0
        self.responseType = 0
        self.valid = 0
        self.height = 0
    
    def unpack(self, data):
        byte1 = 0
        reserved = 0
        packetId = 0
        size = 0

        # rivi 1
        (packetId, size, self.hatHotId,
        # rivi 2
        byte1, reserved, reserved, reserved,
        #loput
        self.height) = struct.unpack(self.format, data)
        
        self.valid = byte1 & 0x01
        self.responseType = (byte1 >> 1) & 0x01
        self.hostFrameNumber = (byte1 >> 4) & 0xf
        
        #print struct.unpack(self.format, data)
        
        if packetId != self.packetId:
            print "*** Error in hatHotResponse packet id: ", packetId, " vs ", self.packetId
        if size != self.size:
            print "*** Error in hatHotResponse id: ", size, " vs ", self.size            


class hatHotExtendedResponse():
    def __init__(self):
        self.format = "BBHBBBBddIffHH"

        self.packetId = 103
        self.size = 40

        self.hatHotId = 0
        self.hostFrameNumber = 0
        self.valid = 0
        self.hat = 0
        self.hot = 0
        self.materialCode = 0
        self.normalVectorAzimuth = 0
        self.normalVectorElevation = 0
    
    def unpack(self, data):
        byte1 = 0
        reserved = 0
        packetId = 0
        size = 0

        # rivi 1
        (packetId, size, self.hatHotId,
        # rivi 2
        byte1, reserved, reserved, reserved,
        #loput
        self.hat, 
        self.hot,
        self.materialCode,
        self.normalVectorAzimuth,
        self.normalVectorElevation,
        reserved, reserved) = struct.unpack(self.format, data)
        
        self.valid = byte1 & 0x01
        self.hostFrameNumber = (byte1 >> 4) & 0xf
        
        #print struct.unpack(self.format, data)
        
        if packetId != self.packetId:
            print "*** Error in hatHotExtendedResponse packet id: ", packetId, " vs ", self.packetId
        if size != self.size:
            print "*** Error in hatHotExtendedResponse id: ", size, " vs ", self.size    
            
class weatherControl():
    def __init__(self):
        self.format = "BBHBBBBffffffffffff"

        self.packetId = 12
        self.size = 56

        self.entityId = 0
        self.layerId = 0
        self.humidity = 0
        self.weatherEnable = 0
        self.scudEnable = 0
        self.randomWindsEnable = 0
        self.randomLightningEnable = 0
        self.cloudType = 0
        self.scope = 0
        self.severity = 0
        self.airTemperature = 0
        self.visibilityRange = 0
        self.scudFrequency = 0
        self.coverage = 0
        self.baseElevation = 0
        self.thickness = 0
        self.transitionBand = 0
        self.horizontalWindSpeed = 0
        self.verticalWindSpeed = 0
        self.windDirection = 0
        self.barometricPressure = 0
        self.AerosolConcentration = 0
        

    def pack(self):
        if struct.calcsize(self.format) != self.size:
            print "*** Error in Weather Control packet format: ", struct.calcsize(self.format), " vs ", self.size

        return struct.pack(self.format,
            # rivi 1
            self.packetId, self.size, self.entityId,
            # rivi 2
            self.layerId, self.humidity, (self.weatherEnable & 0x01) | ((self.scudEnable & 0x01) << 1) | ((self.randomWindsEnable & 0x01) << 2) | ((self.randomLightningEnable & 0x01) << 3) | ((self.cloudType & 0x0f) << 4),
            (self.scope & 0x03) | ((self.severity & 0x07) << 2),
            # loput
            self.airTemperature,
            self.visibilityRange,
            self.scudFrequency,
            self.coverage,
            self.baseElevation,
            self.thickness,
            self.transitionBand,
            self.horizontalWindSpeed,
            self.verticalWindSpeed,
            self.windDirection,
            self.barometricPressure,
            self.AerosolConcentration)

    def unpack(self, data):
        byte1 = 0
        byte2 = 0
        reserved = 0
        packetId = 0
        size = 0

        # rivi 1
        (packetId, size, self.entityId,
        # rivi 2
        self.layerId, self.humidity, byte1, byte2,
        # loput
        self.airTemperature,
        self.visibilityRange,
        self.scudFrequency,
        self.coverage,
        self.baseElevation,
        self.thickness,
        self.transitionBand,
        self.horizontalWindSpeed,
        self.verticalWindSpeed,
        self.windDirection,
        self.barometricPressure,
        self.AerosolConcentration) = struct.unpack(self.format, data)
    
        self.weatherEnable = byte1 & 0x01
        self.scudEnable = (byte1 >> 1) & 0x01
        self.randomWindsEnable = (byte1 >> 2) & 0x01
        self.randomLightningEnable = (byte1 >> 3) & 0x01
        self.cloudType = (byte1 >> 4) & 0x0f
        self.scope = byte2 & 0x03
        self.severity = (byte2 >> 2) & 0x07
    
        #print struct.unpack(self.format, data)
        
        if packetId != self.packetId:
            print "*** Error in Weather Control packet id: ", packetId, " vs ", self.packetId
        if size != self.size:
            print "*** Error in Weather Control id: ", size, " vs ", self.size        
            

class startOfFrame():
    def __init__(self):
        self.format = "BBBBBBHIIII"

        self.packetId = 101
        self.size = 24

        self.majorVersion = 0
        self.databaseNumber = 0
        self.IGStatusCode = 0
        self.minorVersion = 0
        self.IGMode = 0
        self.timestampValid = 0
        self.earthReferenceModel = 0
        self.magicNumber = 0
        self.IGFrameNumber = 0
        self.timestamp = 0
        self.lastHostFrameNumber = 0
        
    def unpack(self, data):
        byte1 = 0
        byte2 = 0
        reserved = 0
        packetId = 0
        size = 0

        # rivi 1
        (packetId, size, self.majorVersion, self.databaseNumber,
        # rivi 2
        self.IGStatusCode, byte1, magicNumber,
        #loput
        self.IGFrameNumber,
        self.timestamp,
        self.lastHostFrameNumber,
        reserved) = struct.unpack(self.format, data)
        
        self.IGMode = byte1 & 0x03
        self.timestampValid = (byte1 >> 2) & 0x01
        self.earthReferenceModel = (byte1 >> 3) & 0x01
        self.minorVersion = (byte1 >> 4) & 0x0f
        
        #print struct.unpack(self.format, data)
        
        if packetId != self.packetId:
            print "*** Error in Start of Frame packet id: ", packetId, " vs ", self.packetId
        if size != self.size:
            print "*** Error in Start of Frame id: ", size, " vs ", self.size                        
            
class collisionDetectionVolumeNotification():
    def __init__(self):
        self.format = "BBHBBHBBBBHH"

        self.packetId = 114
        self.size = 16

        self.entityId = 0
        self.volumeId = 0
        self.collisionType = 0
        self.contactedEntityId = 0
        self.contactedVolumeId = 0
        
    def unpack(self, data):
        byte1 = 0
        byte2 = 0
        reserved = 0
        packetId = 0
        size = 0

        # rivi 1
        (packetId, size, self.entityId,
        # rivi 2
        self.volumeId,byte1, self.contactedEntityId,
        #loput
        self.contactedVolumeId, reserve1, reserved, reserved,
        reserved, reserved) = struct.unpack(self.format, data)
        
        self.collisionType = byte1 & 0x01
        
        #print struct.unpack(self.format, data)
        
        if packetId != self.packetId:
            print "*** Error in Collision Detection Volume Notification packet id: ", packetId, " vs ", self.packetId
        if size != self.size:
            print "*** Error in Collision Detection Volume Notification id: ", size, " vs ", self.size                        
                        
class conformalClampedEntityControl():
    def __init__(self):
        self.format = "BBHfdd"

        self.packetId = 3
        self.size = 24
        self.entityId = 0
        self.yaw = 0
        self.latitude = 0
        self.longitude = 0
        

    def pack(self):
        if struct.calcsize(self.format) != self.size:
            print "*** Error in conformal clamped entity control packet format: ", struct.calcsize(self.format), " vs ", self.size

        return struct.pack(self.format,
            # rivi 1
            self.packetId, self.size, self.entityId,
            # rivi 2
            self.yaw,
            # loput
            self.latitude,
            self.longitude) 
    
    def unpack(self, data):
        packetId = 0
        size = 0

        # rivi 1
        (packetId, size, self.entityId,
        # loput
        self.yaw,
        self.latitude,
        self.longitude) = struct.unpack(self.format, data)

        #print struct.unpack(self.format, data)

        if packetId != self.packetId:
            print "*** Error in Conformal clamped entity control packet packet id: ", packetId, " vs ", self.packetId
        if size != self.size:
            print "*** Error in Conformal clamped entity control packet id: ", size, " vs ", self.size


class componentControl():
    def __init__(self):
        
        self.format = "BBHHBBffffff"

        self.packetId = 4
        self.size = 32
        self.componentId = 0
        self.instanceId = 0
        self.componentClass = 0
        self.componentState = 0
        self.componentData1 = 0
        self.componentData2 = 0
        self.componentData3 = 0
        self.componentData4 = 0
        self.componentData5 = 0
        self.componentData6 = 0

    def set(self, iid = "NA",cclass = "NA",cid = "NA",state = "NA",data1 = "NA",data2 = "NA",data3 = "NA",data4 = "NA",data5 = "NA",data6 = "NA"):
        if iid != "NA":
            self.instanceId = iid
        if cclass != "NA":
            self.componentClass = cclass
        if  cid != "NA":
            self.componentId = cid
        if  state != "NA":
            self.componentState = state
        if  data1 != "NA":
            self.componentData1 = data1
        if  data2 != "NA":
            self.componentData2 = data2
        if  data3 != "NA":
            self.componentData3 = data3
        if  data4 != "NA":
            self.componentData4 = data4
        if  data5 != "NA":
            self.componentData5 = data5
        if  data6 != "NA":
            self.componentData6 = data6
        

        
    def pack(self):
        if struct.calcsize(self.format) != self.size:
            print "*** Error in component control packet format: ", struct.calcsize(self.format), " vs ", self.size

        return struct.pack(self.format,
            # rivi 1
            self.packetId, self.size, self.componentId,
            # rivi 2
            self.instanceId, self.componentClass, self.componentState,
            # loput
            self.componentData1, 
            self.componentData2, 
            self.componentData3, 
            self.componentData4, 
            self.componentData5, 
            self.componentData6)
    
    def unpack(self, data):
        packetId = 0
        size = 0

        # rivi 1
        (packetId, size, self.componentId,
        # rivi 2
        self.instanceId, self.componentClass, self.componentState,
        # loput
        self.componentData1, 
        self.componentData2, 
        self.componentData3, 
        self.componentData4, 
        self.componentData5, 
        self.componentData6) = struct.unpack(self.format, data)

        #print struct.unpack(self.format, data)

        if packetId != self.packetId:
            print "*** Error in component control packet packet id: ", packetId, " vs ", self.packetId
        if size != self.size:
            print "*** Error in component control packet id: ", size, " vs ", self.size
            


class shortComponentControl():
    def __init__(self):
        
        self.format = "BBHHBBff"

        self.packetId = 5
        self.size = 16
        self.componentId = 0
        self.instanceId = 0
        self.componentClass = 0
        self.componentState = 0
        self.componentData1 = 0
        self.componentData2 = 0
   
    def set(self, iid = "NA",cclass = "NA",cid = "NA",state = "NA",data1 = "NA",data2 = "NA",data3 = "NA",data4 = "NA",data5 = "NA",data6 = "NA"):
        if iid != "NA":
            self.instanceId = iid
        if cclass != "NA":
            self.componentClass = cclass
        if  cid != "NA":
            self.componentId = cid
        if  state != "NA":
            self.componentState = state
        if  data1 != "NA":
            self.componentData1 = data1
        if  data2 != "NA":
            self.componentData2 = data2
   
    def pack(self):
        if struct.calcsize(self.format) != self.size:
            print "*** Error in short component control packet format: ", struct.calcsize(self.format), " vs ", self.size

        return struct.pack(self.format,
            # rivi 1
            self.packetId, self.size, self.componentId,
            # rivi 2
            self.instanceId, self.componentClass, self.componentState,
            # loput
            self.componentData1, 
            self.componentData2)
                
    def unpack(self, data):
        packetId = 0
        size = 0

        # rivi 1
        (packetId, size, self.componentId,
        # rivi 2
        self.instanceId, self.componentClass, self.componentState,
        # loput
        self.componentData1, 
        self.componentData2) = struct.unpack(self.format, data)

        #print struct.unpack(self.format, data)

        if packetId != self.packetId:
            print "*** Error in short component control packet packet id: ", packetId, " vs ", self.packetId
        if size != self.size:
            print "*** Error in short component control packet id: ", size, " vs ", self.size
            
            
class celestialSphereControl():
    def __init__(self):
        self.format = "BBBBBBBBIf"

        self.packetId = 9
        self.size = 16
        
        self.hour = 0
        self.minute = 0
        self.ephemerisModeEnable = 0
        self.sunEnable = 0
        self.moonEnable = 0
        self.starFieldEnable = 0
        self.dateTimeValid = 0
        self.date = 0
        self.starFieldIntensity = 0
        

    def pack(self):
        if struct.calcsize(self.format) != self.size:
            print "*** Error in celestial sphere control control packet format: ", struct.calcsize(self.format), " vs ", self.size

          
        return struct.pack(self.format,
            # rivi 1
            self.packetId, self.size, self.hour, self.minute,
            # rivi 2
            (self.ephemerisModeEnable & 0x01) | ((self.sunEnable & 0x01) << 1) | ((self.moonEnable & 0x01) << 2) | ((self.starFieldEnable & 0x01) << 3) | ((self.dateTimeValid & 0x01) << 4),0,0,0,
            # loput
            self.date,
            self.starFieldIntensity)

class terrestialSurfaceConditionControl():
    def __init__(self):
        self.format = "BBHHBB"

        self.packetId = 15
        self.size = 8
        
        self.entityId = 0
        self.surfaceConditionId = 0
        self.severity = 0
        self.surfaceConditionEnable = 0
        self.scope = 0
        self.coverage =  0
        
    def pack(self):
        if struct.calcsize(self.format) != self.size:
            print "*** Error in terrestialSurfaceConditionControl control packet format: ", struct.calcsize(self.format), " vs ", self.size

        return struct.pack(self.format,
            # rivi 1
            self.packetId, self.size, self.entityId,
            # rivi 2
            self.surfaceConditionId, (self.surfaceConditionEnable & 0x01) | ((self.scope & 0x03) << 1) | ((self.severity & 0x1f) << 3), self.coverage)

class timeControl():
    def __init__(self):
        self.format = "BBHI"

        self.packetId = 239
        self.size = 8
        
        self.fractions = 0
        self.time = 0
    

    def pack(self):
        if struct.calcsize(self.format) != self.size:
            print "*** Error in timeControl control packet format: ", struct.calcsize(self.format), " vs ", self.size

        return struct.pack(self.format,
            self.packetId, self.size, self.fractions, self.time)


class sunNotification():
    def __init__(self):
        self.format = "BBHfff"

        self.packetId = 240
        self.size = 16
        
        self.azimuth = 0
        self.elevation = 0
                        
    def pack(self):
    
        if struct.calcsize(self.format) != self.size:
            print "*** Error in sunNotification packet format: ", struct.calcsize(self.format), " vs ", self.size

        return struct.pack(self.format,
            # rivi 1
            self.packetId, self.size, 0,
            # loput
            self.azimuth,
            self.elevation, 0 )
    
    def unpack(self, data):
        packetId = 0
        size = 0
        reserved = 0

        # rivi 1
        (packetId, size, reserved,
        # loput
        self.azimuth,
        self.elevation,
        reserved) = struct.unpack(self.format, data)
        
        #print struct.unpack(self.format, data)

        if packetId != self.packetId:
            print "*** Error in sunNotification packet packet id: ", packetId, " vs ", self.packetId
        if size != self.size:
            print "*** Error in sunNotification packet id: ", size, " vs ", self.size


             
# ----------------------------------------------------------------------            
# Function will search given packet id data from the given data dump
#
# Input parameters:
#   data: data dump (may include several packets)
#   id: packet id to be searched
#
# Output:
#   If found, data of the found packet id
#   If not found, 0
# ----------------------------------------------------------------------
            
def analyse_data(data, id, converted = 0):
    id_found = 0
    ret_data = ""
    
    
    # Convert data to text
    if not converted:
        text = ""
        for i in range(len(data)):
            text += str(ord(data[i])) + " "
    else:
        text = data

    #print "ANALYSER: received text is " + text
        
    # Split the text
    splitted = text.split()

    # - Too short packet ? -
    if len(splitted) < 2 :
        return 0, 0

    data_id = int(splitted[0])
    data_length = int(splitted[1])
    
    # - Too short packet ? -
    if len(splitted) < data_length:
        print "WARNING: invalid lenght in Visu return value " + text
        return 0, 0
    
    # Is the first packet the searched one?    
    if data_id == id:
        id_found = 1
        first_packet_data = ""
        for i in range(len(splitted[:data_length])):
            first_packet_data += chr(int(splitted[:data_length][i]))
        ret_data = first_packet_data
        return id_found, ret_data        
    
    # Are there more packets ?
    elif len(splitted) > data_length:
        s = " "
        remaining = s.join(splitted[data_length:])
        id_found, ret_data = analyse_data(remaining,id,1)
        return id_found, ret_data
        
    else:
        return 0, 0
        
    
    
            
    
    
    
    
    
    
    
    
    
    
    
