import paramiko
import time

def main():
    #Connect SSH server
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("140.118.172.121",22,"m10207432","m10207432")

    chan=ssh.invoke_shell()
    print chan.recv(1024)
    
    #Command Script
    try:
        while True:
            
            cmd=raw_input("Command:")
            chan.send(cmd+'\n')
            
            time.sleep(1)
            
            result=chan.recv(9999)
            
            print result
            
            #print stderr.readlines()
    except:
        ssh.close()
    
if __name__=="__main__":
    main()
