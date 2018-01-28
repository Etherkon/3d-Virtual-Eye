# Include Tornado libs
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

# Library methods by Insta
import cigi_support_methods as host

# Our Websocket-to-CIGI routing
import wsmapper as wsmap
from wsmapper import WSMapper

# IndexHandler could render static html -pages. 
# -- Not actually used in this app
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        print("Rendering index")
        self.render('static/index.html')

# Derives Tornado s websocket handler
# This is responsible for handling all websocket requests
class WSMainHandler( tornado.websocket.WebSocketHandler ):
    # Allow older version of Websockets implementation to be used
    # Mainly for Safari
    def allow_draft76(self):
        print "Allow draft76"
        return True
    
    # New connections are initialized here
    def open(self):
        # Create instance of our routing class
        self.mapper = WSMapper(self)
        # Save this connection for later use
        wsmap.connections.append(self)

        # Mapping string to method name like function pointers in C
        # Correct OO way would be make this a class variable or some
        # other way because now we recreate this for every connection
        self.functions = {
            "position" : self.mapper.setposition,
            "camera"   : self.mapper.setcamera,
            "weather"  : self.mapper.setweather,
            "move"     : self.mapper.movecamera,
            "create"   : self.mapper.createmarker,
            "clicked"    : self.mapper.clicked,
            "time"     : WSMapper.settime,
            "image_size" : WSMapper.setimagesize,
            "foo"      : WSMainHandler.fooprinter,
            "error"    : WSMainHandler.clienterror,
            "multicreate" : self.mapper.multicreatemarkers
            }

        # Connection established.
        # Note: New connection is created everytime the page creating
        # connection is (re)loaded so, websockets don t live across
        # multiple pages without using sessions or Web Storage
        print( "New Connection" )

    # on_message is called whenever a message is received
    def on_message( self, message ):
        print( "Message received " + message )
        # Split into array
        commands = message.split()
        #Remove and evaluate first argument of the message
        self.functions.get(commands.pop(0))(commands)
        # Note: We REMOVED the first parameter of the command
        # We should also use:
        # if commands[0] in functions:
        # to make sure we don t crash when unknown command is given 

    # This is called everytime a Websocket connection is lost due 
    # disconnect or timeout or similar thing
    def on_close(self):
        # Remove this connection from the list
        wsmap.connections.remove(self)
        print( "Connection closed" )

    # Just for testing
    @classmethod
    def fooprinter( cls, params ):
        print params

    # Common error testing
    @classmethod
    def clienterror(cls, params ):
        print params

# Note: We need new socket connection for each page. New instance of handler
# is created for each
application = tornado.web.Application([    
    (r'/wsmain', WSMainHandler ),
    # These could be used for providing static files. Note: These don t work
    # as-is but should work with little configuring and testing
#    (r'/images/(.png)', tornado.web.StaticFileHandler, {"path": "images"}),
#    (r'/js/', tornado.web.StaticFileHandler, {"path": "js"}),
    # We could provide other handlers. Note: Tornado uses first handler it
    # can match, so the more general handlers should go to end of list
#    (r'/', IndexHandler ),
# Change this to False for production code. When debug=True, the server
# can be stopped using ctrl-C and it could restart itself whenever some
# module is changed. In this case the latter feature didn t work as it 
# should ve but could work in some other case.
], debug=True)

# Run is module is the main module
if __name__ == "__main__":
    # Set upp HTTP server
    http_server = tornado.httpserver.HTTPServer(application)
    # Listen for port 8888 - Default address=  emtpy string
    http_server.listen(8888)

    # Connect to CIGI
    host.create_cigi()

    # Set up defaults
    host.set_default_situation()

    # Try to start app new instance of the server
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print( "Got ^C, closing server" )

    print( "Shutting down" )
    # Cleanup
    host.UDPSock.close()
