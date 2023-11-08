from sshtunnel import SSHTunnelForwarder

serverList = [
    {'serverIp': '192.168.1.2',       #vm IP
     'ssh_username': 'username',      #vm username
     'ssh_password': 'password',      #vm password
     'desired_bind_port': 8888},    #should be unique for different vm


     
]

for serverInfo in serverList:
    server = SSHTunnelForwarder(
        (serverInfo['serverIp'],22),
        ssh_username=serverInfo['ssh_username'],
        ssh_password=serverInfo['ssh_password'],
        remote_bind_address=('0.0.0.0', serverInfo['desired_bind_port']),
        local_bind_address=('0.0.0.0', serverInfo['desired_bind_port'])
    )
    server.start()


while True:
    pass


