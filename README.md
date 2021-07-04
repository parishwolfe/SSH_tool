# SSH_tool
SSH tool to run command(s) against server(s)

## usage
python3 SSH_tool.py --server server1 --command ifconfig

python3 SSH_tool.py --servers servers.txt --commands --commands.txt

  servers.txt
  server1
  server2
  
  commands.txt
  hostname
  ifconfig -a
  lspci
  
python3 SSH_tool.py --server server1 --command ifconfig --output /var/log/server_output.log

## notes
default output file SSH_tool.log placed in current working directory

while running commands on multiple servers, the commands are executed concurrently via the multiprocessing module

default is 5 concurrent connections, this can be changed with the --concurrency flag
