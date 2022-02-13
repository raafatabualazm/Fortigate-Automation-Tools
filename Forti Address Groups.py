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
config firewall addrgrp\n
edit \"{0}\"
append member \"{1}\"\n
next
end
'''
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,username=username1,password=password1,port=port1)
    os.system('clear')
    print(banner)
    address_file = input("Enter Path to address groups file: ")
    with open(address_file, 'r') as file:
        reader = csv.reader(file)
        addr_grp_lst = list(reader)
        for idx in range(1, len(addr_grp_lst)):
           for addr in addr_grp_lst[idx][3].split(';'):
                try:
                    names = socket.gethostbyaddr(addr_grp_lst[idx][0])
                    stdin,stdout,stderr = ssh.exec_command(cmd.format(addr_grp_lst[idx][0], names[0]))
                    for line in stdout.readlines():
                        print(line)    
                except:
                    stdin,stdout,stderr = ssh.exec_command(cmd.format(addr_grp_lst[idx][0], addr))
                    for line in stdout.readlines():
                        print(line)

except:
    print("Error initiating SSH coonection. Please re-reun the script and try again and make sure that you typed the IP, port and credentials correctly.")
