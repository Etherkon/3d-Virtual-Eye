from socket import *
import cigi_packet_classes
import time

# -------------------------------------------------------------        
# Supporting functions
#
# -------------------------------------------------------------
def create_cigi(): 
    global UDPSock
    global addr_send

    host = "localhost"
    send_port = 8001
    receive_port = 8000
    buf = 10000
    
    addr_send = (host,send_port)
    addr_recv = (host,receive_port)

    # Create socket
    UDPSock = socket(AF_INET,SOCK_DGRAM)

    # Bind receiving socket
    UDPSock.bind(addr_recv)
    
def set_globals():
    global ig
    global ec
    global viewdef
    global viewcontrol
    global sof
    global celestial
    global weather
    global ac
    
    ig = cigi_packet_classes.IGControl()
    ec = cigi_packet_classes.EntityControl()
    viewdef = cigi_packet_classes.ViewDef()
    viewcontrol = cigi_packet_classes.ViewControl()
    sof = cigi_packet_classes.startOfFrame()
    celestial = cigi_packet_classes.celestialSphereControl()
    weather = cigi_packet_classes.weatherControl()
    ac = cigi_packet_classes.atmosphereControl()

def reset_IG():
    # Reset IG
    ig.IGMode = 0
    UDPSock.sendto(ig.pack(),addr_send)
    ig.IGMode = 1
    UDPSock.sendto(ig.pack(),addr_send)

def set_default_situation():
    set_globals()

    reset_IG()
    
    # Create ownship and view control
    print "***  Setting defaults  ****"
    ec.latitude = 63.0
    ec.longitude = 23.0
    ec.altitude = 1000
    ec.entityState = 1
    ec.entityType = 0
    
    # time and date
    celestial.sunEnable = 1
    celestial.moonEnable = 1
    celestial.starFieldEnable = 1
    celestial.dateTimeValid = 1
    celestial.starFieldIntensity = 100
    celestial.date = 4012012 # (M)MDDYYYY without leading zero!
    celestial.hour = 12
        
    # visibility range
    ac.globalVisibilityRange = 200000
    
    # view control
    viewcontrol.pitchEnable = 1
    viewcontrol.pitch = 0
    viewcontrol.yawEnable = 1
    viewcontrol.yaw = 0
    viewcontrol.rollEnable = 1
    viewcontrol.roll = 0
    viewcontrol.zOffsetEnable = 1
    viewcontrol.zOffset = 0
    viewcontrol.xOffsetEnable = 1
    viewcontrol.xOffset = 0
    viewcontrol.yOffsetEnable = 1
    viewcontrol.yOffset = 0

    # viewdef
    """
    viewdef.leftEnable = 1
    viewdef.left = -73.0/2.0
    viewdef.rightEnable = 1
    viewdef.right = 73.0/2.0
    viewdef.topEnable = 1
    viewdef.top = 59.0/2.0
    viewdef.bottomEnable = 1
    viewdef.bottom = -59.0/2.0
    """
    #UDPSock.sendto(ig.pack()+viewdef.pack(),addr_send)        
    set_fov(75)
 

    # clear weather
    weather.layerId = 0
    weather.weatherEnable = 0
    UDPSock.sendto(ig.pack() + weather.pack(),addr_send)
    weather.layerId = 1
    weather.weatherEnable = 0
    UDPSock.sendto(ig.pack() + weather.pack(),addr_send)
    weather.layerId = 2
    weather.weatherEnable = 0
    UDPSock.sendto(ig.pack() + weather.pack(),addr_send)
    weather.layerId = 3
    weather.weatherEnable = 0
    UDPSock.sendto(ig.pack() + weather.pack(),addr_send)
    weather.layerId = 4
    weather.weatherEnable = 0
    UDPSock.sendto(ig.pack() + weather.pack(),addr_send)
    weather.layerId = 5
    weather.weatherEnable = 0
    UDPSock.sendto(ig.pack() + weather.pack(),addr_send)
        
    data = ig.pack() + ec.pack() + viewdef.pack() + viewcontrol.pack() + celestial.pack() + weather.pack() + ac.pack()
    UDPSock.sendto(data,addr_send)
    sleep(120)
    
def wait_sync():
    while 1:
        data,addr_recv = UDPSock.recvfrom(10000)
        ret, ret_data = cigi_packet_classes.analyse_data(data,101)
        if ret:
            sof.unpack(ret_data)
            if sof.lastHostFrameNumber == ig.hostFrameNumber:
                ig.lastIGFrameNumber = sof.IGFrameNumber
                ig.timestamp = sof.timestamp
            break
    return data

def sleep(frames):
    frame_time = 1.0 / 60.0
    for i in range(frames):
        ig.hostFrameNumber += 1
        UDPSock.sendto(ig.pack(),addr_send)
        wait_sync()
       
def set_wind(speed,direction=0):
    ac.globalHorizontalWindSpeed = speed
    ac.globalWindDirection = direction
    UDPSock.sendto(ig.pack()+ac.pack(),addr_send)
	
def set_humidity(humidity):
	ac.globalHumidity = humidity
	UDPSock.sendto(ig.pack()+ac.pack(),addr_send)
	
def set_temperature(temp):
	ac.globalAirTemperature = temp
	UDPSock.sendto(ig.pack()+ac.pack(),addr_send)
    
def set_date(date):
    txt = date.split(".")
    celestial.dateTimeValid = 1
    celestial.date = int(txt[1] + str(txt[0].zfill(2)) + txt[2])
    UDPSock.sendto(ig.pack()+ celestial.pack(),addr_send)
        
