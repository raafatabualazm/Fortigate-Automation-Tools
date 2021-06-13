import paramiko
import time
import os
from art import *
def add_sites_to_custom_category(ssh):
    os.system('clear')
    banner = text2art("Fortigate Automation Tools v1.0\n by Raafat Abualazm")
    print(banner)
    sites_list = input("Enter webbsite list path: ")
    try:
        sites = open(sites_list)
    except:
        print("Error opening the website list file. Please make sure it exists and has proper permissions.")
    cat_id = input("Enter category ID: ")
    cnt = 1
    for site in sites:
        stdin, stdout, stderr = ssh.exec_command('config webfilter ftgd-local-rating\nedit "{}"\nset rating {}\nnext'.format(site.strip(), cat_id))
        opt = stdout.readlines()
        opt = "".join(opt)
        print(cnt)
        print(opt)
        cnt +=1
        #time.sleep(1)
        sites.close()

def make_a_custom_category(ssh):
    os.system('clear')
    banner = text2art("Fortigate Automation Tools v1.0\n by Raafat Abualazm")
    print(banner)
    cat_name = input("Enter category name: ")
    cat_id = input("Enter category ID: ")
    stdin, stdout, stderr = ssh.exec_command('config webfilter ftgd-local-cat\nedit "{}"\nset id {}\nnext'.format(cat_name, cat_id))
    opt = stdout.readlines()
    opt = "".join(opt)
    print(opt)
    os.system('pause')



banner = text2art("Fortigate Automation Tools v1.0\n by Raafat Abualazm")
print(banner)
ip = input("Fortigate IP: ")
port1 = int(input("SSH Port: "))
username1 = input("Fortigate Username: ")
password1 = input("Fortigate Password: ")

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,username=username1,password=password1,port=port1)
    os.system('clear')
    print(banner)
    print("1- Create a custom category")
    print("2- Add websites to custom category")
    print("3- Exit")
    choice = input("Enter your choice: ")
    if choice.strip() == "1" or choice.strip() == "1-" or choice.strip().lower() == "create a custom category":
        make_a_custom_category(ssh)
    elif  choice.strip() == "2" or choice.strip() == "2-" or choice.strip().lower() == "add websites to custom category":
        add_sites_to_custom_category(ssh)
    os.system('clear')
    print(banner)
    print("Thank you. Have a nice day/evening!")
    
except:
    print("Error initiating SSH coonection. Please re-reun the script and try again and make sure that you typed the IP, port and credentials correctly.")
    


