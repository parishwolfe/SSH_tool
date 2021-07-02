##################################
#     SSH Tool                   #
#     MIT license open source    #
#     author: Parish Wolfe       #
##################################

#global variables
concurrency = 5

#import statements
import sys
try:
    import netmiko
except ModuleNotFoundError:
    import subprocess

    def install(package):
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    install("netmiko")
    #Documentation for the netmiko module can be found at :
    #https://ktbyers.github.io/netmiko/docs/netmiko/index.html
import os
import logging
import multiprocessing
import argparse
parser = argparse.ArgumentParser(description="run ssh commands against servers")
parser.add_argument("-c", "--command", help="command to run against server(s)")
parser.add_argument("-C", "--commands", help="line feed delimited list of commands to run against server(s)")
parser.add_argument("-s", "--server", help="single server to run command(s) against")
parser.add_argument("-L", "--servers", help="line feed delimited list of servers to run command(s) against")
parser.add_argument("-o", "--output", help="file to write output to")
parser.add_argument("-q", "-concurrency", help="set the concurrency, default: 5")
#parser.add_argument("-a", "--amalgamate", help="conbine output into one file")
options = parser.parse_args()

#collect credentials
try:
    import secret
    username = secret.username
    password = secret.password
except ModuleNotFoundError as e:
    username = input("Username: ")
    from getpass import getpass
    password = getpass()
    if password == '':
        print("password is blank, ensure the window has focus before pasting\n")
        password = getpass()

log_file = "SSH_tool.log"
if options.output:
    log_file = str(options.output)
logging.basicConfig(level=logging.INFO, filename=log_file)
try:
    concurrency = int(options.concurrency)
except ValueError as e:
    print("concurrency must be a number")
    exit()
#/import statements

#global functions
def define_targets(*args):
    devices = []
    for dev in list(args):
        devices.append({
        "device_type" : "autodetect",
        "ip" : dev,
        "username" : username,
        "password" : password
        })
    return devices

def append_file(command, output):
    '''Append the command and output to the named file'''
    logging.info(f"command: {command}\noutput: {output}\n")
    return

def process_helper(process_list):
    count = 0
    while len(process_list) > count:
        if count % concurrency == 0 and count!= 0:
            for j in range(concurrency):
                process_list[count-(j+1)].join()
        process_list[count].start()
        count += 1

def operate_on_targets(server, commands): #server string, commands list
    client = netmiko.ConnectHandler(**server)
    host = server.get("ip")
    print(f"Starting SSH Connection to: {host}")
    for command in commands:
        print(f"command sent to {host}; {command}")
        logging.info(f"command sent to {host}; {command}")
        output = client.send_command(command)
        #delay_factor = 1
        #max_loops = 150
        #output = client.send_command_timing(command, delay_factor, max_loops)
        print(f"output received from {host}; {command}\n{output}")
        logging.info(f"output received from {host}; {command}\n{output}")
    client.disconnect()

def main():
    #define targets
    if options.server != None:
        devices = define_targets(options.server)
    elif options.servers != None:
        with open(options.servers) as f:
            devices = define_targets(*[x.strip() for x in f.readlines()])
    else:
        print("you must define a target server")
        exit()

    #define operations
    if options.command != None:
        commands = []
        commands.append(str(options.command))
    elif options.commands != None:
        with open(options.commands) as f:
            commands = [x.strip() for x in f.readlines()]
    else:
        print("you must define an operation")
        exit()

    process_list = []
    for server in devices:
        process_list.append(multiprocessing.Process(target=operate_on_targets, args=(server, commands)))
    process_helper(process_list)

if __name__ == "__main__":
    main()

#cspell:ignore netmiko
