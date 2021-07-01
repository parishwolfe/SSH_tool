##################################
#     SSH Tool                   #
#     open source                #
##################################

#import Statements
try:
    import netmiko
except ModuleNotFoundError:
    import sys
    import subprocess

    def install(package):
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    install("netmiko")

#Documentation for the netmiko module can be found at https://ktbyers.github.io/netmiko/docs/netmiko/index.html#
import sys
import os
import argparse
parser = argparse.ArgumentParser(description="run ssh commands against servers")
parser.add_argument("-c", "--command", help="command to run against server(s)")
parser.add_argument("-C", "--commands", help="line feed delimited list of commands to run against server(s)")
parser.add_argument("-s", "--server", help="single server to run command(s) against")
parser.add_argument("-L", "--server-list", help="line feed delmited list of servers to run command(s) against")
parser.add_argument("-o", "--output", help=)


try:
    import secrets
    username = secrets.username
    password = secrets.password
except ImportError as e:
    username = input("Input User Name ")
    from getpass import getpass
    password = getpass()
    if device["password"] == '':
        print("password is blank, ensure the window has focus before pasting\n")
        device["password"] = getpass()






#Data Structures
filename = input("provide a name for the output text file: ")
#Create file to be appended
try:
    open(f'{filename}.txt', 'x')
except Exception:
    print(f'{filename}.txt already exists. \n')
    filename = input("Please enter a different name: ")

device = {
    "device_type" : "autodetect",
    "ip" : input("Input Server Name: "),
    "username" : username,
    "password" : password
}




#global functions
def send_command(command):
    '''Send a command to the device'''
    global client
    print(f"Command sent: {command}")
    output = client.send_command(command)
    print(output)
    append_file(command, output)
    return output

def send_command_w_timeout(command, delay_factor=1, max_loops=150):
    '''Send a command to the device with a timeout included'''
    global client
    print(f"Command sent: {command} with timeout   {delay_factor * max_loops}")
    output = client.send_command_timing(command, delay_factor, max_loops)
    print(output)
    append_file(command, output)
    return output

def append_file(command, output):
    '''Append the command and output to the named file'''
    with open(f'{filename}.txt', 'a') as file:
        file.write(f'Command sent: {command} \n')
        file.write(output + "\n")
        print("file write")
    return

#Open SSH Connection
client = netmiko.ConnectHandler(**device)
print("Starting SSH Connection")
# **device enters all entries of dictonary   device  as keyword arguments to netmiko.ConnectHandler
# another connection could be created by making a device2 dictionary then client2 = netmiko.ConnectHandler(**device2)
# This would requrie new functions, or the functions could be put into a class along with the connection setup in its __init__

#Detect and print device type then show prompt for debugging
#detect = netmiko.SSHDetect(**device)
#best_match = detect.autodetect()
#print(best_match)
#print(client.find_prompt())


#Sending Commands
send_command_w_timeout('hostname', 1, 50)
send_command('ifconfig -a')

#Close SSH Connection
client.disconnect()
input("Connection closed\nPress enter key to exit")


