# attendance_system
 Attendance system using face Reognition

Objective:
To build a prototype of an engine which records an Attendance using Face
Recognition Technology.
• In this case, we will create a website using Flask framework in Python which
will be used as a mode of communication and for routing between our UI,
Cloud server (Amazon EC2). Python advanced Libraries, Packages and
Machine Learning Trained Models will be used to do heavy lifting work of
Face Detection. Face Recognition, Image Comparison.
• It is a Client-Server architecture using the technique called Message Passing
over the Network/Internet using SSH/TCP for routing and locating both the
client and server.
▪ The client starts the camera and sends the frames from local machine
to the server.
▪ Server Processes the frame and follows the further steps of storing in
DB, Recording, Sending Response, etc.

Basic Hardware Configuration Used To Build System-
o 8 gb RAM

o 1 TB HDD
o Processor- AMD Ryzen 5, 2.1 GHz processor
o Windows OS with 64 bit OS
Technologies used here:
o Python v-3.6
o Flask framework v-1.1.1
o Jupyter Notebook (5.4.0) from Anaconda Navigator v-5.2
o Winscp, Putty
o AWS EC2 cloud server
o JavaScript, CSS, HTML

First, let us see what is the process-flow of whole system-

• A continuous VideoStream is always active once the Website is launched. The
Camera continuously monitors and is live on the top-right corner of Website.
• First User Registers as an Employee on System. One Image is Captured along with
Name while registration.
• Once registered the user, Attendance will be recorded from the very next moment
onwards and the details will be stored in Database (DB).
• Details like ID, NAME, ARRIVAL TIME, DEPARTURE TIME, ARRIVAL
PICTURE, DEPARTURE PICTURE are being stored in Database for each user.
• The unique identifier for a user here is NAME. So, it needs to be unique. If in case the
initial part of name is same for any 2 users, we can use combination of first name and
last name, etc, while registering. ID is being used, given a unique search from
backend during a particular day (if required).
• For each day, the 24 hour cycle will be used to be considered as an attendance IN time
and OUT time. If camera saw user for first in a day, it will be considered as a new
entry for that day and above details will be stored in DB and folders.
• If on a same day, camera saw a user again than it will be considered as an out time for
the same day. Same thing of OUT time will be repeated for the consecutive number of
time whenever camera saw same user on same day. Before the end of 24 hour cycle
for same day, whichever is the last entry of this user for departure time/details, will be
considered as the final departure time/details for same day.
• On GUI, we can also check the Last 5 entries saw by Camera. Simply a click of
button and it shows you all details.
• Apart from this, we can check the details of any particular (one) employee by just
entering the name (same name used while registering) of employee and submit it.
• We also have the functionality of Deleting the Employee completely from System.
• Lastly, if we want to get the details of all Registered Employees at once, we can do it
from the GUI.