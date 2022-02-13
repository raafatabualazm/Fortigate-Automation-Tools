import socket
import paramiko 
import os
from art import *
from getpass import getpass
import csv

# names = socket.gethostbyaddr('10.0.0.0')
# print(names)
banner = text2art("Fortigate Automation Tools v1.0\n by Raafat Abualazm")
print(banner)
ip = input("Fortigate IP: ")
port1 = int(input("SSH Port: "))
username1 = input("Fortigate Username: ")
password1 = getpass(prompt="Fortigate Password: ")
cmd = '''
config firewall address\n
edit \"{0}\"
set type ipmask\n
set associated-interface ToPAN\n
set subnet {1}\n
next
end
'''
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,username=username1,password=password1,port=port1)
    os.system('clear')
    print(banner)
    address_file = input("Enter Path to address objects file: ")
    with open(address_file, 'r') as file:
        reader = csv.reader(file)
        addr_lst = list(reader)
        for idx in range(1, len(addr_lst)):
            print(addr_lst[idx][0] + " " + addr_lst[idx][3])
            print(addr_lst[idx][3][-3])
            if addr_lst[idx][3][-3] != '/' and addr_lst[idx][3][-2] != '/':
                addr_lst[idx][3] =  addr_lst[idx][3] + "/32"
            print(addr_lst[idx][3])
            try:
                names = socket.gethostbyaddr(addr_lst[idx][0])
                print(names[0])
                stdin,stdout,stderr = ssh.exec_command(cmd.format(names[0], addr_lst[idx][3]))
                for line in iter(stdout.readline,""): 
                    print(line)
            except:
                stdin,stdout,stderr = ssh.exec_command(cmd.format(addr_lst[idx][0], addr_lst[idx][3]))
                for line in iter(stdout.readline,""): 
                    print(line)

except:
    print("Error initiating SSH coonection. Please re-reun the script and try again and make sure that you typed the IP, port and credentials correctly.")
