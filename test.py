with open("servers.txt") as f:
    

    print([x.strip() for x in f.readlines()])