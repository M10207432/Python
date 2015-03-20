import paramiko


def main():
    #Connect SSH server
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("140.118.172.121",22,"m10207432","m10207432")

    t=ssh.get_transport()
    chan=t.open_session()
    
    chan.exec_command('bash -s')
    chan.send_ready()
    #Command Script
    try:
        while True:
            cmd=raw_input("Command:")
            chan.send(cmd+'\n')
            
            chan.recv_ready()
            result=chan.recv(1024)
            print result
            
            #print stderr.readlines()
    except:
        ssh.close()
    
if __name__=="__main__":
    main()