def set_time(time):
    txt = time.split(":")
    celestial.dateTimeValid = 1
    celestial.hour = int(txt[0])
    celestial.minute = int(txt[1])
    UDPSock.sendto(ig.pack()+ celestial.pack(),addr_send)

def set_lights(state):
    cc = cigi_packet_classes.componentControl()
    cc.set(0,8,10,0,state)
    UDPSock.sendto(ig.pack()+cc.pack(),addr_send)

def set_sky(object,state=1):
    
    if object.lower() == "sun" :
        celestial.sunEnable = state
    if object.lower() == "moon" :
        celestial.moonEnable = state
    if object.lower() == "stars" or object.lower() == "starfield":
        celestial.starFieldEnable = state
        celestial.starFieldIntensity = 100
    
    UDPSock.sendto(ig.pack()+celestial.pack(),addr_send)    

def set_fov(fov):
        
        viewdef.leftEnable = 1
        viewdef.left = -1 * (float(fov))/2.0
        viewdef.rightEnable = 1
        viewdef.right = (float(fov))/2.0
        viewdef.topEnable = 1
        viewdef.top = (float(fov))/2.0
        viewdef.bottomEnable = 1
        viewdef.bottom = -1 * (float(fov))/2.0
        UDPSock.sendto(ig.pack()+viewdef.pack(),addr_send)
        
def set_visibility(visibility):
    ac = cigi_packet_classes.atmosphereControl()
    ac.globalVisibilityRange = float(visibility)
    UDPSock.sendto(ig.pack()+ac.pack(),addr_send)
    
def set_weather(condition):
    if condition.lower() == "clear":
        weather.weatherEnable = 1
        weather.coverage = 0
    elif condition.lower() == "cloudy":
        weather.layerId = 1
        weather.scope = 0
        weather.weatherEnable = 1
        weather.baseElevation = 4500
        weather.transitionBand = 20
        weather.thickness = 0
        weather.coverage = 50
    
    elif condition.lower() == "overcast":
        weather.layerId = 1
        weather.scope = 0
        weather.weatherEnable = 1
        weather.baseElevation = 4500
        weather.transitionBand = 20
        weather.thickness = 0
        weather.coverage = 100
        UDPSock.sendto(ig.pack() + weather.pack(),addr_send)
        
    elif condition.lower() == "reset":
        weather.layerId = 0
        weather.weatherEnable = 0
        UDPSock.sendto(ig.pack() + weather.pack(),addr_send)
        weather.layerId = 1
        weather.weatherEnable = 0
        UDPSock.sendto(ig.pack() + weather.pack(),addr_send)
        weather.layerId = 2
        weather.weatherEnable = 0
        UDPSock.sendto(ig.pack() + weather.pack(),addr_send)
        weather.layerId = 3
        weather.weatherEnable = 0
        UDPSock.sendto(ig.pack() + weather.pack(),addr_send)
        weather.layerId = 4
        weather.weatherEnable = 0
        UDPSock.sendto(ig.pack() + weather.pack(),addr_send)
        weather.layerId = 5
        weather.weatherEnable = 0
        UDPSock.sendto(ig.pack() + weather.pack(),addr_send) 
    
    elif condition.lower() == "groundfog":
        weather.layerId = 0
        weather.scope = 0
        weather.weatherEnable = 1
        weather.transitionBand = 10
        weather.thickness = 122
        weather.coverage = 80
        weather.visibilityRange = 280
        UDPSock.sendto(ig.pack() + weather.pack(),addr_send) 
    
    elif condition.lower() == "scud":
        weather.layerId = 1
        weather.scope = 0
        weather.weatherEnable = 1
        weather.scudEnable = 1
        weather.visibilityRange = 10
        weather.baseElevation = 2500
        weather.coverage = 100
        weather.thickness = 100
        weather.transitionBand = 100
        weather.scudFrequency = 100
        UDPSock.sendto(ig.pack() + weather.pack(),addr_send) 
    elif condition.lower() == "cirrus":
        weather.layerId = 2
        weather.scope = 0
        weather.weatherEnable = 1
        weather.baseElevation = 8500
        weather.transitionBand = 20
        weather.thickness = 50
        weather.coverage = 70
        ec.altitude = 5000
        UDPSock.sendto(ig.pack() + weather.pack(),addr_send)

    elif condition.lower() == "lightning":
        weather.layerId = 1
        weather.scope = 0
        weather.weatherEnable = 1
        weather.randomLightningEnable = 1
        weather.severity = 100
        UDPSock.sendto(ig.pack() + weather.pack(),addr_send)            
    else:
        print "WARNING: unknown weather type: " + condition

# Sets position based on given parameters
def set_position( lat, lng, height=250, pitch=-20, yaw=0, roll=0 ):
    ec.set( lat, lng, height, roll, pitch, yaw )
    UDPSock.sendto(ig.pack()+ec.pack(),addr_send)
    sleep(120)

# Sets current server time for SimCore
def set_currenttime():
    # Get the time
    now = time.localtime()
    print( now )
    # Set CIGI parameters
    celestial.dateTimeValid = 1
    celestial.date = int( str( now.tm_mon ) + str( now.tm_mday ).zfill(2) + str( now.tm_year ))
    celestial.hour = now.tm_hour
    celestial.minute = now.tm_min
    # Tried to light up
    if now.tm_hour > 20 or now.tm_hour < 8:
        print( "Lights ON")
        # Hmm... These are just the tower lights
        set_lights(2)
    # Send CIGI packet
    UDPSock.sendto(ig.pack()+ celestial.pack(),addr_send)    



