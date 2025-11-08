# SSH_tool

SSH tool to run command(s) against server(s)

## usage

`python3 SSHtool.py --server server1 --command ifconfig`  

`python3 SSHtool.py --servers servers.txt --commands --commands.txt`   

servers.txt  
  
```
server1  
server2
```

commands.txt  

```
hostname  
ifconfig -a  
lspci
```

to specify a path for the output:    
`python3 SSHtool.py --server server1 --command ifconfig --output /var/log/server_output.log`  
to specify a higher number of concurrent connections:  
`python3 SSHtool.py --server server1 --command ifconfig  --concurrency 20`

## notes

default output file SSH_tool.log placed in current working directory  
while running commands on multiple servers, the commands are executed concurrently via the multiprocessing module  
default concurrent connections: 5  



