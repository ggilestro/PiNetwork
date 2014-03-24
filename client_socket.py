import urllib.request as urllib
import sys, time, subprocess, paramiko

def piDiscover(port):
        
    rpiList = []
    for i in range(1,255):
        url = "http://192.168.0."+str(i)
        #print(url+port)
        try:
            req = urllib.Request(url=url+':'+str(port), data=b"Pi from Polygonal?",method='PIDISCOVER')
            f = urllib.urlopen(req,timeout = 0.05)
            message = f.read()
            #print(message)
            password = b'yes'
            if (message == password):
                rpiList.append(url)
                print ('[%s]' % ', '.join(map(str, rpiList)))
        except:
            pass
            #print("No this one")
            
        #print percentage complete
        sys.stdout.write( "scaning..."+str(int(i/255*100)) + '%\r'),
    print("Ended")
    return rpiList

def askPiId(device, port):
    req = urllib.Request(url='http://'+device+':'+str(port),method='PIID')
    f = urllib.urlopen(req,timeout = 1)
    piId=f.read()
    return piId

def startMplayer():
     p=subprocess.Popen('nc -l -p 5001 | mplayer -fps 30 -cache 1024 -', shell=True, stdout=subprocess.PIPE).pid


def startVideo(deviceIP,port):
    print (deviceIP)
    print (port)
    req = urllib.Request(url='http://'+deviceIP+':'+str(port),data=b'{"cameraOn":"True"}', method='VIDEO')
    f = urllib.urlopen(req,timeout = 2)

    
def stopVideo(deviceIP,port):
    print (deviceIP)
    print (port)
    req = urllib.Request(url='http://'+deviceIP+':'+str(port),data=b'{"cameraOn":"False"}', method='VIDEO')
    f = urllib.urlopen(req,timeout = 2)
    
def openingListeningSocket(deviceIP,port):
    import socket
    import subprocess

    # Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
    # all interfaces)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setblocking(0)
    server_socket.settimeout(10)
    server_socket.bind(('', 5023))
    server_socket.listen(1)
    # Accept a single connection and make a file-like object out of it
    connection = server_socket.accept()[0].makefile('rb')
    try:
        # Run a viewer with an appropriate command line. Uncomment the mplayer
        # version if you would prefer to use mplayer instead of VLC
        #cmdline = ['vlc', '--demux', 'h264', '-']
        cmdline = ['mplayer', '-fps', '30', '-cache', '1024', '-']
        player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
        while True:
            # Repeatedly read 1k of data from the connection and write it to
            # the media player's stdin
            data = connection.read(1024)
#            if not data:
#                print("no data")
#                break
            player.stdin.write(data)
    finally:
        connection.close()
        server_socket.close()
        player.terminate()

def openSSHConnection(device, deviceIp, port):
    print(device)
    print(deviceIp)
    
    ####ATención para este proceso cuando se pare el video!!!
    try:
        p=subprocess.Popen('nc -l -p 5002 | mplayer -fps 30 -cache 1024 -', shell=True).pid

        #req = urllib.Request(url='http://'+device+':'+str(port),method='VIDEO')
        #f = urllib.urlopen(req,timeout = 1)
        #piId=f.read()
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('192.168.0.9', username='root', password='root')
        print("executing command")
        stdin, stdout, stderr = ssh.exec_command("/opt/vc/bin/raspivid -t 999999 -o - | nc {} {}".format('192.168.0.3',5002))
        data = stdout.read()
        error = stderr.read()
        print (data)
        print (error)

      
    
    except KeybpardInterrupt:
        pass

    


    
def main():
    deviceList = ['192.168.0.9']
    port = 7855
    
    while True:
        try:
            print("Select one option:")
            print("1. Scan Network")
            print("2. Access to a SM/SD")
            option = input()
            if option == '1':
                deviceList = piDiscover(port)
                print(deviceList)
            if option == '2':
                print("Select SM/SD")
                
                if not deviceList:
                    print("Error:Do you scan the network?")
                    time.sleep(0.5)
                else:
                    i = 0
                    piIdList = []
                    print("Select a device")
                    for device in deviceList:
                        piId = askPiId(device, port)
                        piIdList.append(piId)
                        print(piId)
                        print("{}: {}".format(i,piId))
                        i += 1
                    deviceSelected =int( input())
                    #startMplayer()
                    #openSSHConnection(deviceSelected,deviceList[deviceSelected],port)  
                    startVideo(deviceList[deviceSelected],port)
                    openingListeningSocket(deviceList[deviceSelected],port)
                    print("q to quit")
                    stop = input()
                    if stop == 'q':
                        stopVideo(deviceList[deviceSelected],port)

                    
        except (KeyboardInterrupt):
            print("closing program...")
            
            time.sleep(0.5)
            break
            

if __name__ == "__main__":
    main()