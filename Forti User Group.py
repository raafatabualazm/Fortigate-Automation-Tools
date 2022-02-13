import socket
import paramiko 
import os
from art import *
from getpass import getpass
import csv
from ldap3 import Server, Connection, SAFE_SYNC

banner = text2art("Fortigate Automation Tools v1.0\n by Raafat Abualazm")
print(banner)
ip = input("Fortigate IP: ")
port1 = int(input("SSH Port: "))
username1 = input("Fortigate Username: ")
password1 = getpass(prompt="Fortigate Password: ")
ldapusername = input("LDAP Username: ")
ldappassword = getpass(prompt="LDAP Password: ")
server = Server('Active Directory IP')
conn = Connection(server, ldapusername, ldappassword, client_strategy=SAFE_SYNC, auto_bind=True)

cmd = '''
config user group\n
edit "<Group Name>"\n
append member \"{0}\"\n
next
end
'''
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,username=username1,password=password1,port=port1)
    os.system('clear')
    print(banner)
    members_file = input("Enter Path to user group file: ")
    with open(members_file, 'r') as file:
        reader = csv.reader(file)
        user_group_list = list(reader)
        for idx in range(1, len(user_group_list)):
           for user in user_group_list[idx][2].split(';'):
                status, result, response, _ = conn.search('dc=enppi,dc=com', '(employeeID={0})'.format(user))
                if len(response) == 4:
                    stdin,stdout,stderr = ssh.exec_command(cmd.format(response[0]['dn']))
                    print(user)
                    for line in stdout.readlines():
                        print(line)
       
except:
    print("Error initiating SSH coonection. Please re-reun the script and try again and make sure that you typed the IP, port and credentials correctly.")
