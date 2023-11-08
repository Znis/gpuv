from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from gpuv.models import UserVm, Vmlist
from django.contrib.auth.models import User
import socket
from gpuv.utilities import *
import pika
import time
import libvirt

from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout




def login_handler(request):

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None :
            sameUserAlreadyAuth, vmStatus = isVmFree(user.id)
            if sameUserAlreadyAuth or vmStatus:
                if user.is_active:
                    auth_login(request,user)
                   
                    if not sameUserAlreadyAuth:
                        messages.success(
                        request, 'Login successful.')

                    else:
                        messages.warning(
                        request, 'Same User is already logged in from another device. Please browse carefully to avoid conflict.')
                    return render(request, 'index.html', {'iframeurl':notebookIP()})
            else:
                messages.warning(
                request, 'The VM allocated to you is in use at the current moment.')
                return render(request, 'login.html')
        else:
            messages.error(
                request, 'something went wrong')
            return redirect("/")




      
def sessionCheck(request):
    if request.method == 'POST':
        userstatus = request.POST.get('status') 
     
        if userstatus == '0':
            if request.user.is_authenticated:
                rabbitmqCommunicate(request.user.id, False)
                logout(request)

        
    return JsonResponse({'message': 'All Good'})


def sessionEnd(request):
    if request.user.is_authenticated:
      consumerstatus = rabbitmqCommunicate(request.user.id, False)
      logout(request)
      if consumerstatus:
        messages.warning(
                    request, 'You got logged out due to inactivity.')
        return render(request, 'login.html')
      else:
            messages.warning(
                    request, 'You got logged out due to inactivity and VM shutdown failed.')
            return render(request, 'login.html')
    else:   
        messages.warning(
                request, 'You got logged out due to inactivity.')
        return render(request, 'login.html')


         

def loginPage(request):
    if request.user.is_authenticated:
      return render(request, 'index.html', {'iframeurl':notebookIP()})
    else:   
        return render(request, 'login.html')


def userlogout(request):
    if request.user.is_authenticated:
        consumerstatus = rabbitmqCommunicate(request.user.id, False)
        logout(request)
        if consumerstatus:
            messages.success(
                request, 'Logged Out Successfully')
            return redirect("/") 
        else:
            messages.warning(
                request, 'Logged Out But VM couldnot shut down')
            return redirect("/") 


def index(request):
 conn = libvirt.open()
 if conn is None:
        error_message = 'Failed to connect to the hypervisor.'
        return render(request, 'index.html', {'error_message': error_message})

 try:
        domains = conn.listAllDomains()
        vm_list = []
        for domain in domains:
            name = domain.name()
            state, _ = domain.state()
            vm_list.append({'name': name, 'state': state})
        
        return render(request, 'index.html', {'vm_list': vm_list, 'iframeurl':notebookIP()})
 finally:
        conn.close()








    

def backend(request):
    
    if request.user.is_authenticated:

        userid = request.user.id
        statusConsumer = rabbitmqCommunicate(userid, True)
        if statusConsumer:
        
            resp = {'status': 'success'}
            
            
            
        else:
            resp = {'status': 'failed'}
            
        
        return JsonResponse(resp)
     
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

    
         


def rabbitmqCommunicate(userid, sessionstate):
        
        dataqueryfromuservm = UserVm.objects.filter(user_choice_id = userid).values()[0]
        vmtoinit = dataqueryfromuservm['vm_choice_id']
        dataqueryfromvmlist = Vmlist.objects.filter(id = vmtoinit).values()[0]
        vmtoinit = dataqueryfromvmlist['vm_name'] 
        vmipaddr = dataqueryfromvmlist['ipaddr']   
        vmrootname = dataqueryfromvmlist['rootname']
        vmrootpass = dataqueryfromvmlist['rootpass']     
        vmaccountname = dataqueryfromuservm['accountname'] 
        vmaccountpass = dataqueryfromuservm['accountpass'] 
        data = {
            "vmname": vmtoinit,
            "vmipaddr": vmipaddr,
            "vmaccountname" : vmaccountname,
            "vmaccountpass": vmaccountpass,
            "vmrootname": vmrootname,
            "vmrootpass" : vmrootpass,
            "sessionstate": str(sessionstate)
        }
        data = str(data)
        data = data.replace("'","\"")
        
     



       
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        # Enable publisher confirms
        channel.confirm_delivery()

        # Declare a queue to send messages
        channel.queue_declare(queue='vm_start_queue')

        # Send a message to start the VM and activate Jupyter Notebook
        channel.basic_publish(exchange='', routing_key='vm_start_queue', body= data)
    
    

    
        

        statusConsumer = False
    
        
            
        # Connect to the message queue system
        connection2 = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel2 = connection2.channel()

        # Declare the same queue as in the producer
        channel2.queue_declare(queue='vm_start_status')

        for method_frame, properties, body in channel2.consume(queue='vm_start_status', inactivity_timeout=4):
            
            if method_frame:
                # Process the received message
                statusConsumer = True
                channel2.basic_ack(delivery_tag=method_frame.delivery_tag)
                
            else:
                # No message received within the timeout
                print("No message received within the timeout")
                for method_Frame, b, c  in channel.consume(queue='vm_start_queue'):
                    channel.basic_ack(delivery_tag= method_Frame.delivery_tag )
                    break
        
            break

            # Close the connection
        connection.close()
        channel2.cancel()
        connection2.close()
    
        return statusConsumer
    


    
    
def notebookIP():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.connect(("8.8.8.8", 80))
    server_ip = my_socket.getsockname()[0]
    notebook_ip = "http://" + server_ip + ":8888"  #update this port as per server bind port
    return notebook_ip
   
   



   
