import paramiko
import time
import re
import pysftp

'''
account=raw_input("Account:")
passwd=raw_input("Password:")
'''
account='m10207432'
passwd='m10207432'
ip="192.168.29.128"
port = 22

def SendCMD():
    #Connect SSH server
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,port,account,passwd)

    chan=ssh.invoke_shell()
    print chan.recv(9999)
    chan.send('\n')
    time.sleep(1)
    result=chan.recv(9999)
    insidecmd=0
    
    #Command Script
    try:
        while True:
            if insidecmd==0:
                cmd=raw_input("Command:")
            else:
                cmd=raw_input("")
            chan.send(cmd+'\n')
            
            time.sleep(0.1)
            
            result=chan.recv(9999)
            rlist=result.split('\n')
            if len(rlist)>=2:
                rlist.remove(rlist[0])                  #remove first one
                if rlist[len(rlist)-1].find('@')>0:
                    rlist.remove(rlist[len(rlist)-1])   #remove last one
                    insidecmd=0
                else:
                    insidecmd=1
            
            for i in rlist:
                print (re.compile(r'\x1b[^m]*m')).sub('', i)
    except:
        ssh.close()

def main():
    
    Conn_sftp=paramiko.Transport((ip, port))
    Conn_sftp.connect(username=account, password=passwd)

    sftp=paramiko.SFTPClient.from_transport(Conn_sftp)
    remotepath='/home/m10207432/upload1.txt'
    localpath='./upload.txt'
    sftp.put(localpath,remotepath)
    Conn_sftp.close()
    
    #SendCMD()
    
if __name__=="__main__":
    main()
