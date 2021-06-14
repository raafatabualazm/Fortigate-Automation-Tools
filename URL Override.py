import paramiko
import time
import os
from art import *

def print_out(stdout):
    opt = stdout.readlines()
    opt = "".join(opt)
    print(opt)

def add_url_list_to_profile(ssh):
    cmd_to_add_url_list_to_profile = '''
    config webfilter profile\n
    edit "{}"\n 
        config web\n
            set urlfilter-table {}\n
        end\n
    next\n
    end\n
    '''
    profile_name = input("Profile name: ")
    url_filter_id = input("Profile filter ID: ")
    stdin, stdout, stderr = ssh.exec_command(cmd_to_add_url_list_to_profile.format(profile_name,url_filter_id))
    print_out(stdout)

def add_url_to_filter(ssh):
    cmd_add_to_url_filter = '''
    config webfilter urlfilter\n
        edit {}\n
            set name "{}"\n
            config entries\n
                edit {}\n
                    set url "{}"\n
                    set type {}\n
                    set action {}\n
                next\n
            end\n
        next\n
    end\n
    '''
    sites_list = input("Enter website list path: ")
    try:
        sites = open(sites_list)
        print("Choose a random ID number, preferably big, and make note of it.")
        filter_id = input("Enter filter ID: ")
        filter_name = input("Enter filter name: ")
        idx = 1
        for site in sites:
            components = site.split(',')
            if components[1] == "simple" or components[1] == "regex":
                if components[2] != "":
                    stdin, stdout, stderr = ssh.exec_command(cmd_add_to_url_filter.format(filter_id,filter_name, idx,components[0],components[1],components[2]))
                    print_out(stdout)
                else:
                    stdin, stdout, stderr = ssh.exec_command(cmd_add_to_url_filter.format(filter_id,filter_name, idx,components[0],components[1],"exempt"))
                    print_out(stdout)
            elif components[1] == "wildcard" or components[1] == "":
                if "*" not in components[0]:
                    if components[2] != "":
                        stdin, stdout, stderr = ssh.exec_command(cmd_add_to_url_filter.format(filter_id,filter_name, idx,'*'+components[0]+'*',"wildcard",components[2]))
                        print_out(stdout)
                    else:
                        stdin, stdout, stderr = ssh.exec_command(cmd_add_to_url_filter.format(filter_id,filter_name, idx,'*'+components[0]+'*',"wildcard","exempt"))
                        print_out(stdout)
                else:
                    if components[2] != "":
                        stdin, stdout, stderr = ssh.exec_command(cmd_add_to_url_filter.format(filter_id,filter_name, idx,components[0],"wildcard",components[2]))
                        print_out(stdout)
                    else:
                        stdin, stdout, stderr = ssh.exec_command(cmd_add_to_url_filter.format(filter_id,filter_name, idx,components[0],"wildcard","exempt"))
                        print_out(stdout)
            idx += 1

    except:
        print("Error opening the website list file. Please make sure it exists and has proper permissions.")
    
    


def add_web_profile(ssh):
    cmd_to_add_web_profile = '''
    config webfilter profile\n
    edit "{}"\n
    next\n
    end\n
    '''
    os.system('clear')
    banner = text2art("Fortigate Automation Tools v1.0\n by Raafat Abualazm")
    print(banner)
    profile_name = input("Enter Profile name: ")
    stdin, stdout, stderr = ssh.exec_command(cmd_to_add_web_profile.format(profile_name))
    print_out(stdout)
    time.sleep(1)

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
    print("1- Create a new Web Profile")
    print("2- Add websites to custom URL List")
    print("3- Add a URL list to a Web Profile")
    print("4- Exit")
    choice = input("Enter your choice: ")
    if choice.strip() == "1" or choice.strip() == "1-" or choice.strip().lower() == "create a new web profile":
        add_web_profile(ssh)
    elif choice.strip() == "2" or choice.strip() == "2-" or choice.strip().lower() == "add websites to custom url list":
        add_url_to_filter(ssh)
    elif choice.strip() == "3" or choice.strip() == "3-" or choice.strip().lower() == "add a url list to a web profile":
        add_url_list_to_profile(ssh)

except:
    print("Error initiating SSH coonection. Please re-reun the script and try again and make sure that you typed the IP, port and credentials correctly.")