# coding: utf-8

import pprint
import subprocess
import binascii
import sys
import PyMySQL as mdb


try:    
    # Module for output coloring
    from colorama import init, deinit, Fore, Style

except ImportError:
    print(Fore.RED + Style.BRIGHT + "\n* Module colorama needs to be installed on your system.")
    print("Download it from: https://pypi.python.org/pypi/colorama\n" + Fore.WHITE + Style.BRIGHT)
    sys.exit()


try:
    import matplotlib.pyplot as matp

except ImportError:
    print(Fore.RED + Style.BRIGHT + "\n* Module matplotlib needs to be installed on your system.")
    print("Download it from: https://pypi.python.org/pypi/matplotlib\n" + Fore.WHITE + Style.BRIGHT)
    sys.exit()


try:
    import matplotlib.pyplot as matp

except ImportError:
    print(Fore.RED + Style.BRIGHT + "\n* Module matplotlib needs to be installed on your system.")
    print("Download it from: https://pypi.python.org/pypi/matplotlib\n" + Fore.WHITE + Style.BRIGHT)
    sys.exit()


try:    
    import networkx as nx

except ImportError:
    print(Fore.RED + Style.BRIGHT + "\n* Module networkx needs to be installed on your system.")
    print("Download it from: https://pypi.python.org/pypi/networkx")
    print("You should also install decorator: https://pypi.python.org/pypi/decorator\n" + Fore.WHITE + Style.BRIGHT)
    sys.exit()


try:
    # Module for SNMP
    from pysnmp.entity.rfc3413.oneliner import cmdgen

except ImportError:
    print(Fore.RED + Style.BRIGHT + "\n* Module pysnmp needs to be installed on your system.")
    print("Download it from: https://pypi.python.org/pypi/pysnmp\n" + Fore.WHITE + Style.BRIGHT)
    sys.exit()


# Initialize colorama
init()


# Procedure for configuring Linux scheduler:
# root@kali:/# crontab -l   view scheduled tasks
# root@kali:/# crontab -e   edit scheduler
# Add the following line to run the script every 5 minutes, every hour, every day, every month:
# */5 * * * * /path_to_file/NetMon_SQL_v1.py /path_to_file/NETWORK_IP /path_to_file/SSH_USERPASS.txt /path_to_file/SQL_CONN.txt


# # 1 - Save IP Addresses Into a List


# Read IP addresses from the file
def read_ip_address():
    global ip_list
    while True:
        # Prompt user for the name of the IP file
        ip_file = input("\n Please enter the IP file name: ")
        
        try:
            selected_ip_file = open(ip_file, "r")
            selected_ip_file.seek(0)
            ip_list = selected_ip_file.readlines()
            selected_ip_file.close()
            return ip_list
            break
        except IOError:
            print("\n File %s does not exist! Please make sure the file exist and try again!\n" %ip_file)


# # 2 - Define IP Address Validity Test Function


# Check IP address validity
def check_ip_validity():
    ip_validity_flag = False
    
    while True:
        # Check the octets of the IP addresses
        for ip in ip_list:
            octet = ip.split(".")
            if (len(octet) == 4) and (1 <= int(octet[0]) <= 223) and (int(octet[0]) != 127) and (int(octet[0]) != 169 or int(octet[1]) != 254) and (0 <= int(octet[1]) <= 255 and 0 <= int(octet[2]) <= 255 and 0 <= int(octet[3]) <= 255):
                ip_validity_flag = True
                print("%s is a valid IP address. \n"%ip)
                continue
            else:
                print("\n %s is an INVALID IP address!\n" %ip)
                ip_validity_flag = False
                break
                
        # Evaluate the ip validity flag    
        if ip_validity_flag == False:
            print("\n *Please check the IP file and try again! \n")
            break
        elif ip_validity_flag == True:
            print(Fore.GREEN + Style.BRIGHT + "\n *All IP addresses are valid. Checking IP reachability...\n \n")
            break


# # 3 - Define IP Reachability Test Function


# Check IP reachability
def check_ip_reachability():
    ip_reachability_flag = False

    while True:
        for ip in ip_list:
#        ping_reply = subprocess.call(['ping', '-c', '3', '-w', '3', '-q', '-n', ip], stdout = subprocess.PIPE)
            ping_reply = subprocess.call(['ping', '-c', '3', '-w', '3', '-q', '-n', ip])
            if ping_reply == 0:
                print(Fore.GREEN + Style.BRIGHT + "%s is reachable.\n" %ip)
#                print(Fore.GREEN + Style.BRIGHT + "This may take a few moments...\n")
                ip_reachability_flag = True
                continue
            elif ping_reply == 2:
                print(Fore.RED + Style.BRIGHT + "\n No response from %s." %ip)
                ip_reachability_flag = False
                break
            else:
                print(Fore.RED + Style.BRIGHT + "\n Ping to %s has failed." %ip)
                ip_reachability_flag = False
                continue

        #Evaluate the ip reachability flag 
        if ip_reachability_flag == False:
            print("\n *Please re-check the IP address list/device(s).\n \n")
            break
        
        elif ip_reachability_flag == True:
            print("\n *All devices are reachable.\n \n")
            break


# SNMP Community String RO
# Prompt user for input
try:
    print(Style.BRIGHT + "\n######################## Traffic Engineering Tool ########################")
    print("Make sure to connect to all the devices!")
    print("SNMP community string should be the same on all devices running OSPF!\n")
    comm = input("\n Please enter community string: ")
    
except KeyboardInterrupt:
    print(Fore.RED + Style.BRIGHT + "\n\n Program aborted by user. Exiting...\n")
    sys.exit()
    
try:
    # Call read IP function    
    read_ip_address()
    
except KeyboardInterrupt:
    print("\n\n* Program aborted by user. Exiting...\n")
    sys.exit()

try:
    #Call IP validity function    
    check_ip_validity()
    
except KeyboardInterrupt:
    print("\n\n* Program aborted by user. Exiting...\n")
    sys.exit()
    
try:
    #Call IP reachability function
    check_ip_reachability()
    
except KeyboardInterrupt:
    print("\n\n* Program aborted by user. Exiting...\n")
    sys.exit()