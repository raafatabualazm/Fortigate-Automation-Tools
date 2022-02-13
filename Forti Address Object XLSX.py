import socket
import paramiko 
import os
from art import *
from getpass import getpass
import csv
import pandas
import time
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
set subnet {1}/32\n
next\n
end\n
'''
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,username=username1,password=password1,port=port1)
    os.system('clear')
    print(banner)
    address_file = input("Enter Path to address objects file: ")
    with open(address_file, 'r') as file:
        addr_lst = pandas.read_excel("ENG VMware.xlsx")
        for idx, addr in addr_lst.iterrows():
            stdin,stdout,stderr = ssh.exec_command(cmd.format(addr['Name'], addr['IP Address']))
            time.sleep(1)
            for line in iter(stdout.readline,""): 
                    print(line)

except:
    print("Error initiating SSH coonection. Please re-reun the script and try again and make sure that you typed the IP, port and credentials correctly.")
