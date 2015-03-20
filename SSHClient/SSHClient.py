import paramiko
import time
import re


account=raw_input("Account:")
passwd=raw_input("Password:")

#Connect SSH server
ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("140.118.172.121",22,account,passwd)

def SendCMD():
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
    '''
    sftp=paramiko.SFTPClient.from_transport(ssh)
    remotepath='/home/m10207432/upload.txt'
    localpath='/upload.txt'
    sftp.put(localpath,remotepath)
    ssh.close()
    '''
    SendCMD()
    
if __name__=="__main__":
    main()
