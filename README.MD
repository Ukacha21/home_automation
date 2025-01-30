``Python 3.12.3 -Used Version``


Creating a Python-Based Remote Control System for Your Home
Understanding the Components
Before we dive into the code, let's break down the key components of your system:

Mobile App: This will be the user interface for sending commands.
Database: A cloud-based database to store user commands and device states.
Server: A server (e.g., a Raspberry Pi or a cloud-based server) that will:
Connect to the database.
Receive commands from the mobile app.
Process and execute commands on your home devices (e.g., Raspberry Pi).


Python Libraries and Technologies
We'll use the following Python libraries and technologies:

* Flask: For creating the web server.
* SQLite: For a local database (can be replaced with a cloud-based solution like Firebase or MongoDB).
* Requests: For making HTTP requests from the mobile app to the server.
* MQTT: For real-time communication between the server and your home devices.




**Important:** `you need to add encryption methods, if you use implement this at your own home`

Yes, you can host a home_control.db file on your router, provided your router supports USB storage or has a built-in feature for file sharing. Here’s a general approach:

Check Router Compatibility: Ensure your router supports USB storage or file sharing (like Samba).

Connect Storage: If your router has a USB port, connect a USB drive.

Enable File Sharing: Access your router’s settings via its IP address (commonly 192.168.1.1 or similar) and enable file sharing or Samba.

Upload the Database: Upload the home_control.db file to the shared folder on the USB drive.

Access from Devices:

PC: Use the network path to access the shared folder (e.g., \\router_ip\shared_folder).
Raspberry Pi: You can use Samba or mount the shared directory with a command like:
bash
Copy code
sudo mount -t cifs //router_ip/shared_folder /mnt/shared -o user=username,password=password
Ensure Permissions: Make sure the file permissions allow read/write access from both devices.

Additional Tips
Backup: Regularly back up your database in case of corruption.
Network Stability: Ensure your router has a stable connection to prevent data loss.
Security: If sensitive, consider securing your shared folder with a password.
This setup allows you to easily access and modify the database from both your PC and Raspberry Pi.


---------------------------------------

To share a home_control.db file and access it from a Raspberry Pi using Python and SQLite, you can consider two methods: one using a router with network file sharing and the other using a Raspberry Pi as a file server.

Method 1: Using a Router with SMB/CIFS
Setup SMB on the Router:

Many routers support Samba (SMB/CIFS) for file sharing. Check your router’s firmware to enable file sharing (e.g., DD-WRT or OpenWrt can provide this functionality).
Enable the file sharing feature and create a shared folder for the home_control.db file.

**Method 1**:
Accessing the Shared File from Raspberry Pi:

* Install the required package:
 ```bash
    sudo apt update
    sudo apt install cifs-utils
```

* Create a mount point:
```bash
mkdir ~/shared_folder
```

* Mount the shared folder (replace `<router_ip>, <share_name>, <username>`, and `<password>`):

```bash
    sudo mount -t cifs //<router_ip>/<share_name> ~/shared_folder -o username=<username>,password=<password>
```

* Access the database in Python:
```python
import sqlite3

conn = sqlite3.connect('~/shared_folder/home_control.db')
cursor = conn.cursor()
# Perform database operations...
conn.close()
```
-------------------------------------

**Method 2**:
Using Raspberry Pi as a File Server

***1-Setup Samba on the Raspberry Pi:***

* Install Samba:
```bash
sudo apt update
sudo apt install samba
```
* Configure Samba by editing the configuration file:
```bash
sudo nano /etc/samba/smb.conf
```
* Add the following to the end of the file to share the directory containing home_control.db:

```bash
[home_control]
path = /path/to/your/db/folder
browseable = yes
read only = no
guest ok = yes
```

* Restart the Samba service:
```bash
sudo systemctl restart smbd
```

***2-Accessing the Shared File from Another Device:***

From the Raspberry Pi or any other device on the same network, you can mount the shared folder similarly to the first method.
If you’re accessing it from the Raspberry Pi itself, you can directly access the database file without mounting it:
```python
import sqlite3

conn = sqlite3.connect('/path/to/your/db/folder/home_control.db')
cursor = conn.cursor()
# Perform database operations...
conn.close()
```

**Summary**

`Method 1`: Use your router for SMB sharing and mount it on the Raspberry Pi.

`Method 2`: Set up the Raspberry Pi as a Samba file server for direct access.
In both cases, make sure to adjust permissions and network settings as needed for secure access!

----------------------

***To access a file shared on a router from a Windows computer using Python, you can follow these steps:***

`**Step 1`: Map the Network Drive**

First, you need to map the shared folder to a network drive in Windows:

Open File Explorer.
Right-click on "This PC" and select "Map network drive...".
Choose a drive letter (e.g., Z:).
In the Folder field, enter the path to the shared folder in the format \\`<router_ip>\<share_home_control_foldername>`.
If required, check "Reconnect at sign-in" and enter the necessary credentials.
Click Finish.

`Step 2`: Access the File in Python
Now that the shared folder is mapped, you can access it using Python. Here’s an example of how to read a SQLite database file from the mapped network drive:

* Install the SQLite library (if it's not already installed, but it's included with Python by default):

```bash
pip install sqlite3
```

* Use the following Python code to access the database:

```python
import sqlite3

# Path to the SQLite database on the mapped drive
db_path = r'Z:\home_control.db'  # Replace 'Z:' with your mapped drive letter

# Connect to the SQLite database
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Example query
    cursor.execute("SELECT * FROM your_table_name")  # Replace with your actual query
    rows = cursor.fetchall()

    # Print the results
    for row in rows:
        print(row)

except sqlite3.Error as e:
    print(f"An error occurred: {e}")
finally:
    if conn:
        conn.close()

```

**Key Points:**

* Ensure the shared folder is accessible before running the script.
* Use raw string notation (r'...') for the file path to handle backslashes correctly in Windows.
* Adjust the SQL query and table name as needed for your database structure.

This will allow you to read data from the SQLite database stored on your router's shared folder!

**Full Path Example**

If your router’s IP address is 192.168.1.1 and your shared folder is named home_control, the path would look like this:

```
\\192.168.1.1\home_control
```

You would use this path to map the network drive or access files in your Python code.
