import sys
import http.server
import subprocess
import picamera
import socket
import time
import json


class HandlerClass (http.server.BaseHTTPRequestHandler):
    
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
   ### Custom autodiscover protocol: expects a question and gives and answer. 
    def do_PIDISCOVER(self):
        try:
            self.do_HEAD()
            data = self.readData(self)
            print(str(data))
            print("getting something")
            expected = b'Pi from Polygonal?'
            if (data == expected):
                self.wfile.write(b'yes')
                print(data)
        except ValueError:
            print("error")
        except IOError as e:
            print (e)
        except:
            print("error", sys.exc_info()[0])
    
    
    ##Gets the machine-id and send it to the master
    def do_PIID(self):
        self.do_HEAD()
        #try:
        f = open('/etc/machine-id','r')
        piId = f.read().rstrip()
        print(piId)
        self.wfile.write(bytes(piId,'UTF-8'))
        #except ValueError:
         #   print("error")
        #except IOError as e:
         #   print (e)
        #except:
         #   print("error", sys.exc_info()[0])
    
    ##receives the master address and the port to open the socket, also if the "cameraON" is false, it closes the socket.
    def do_VIDEO(self):
        print("VIDEO")
        self.do_HEAD()
        rawData = self.readData()
        decodeData = rawData.decode('UTF-8')
        print (rawData)
        data = json.loads(decodeData)
        print (data)
        self.cameraSocket(data)
            
        
    def readData(self):
        dataLen = int(self.headers['content-length'])
        data = self.rfile.read(dataLen)
        return data
    
    
    def cameraSocket(self,data):
        # Connect a client socket to my_server:8000 (change my_server to the
        # hostname of your server)
        time.sleep(2)
        client_socket = socket.socket()
        client_socket.connect(('192.168.0.3', 5023))
        print("waiting")
        # Make a file-like object out of the connection
        connection = client_socket.makefile('wb')
        print("connected")
        try:
            camera = picamera.PiCamera()
        except:
            print ("camera exists")
        
        if data["cameraOn"] == 'True':
            try:
                print("starting camera")
                camera.resolution = (1296, 972)
                # Start a preview and let the camera warm up for 2 seconds
                camera.start_preview()
                time.sleep(2)
                # Start recording, sending the output to the connection for 60
                # seconds, then stop
                camera.start_recording(connection, format='h264')
                    
            except:
                print ("error opening socket")

        elif data["cameraOn"] == 'False':   
            try:
                print("camera off")
                camera.stop_recording()
                camera.stop_preview()
                camera.close()
                connection.close()
                client_socket.close()
            except:
                print ("error closing camera")
            
        
ServerClass = http.server.HTTPServer
Protocol = "HTTP/1.0"

port = 7855

server_address = ('', port)

HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address, HandlerClass)


httpd.serve_forever()