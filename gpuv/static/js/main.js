
document.addEventListener("DOMContentLoaded",function(){
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
function initBtn(vmList){
    
document.addEventListener('DOMContentLoaded', function() {
  
var buttonContainer = document.getElementById('button-container');



vmList.forEach(function(vm) {
var button = document.createElement('button');
button.id = vm.name;
if (vm.state == 1){
button.innerHTML = vm.name + ' ' + '<span class="dot" id="green-dot"></span>';

// button.addEventListener('click', function() {
//     checkSession(1);
//     const data = {
//         vmtoinit: vm.name.toString(),
      
//       };
    
       
//         $.ajax({
//             url: 'backend/',
//             headers:{'X-CSRFToken': csrftoken},
//             method: 'POST',
          
//             data: data,
            
            
            
//             success: function(response) {
           
//                resp(response, vm.name);
//             },
//             error: function(error) {
                
//             }
//         });
    
// });
}
if (vm.state == 10){
    button.innerHTML = vm.name + ' ' + '<span class="dot" id="red-dot"></span>';
    button.disabled = true;
    

 
    }
buttonContainer.appendChild(button);
});
});
}


function resp(response, vmname){
    if((response).status.toString() == "failed"){
        document.getElementById("responsee").innerHTML = "Failed";
        document.getElementById(vmname).disabled = true;
        document.getElementById(vmname).innerHTML = vmname + ' ' + '<span class="dot" id="red-dot"></span>';
        
        }
        
        if((response).status.toString() == "success"){
        document.getElementById("responsee").innerHTML = "Success";
        document.getElementById(vmname).disabled = true;
        
        }
}
// Set the timeout duration (in milliseconds)
var timeoutDuration = 60000;



    function checkSession(statusData) {
        // Make an AJAX request to your Django server
        // Here, you can use libraries like Axios, jQuery, or the native fetch API
        // Example using fetch API

        var data = {status: statusData};




            fetch('/checksession/',{
            headers:{'X-CSRFToken': csrftoken},
            method: 'POST', data: data,})
              .then(response => response.json())
              .then(data => {
                if (statusData == 0){
                    window.location.href = "/sessionend/";
                     }
              })
              .catch(error => {
                // Handle any error that occurred during the API request
                console.error(error);
              });
          




       
        }

function userlogout(){
    window.location.href = "/logout/";

}

var initbtn = document.getElementById("init");
var iframe = document.getElementById("embeddedContent")
initbtn.addEventListener("click",function(){



      fetch('/backend/',  {
        method: 'POST', // Specify the HTTP method (e.g., POST, GET, PUT, DELETE)
        headers: {
            'X-CSRFToken': csrftoken
        },
        
      })
    .then(response => response.json())
    .then(data => {
      // Handle the API response
      console.log(data);
    })
    .catch(error => {
      // Handle any error that occurred during the API request
      console.error(error);
    });
    
    iframe.style.display = "block";
});




var logoutbtn = document.getElementById("logoutBtn");
logoutbtn.addEventListener("click",userlogout);



var dialogBox = document.getElementById("dialogBox");
var confirmBtn = document.getElementById("confirmButton");
var timerSpan = document.getElementById("timerSpan");
confirmBtn.addEventListener("click",function(){
checkSession(1);
resetTimer();
});


// Variable to hold the timeout reference
var timeoutRef;

// Variables to track the last activity time
var lastMouseMoveTime;
var lastKeydownTime;

// Flag to track if alert box has been shown
var isAlertShown = false;



var timer;
   
var dialogVisible = false;
var timerSeconds = 30;

// Function to display the alert box
function showAlertBox() {
showDialog();
var remainingTime = timerSeconds;
timerSpan.innerText = timerSeconds;
timer = setInterval(function(){
    remainingTime -- ;
   if (remainingTime <= 0){
        clearInterval(timer);
        hideDialog();
        checkSession(0);
      

    } else {
        timerSpan.innerText = remainingTime;
    }
}, 1000);
}


function resetTimer(){
    clearInterval(timer);
    hideDialog();
    
}

function showDialog(){
    dialogBox.style.display = "block";
    dialogVisible = true;
}

function hideDialog(){
    dialogBox.style.display = "none";
    dialogVisible = false;
}

// Function to reset the timeout
function resetTimeout() {
clearTimeout(timeoutRef);
timeoutRef = setTimeout(showAlertBox, timeoutDuration);
}

// Update the last mouse move time and reset the timeout
function handleMousemove() {
lastMouseMoveTime = Date.now();
resetTimeout();
}

// Update the last keydown time and reset the timeout
function handleKeydown() {
lastKeydownTime = Date.now();
resetTimeout();
}

// Attach the mousemove and keydown event listeners
document.addEventListener('mousemove', handleMousemove);
document.addEventListener('keydown', handleKeydown);

// Start the initial timeout
resetTimeout();

// Check if both mouse and keyboard activity are absent
function checkUserActivity() {
var currentTime = Date.now();
if (
!isAlertShown &&
currentTime - lastMouseMoveTime >= timeoutDuration &&
currentTime - lastKeydownTime >= timeoutDuration
) {
showAlertBox();
}
}

// Check user activity periodically
setInterval(checkUserActivity, timeoutDuration);


  // Set the interval to 20 seconds (20000 milliseconds)
  setInterval(() => {
  
    checkSession(1);
  }, 600000);





// Display the session expired message
function displaySessionExpiredMessage(arg) {
// Add your code to display the message on the frontend
// This can be done by updating the DOM, showing a modal, or any other UI approach you prefer
// Example:
const messageElement = document.getElementById('responsee');
messageElement.innerHTML = arg;

}







// document.addEventListener('DOMContentLoaded', checkSession); // Run on page load
// window.addEventListener('beforeunload', checkSession); // Run on page unload
});