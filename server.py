import sys
import http.server
import subprocess


class HandlerClass (http.server.BaseHTTPRequestHandler):
    
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
    
    def do_PIDISCOVER(self):
        try:
            self.send_response(200)
            self.end_headers()
            dataLen = int(self.headers['content-length'])
            data = self.rfile.read(dataLen)
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
            
    def do_PIID(self):
        self.do_HEAD()
        f = open('/etc/machine-id','r')
        piId = f.read().rstrip()
        print(piId)
        self.wfile.write(bytes(piId,'UTF-8'))

            
ServerClass = http.server.HTTPServer
Protocol = "HTTP/1.0"

port = 7855

server_address = ('', port)

HandlerClass.protocol_version = Protocol
httpd = ServerClass(server_address, HandlerClass)


httpd.serve_forever()