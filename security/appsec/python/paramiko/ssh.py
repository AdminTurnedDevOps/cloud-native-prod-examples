import paramiko
import sys

def ssh_command(ip, port, user, passwd, cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"Connecting to {ip}:{port}...")
        client.connect(
            hostname=ip, 
            port=port, 
            username=user, 
            password=passwd,
            timeout=30,  # Longer timeout
            allow_agent=False,  # Don't use SSH agent
            look_for_keys=False  # Don't look for SSH keys
        )
        
        _, stdout, stderr = client.exec_command(cmd)
        output = stdout.readlines() + stderr.readlines()
        if output:
            print('--- Output ---')
            for line in output:
                print(line.strip())
        client.close()
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    import getpass
    # user = getpass.getuser()
    user = input('Username: ')
    password = getpass.getpass()

    ip = input('Enter server IP: ')
    port = input('Enter port or <CR>: ')
    port = 22 if port == '' else int(port)
    cmd = input('Enter command or <CR>: ')
    ssh_command(ip, port, user, password, cmd)