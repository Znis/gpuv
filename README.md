# gpuv
The GpuV web app is much like Google Colab (a cloud-based Jupyter notebook environment for Python coding). In this web app, users can sign in, gaining access to a Jupyter notebook interface to run their code. The app allows users to execute notebook files, upload files, and more. Importantly, the code runs on the server, not on the user's local machine. The server is equipped with multiple virtual machines and dedicated GPUs, providing the necessary hardware resources for accelerating data and machine learning projects and scripts.

The web application is built with HTML, CSS, and JavaScript for the frontend, while Django powers the backend. Django handles user authentication, the database, and provides an admin control panel. The platform for Jupyter notebook is hosted on virtual machines managed by the QEMU virtual machine manager in a Linux operating system. Communication between the Django server and the virtual machine manager is facilitated by a message broker software called RabbitMQ.

## Installation

#Steps on setting up the server machine  
 (Assuming the server machine is running Ubuntu Linux OS.)   

A. VM Setup:   
 - 1. Install the Virtual machine manager and set up the virtual machines (Ubuntu Server 22.04).
- 2. Enable the Root SSH in the VMs and setup the Root password too.
- 3. Setup the User Accounts in the VMs. (The user accounts are the users who will be using the VMs for running their code in Jupyter notebook. Later, we will create the users with the same name in the django web app too.)
- 4. Create usersgroup to group the users in a usergroup.
- 5. Setup the python virtual environments for each user accounts and install Jupyter Notebook in it.
- 6. Generate the Jupyter Notebook config file and edit the Content-Security-Policy line as follows in order to allow the notebook to be displayed in an /<iframe/>.
    >
     > c.NotebookApp.tornado_settings = {'headers': {'Content-Security-Policy': "frame-ancestors 'self' *"}}) 
    >                                                          
   Different approach can be implemented for allowing the notebook to be - displayed inside an /<iframe/> if required.  
- 7. Setup the password in the Jupyter Notebook for each user.  
- 8. Add a custom js file for Jupyter Notebook config to prevent the notebook from opening a new tab in every link click.  
- 9. Edit the ~/.profile file of each user account in order to auto activate the virtual environment as soon as logged in.
 - 10. Add the VM's IP address, port, SSH username and password as a server list in the tunnel.py script. 
     
B. Host Machine Setup:
- 1. Install and run the RabbitMQ server.
- 2. Create a virtual environment and install the required packages from the requirements.txt file.
- 3. Create a superuser by running the command 'python manage.py createsuperuser'.
- 4. Run the Django development server by running the command 'python manage.py runserver'. The webappp server can be made accessible in the entire local network by adding the 0.0.0.0:/<PORT/> parameter in the command.
- 5. Access the Django admin panel and add the user accounts, user profiles and the VM list in the respective models.
- 6. Run the vmscript.py and tunnel.py script in separate terminal windows.






## Usage

The webapp can be browsed from the browser in any machine that is connected to the local network in which the server is in. The code executed on the webapp i.e. notebook is running on the server machine.

## Youtube Link Showing the Demo
[GpuV Project's Demo](https://www.youtube.com/embed/TGWBT7ZajAw)


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.
