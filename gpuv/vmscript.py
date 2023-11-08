import pika
import libvirt
import subprocess
import time

import json


import paramiko
import getpass





def destroy_running_users(ipaddr,rootname,rootpass,current_user, kill_current_user):
    # Connect to the SSH server
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ipaddr, username="root", password= rootpass)
    

    try:
        
        groupname = "usersgroup"
        uidlowerlimit = 1000
        # Terminate the existing user's session
        command = "getent group " + groupname
        _, stdout, stderr = ssh.exec_command(command)
       
        group_info = stdout.read().decode('utf-8').split(":")
        users = group_info[3].split(",")
        group_users = list(users)
    
        for username in group_users:
            _, uid, _ = ssh.exec_command(f"id -u {username}")
          
            uid = int(uid.read().decode('utf-8'))
            if not kill_current_user:
                if username != rootname and username != current_user and uid > uidlowerlimit:
                    _, stdout, stderr = ssh.exec_command(f"pkill -u {username}")
                    exit_status = stdout.channel.recv_exit_status()

                    if exit_status != 0: 
                        print(f"Cant kill this user's processes (maybe offline): {username}")
            else:
                if username != rootname and username == current_user and uid > uidlowerlimit:
                    _, stdout, stderr = ssh.exec_command(f"pkill -u {username}")
                    exit_status = stdout.channel.recv_exit_status()

                    if exit_status != 0: 
                        print(f"Cant kill current user's processes: {username}")
            



        



        exit_status = stdout.channel.recv_exit_status()

        if exit_status != 0:
            
            print(f"Error: {stderr.read().decode()}")

       
        

      

    

    finally:
        # Close the SSH connection
        ssh.close()


def connect_user_and_init_notebook(hostname, username, password):
    # Connect to the SSH server
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname = hostname, username=username, password= password)
    
    

    try:

        

        ssh.exec_command(". virtualenv/bin/activate ; jupyter notebook --no-browser --ip=0.0.0.0 --port=8888")
       

       


  

       
        

      

    

    finally:
        # Close the SSH connection
        ssh.close()
      







def start_vm():
  
    conn = libvirt.open()
    if conn is None:
        print('Failed to connect to the hypervisor')
        return
  
    try:
        domains = conn.listAllDomains()
        for domain in domains:
            vm_name = domain.name()
            vm = conn.lookupByName(vm_name)
            if vm is None:
                print(f'VM {vm_name} not found')
                continue

            # Check if the VM is already running
            if vm.isActive():
                print(f'VM {vm_name} is already running')
                continue

            # Start the VM
            vm.create()
            
      
            

            print(f'Started VM {vm_name} successfully')
    except libvirt.libvirtError as e:
        print(f'Error starting VM {vm_name}: {str(e)}')
    finally:
        conn.close()





def statusProducer(vmname):
  
    connection2 = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel2 = connection2.channel()
    # Enable publisher confirms
    channel2.confirm_delivery()
     # Declare a queue to send messages
    channel2.queue_declare(queue='vm_start_status')
    msg = str(vmname)
    

    # Send a message to start the VM and activate Jupyter Notebook
    channel2.basic_publish(exchange='', routing_key='vm_start_status', body = msg )
    # Close the connection
    connection2.close()




def callback(ch, method, properties, body):
     # Once the task is completed, acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)
    data = body.decode('utf-8')
    data = json.loads(data)
    
    if (data['sessionstate'] == "True"):
        kill_current_user = False
        statusProducer(data['vmname'] + " " + data['vmaccountname'] + "started" )
        destroy_running_users(data['vmipaddr'],data['vmrootname'],data['vmrootpass'],data['vmaccountname'], kill_current_user)
        connect_user_and_init_notebook(data['vmipaddr'],data['vmaccountname'],data['vmaccountpass'])
    else:
        kill_current_user = True
        statusProducer(data['vmname'] + " " + data['vmaccountname'] + " exited" )
        destroy_running_users(data['vmipaddr'],data['vmrootname'],data['vmrootpass'],data['vmaccountname'], kill_current_user)
   
   

    # start_vm(vmtoinit)


#     ssh_command = [
#     "jupyter","notebook","--no-browser" , "--ip=0.0.0.0", "--port=8888"


# ]
#     subprocess.run(ssh_command, shell=False)

   

start_vm()
# Connect to the message queue system
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the same queue as in the producer
channel.queue_declare(queue='vm_start_queue')

# Set the maximum number of unacknowledged messages to 1
channel.basic_qos(prefetch_count=1)

# Set the callback function to process incoming messages
channel.basic_consume(queue='vm_start_queue', on_message_callback=callback)

# Start consuming messages
channel.start_consuming()



