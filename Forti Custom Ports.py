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
cmd_tcp = '''
config firewall service custom\n
edit \"{0}\"
set tcp-portrange {1}-{2}\n
next
end
'''

cmd_udp = '''
config firewall service custom\n
edit \"{0}\"
set udp-portrange {1}-{2}\n
next
end
'''
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,username=username1,password=password1,port=port1)
    os.system('clear')
    print(banner)
    address_file = input("Enter Path to custom ports file: ")
    with open(address_file, 'r') as file:
        reader = csv.reader(file)
        port_lst = list(reader)
        print(len(port_lst))
        for idx in range(1, len(port_lst)):
            if port_lst[idx][2] == 'TCP':
                if '-' in port_lst[idx][3]:
                    port1 =port_lst[idx][3].split('-')[0]
                    port2 = port_lst[idx][3].split('-')[1]
                    print(port1 + ' - ' + port2)
                    stdin,stdout,stderr = ssh.exec_command(cmd_tcp.format(port_lst[idx][0], port1, port2))
                    for line in stdout.readlines():
                        print(line)
                else:
                    port1 = port_lst[idx][3]
                    print(port1)
                    stdin,stdout,stderr = ssh.exec_command(cmd_tcp.format(port_lst[idx][0], port1, port1))
                    for line in stdout.readlines():
                        print(line)
            elif port_lst[idx][2] == 'UDP':
                if '-' in port_lst[idx][3]:
                    port1 = port_lst[idx][3].split('-')[0]
                    port2 = port_lst[idx][3].split('-')[1]
                    print(port1 + ' - ' + port2)
                    stdin,stdout,stderr = ssh.exec_command(cmd_udp.format(port_lst[idx][0], port1, port2))
                    for line in stdout.readlines():
                        print(line)
                else:
                    port1 = port_lst[idx][3]
                    print(port1)
                    stdin,stdout,stderr = ssh.exec_command(cmd_udp.format(port_lst[idx][0], port1, port1))
                    for line in stdout.readlines():
                        print(line)

           

except:
    print("Error initiating SSH coonection. Please re-reun the script and try again and make sure that you typed the IP, port and credentials correctly.")
