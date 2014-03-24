import urllib.request as urllib
import sys, time, subprocess, paramiko
#import Xlib.support.connect as xlib_connect

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
        stdin, stdout, stderr = ssh.exec_command("/opt/vc/bin/raspivid -t 999999 -w 1296 -h 730 -o - | nc {} {}".format('192.168.0.3',5002))
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
                    openSSHConnection(deviceSelected,deviceList[deviceSelected],port)  

                    

                    
        except (KeyboardInterrupt):
            print("closing program...")
            time.sleep(0.5)
            break
            

if __name__ == "__main__":
    main()