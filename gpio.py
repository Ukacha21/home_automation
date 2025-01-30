#Python 3.12.3 - used in this project
#--------------------------------------

"""
First thing Mount the shered Folder on the router to the raspberry Pi,
Steps Explained within ReadMe.md
"""

"""
("irrigation_systems", 0, "compound"),

is going to be automatic, not to depend on database commmands, or
set the databbese on/off fo the irrigation system then operate on it


------------------------------------------------

coompound lights will have 4 values,

0 all off, 
1 compound lights on, 
2 outside lights on, 
3 both on

-------------------------

curtains and windows 

0 close
1 curtains open
2 windows open
3 curtains close
4 windows close

"""


from threading import Timer as timer

import os, time


from dbmanager import DatabaseCommands as DBComms

database = "databases/home_control.db"

# conn = DBComms.init_connection(database) #defined in init function

# from RPi.GPIO import GPIO as Board
from RPiGPIO import GPIO as Board
#fix RPi.GPIO with the dot later

appliances = [

    ("SOS_alarm_systems", 0, "compound"),# place button under show_feed button

    #Outside---------------------
    ("compound_lights", 0, "outside"), # button without iccon

    ("garage_gate", 0, "compound"),
    ("small_gate", 0, "compound"),

    #rooms
    ("rooms_fire_systems", 0, "general"),

    #general---------------------
    ("general_fire_systems", 0, "general"),
    
    ("general_main_lights", 0, "general"),
    ("general_rgb_tapelights", 0, "general"),
    ("house_kitchen_lights", 0, "general"),

    ("general_windows_curtains", 0, "general"),

    ("house_backdoor", 0, "general"),
    ("house_frontdoor", 0, "general"),

    #cut all of the above
    ("cut_all", 0, "general"),

    ]



appliance_dictionary = {
#Outside---------------------

#MULTIPLE STATES
"compound_lights" : 2, # button without iccon
"general_windows_curtains" : 3,


#DUAL STATES

"SOS_alarm_systems" : 4, # place button under show_feed button

"garage_gate" : 11,
"small_gate" : 13,

#rooms
"rooms_fire_systems" : 15,

#general---------------------
"general_fire_systems" : 19,
    
"general_main_lights" : 21,
"general_rgb_tapelights" : 23,
"house_kitchen_lights" : 27,


"house_backdoor" : 29,
"house_frontdoor" : 31,

#cut all of the above
"cut_all" : 33, }


"""
#examples of dictionary usage:

#GETTING VALUES FROM KEYS --------------------

my_dict = {'name': 'Alice', 'age': 30, 'city': 'New York'}
print(my_dict['name'])  # Output: Alice

#GETTING KEYS FROM VALUES -------------------

def get_key_from_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None

age_key = get_key_from_value(my_dict, 30)
print(age_key)  # Output: age

#CHANGING VALUES---------------------

my_dict = {'name': 'Alice', 'age': 30, 'city': 'New York'}
my_dict['age'] = 31

--------------------------
You can use the items(), keys(), and values() 
methods to iterate over the key-value pairs, keys, 
or values of a dictionary, respectively.

"""

# for i in appliance_dictionary.keys():
#     print(str(i), ":", appliance_dictionary[i]) # Output:

class Main:

    """

    by making it 
    __restart method,
    rstart should not be accessible from outside the class
    like other methods do


    ----------------------------------------

    GPIO Pin Numbering: Ensure you're using the correct GPIO pin 
        numbering convention (BCM or BOARD). BCM numbering is generally 
        preferred as it's more consistent across different Raspberry Pi 
        models.
    
    *Pull-Up/Pull-Down Resistors: If you need to ensure a stable input 
        value when no external signal is connected, consider using a 
        pull-up or pull-down resistor. You can add this by passing the 
        GPIO.PUD_UP or GPIO.PUD_DOWN argument to the GPIO.setup() function:

    GPIO.setup(your_pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Pull-up resistor

    """

    def __init__(self, conn):
        try:
            self.conn = DBComms.init_connection(database)
        except:
            print("Failed to connect to the database\nrestablishing connection...")
            try:
                DBComms.close_connection(self.conn)
                self.conn = DBComms.init_connection(database)
            except:
                print("Fatal.......")

            
        # super().__init__()
        


    def __restart(conn, *args, **kwargs):
        # os.execl("python", "gpio.py")
        print("Restarting...")
        #restart connection and the raspberry code
        try:
            DBComms.init_connection(conn)
            #quit current python file and restart
            #exec("gpio.py")
            # os.system("python3 gpio.py")
        except:
            print("Restart failed")

    def setup(pin, mode, *args, **kwargs):
        if mode.lower() == "in":
            Board.setup(pin, Board.IN)
        elif mode.lower() == "out":
            Board.setup(pin, Board.OUT)
        else:
            print("Invalid mode")

    def write(pin, value, *args, **kwargs):
        if str(value) == "0":
            Board.setup(pin, Board.LOW)
        elif str(value) == "1":
            Board.setup(pin, Board.HIGH)
        else:
            print("Invalid VALUE")

    def main(self):

        Board.setmode(Board.BCM) #BCM is recommended over BOARD

        run = True

        while run:

            try:
                for i in appliance_dictionary.keys():

                    state = DBComms.get_state(self.conn, str(i))
                    self.write(appliance_dictionary[i], state) #appliance_dictionary[i] = pin number
                    print(f"{i} : {state}")
                    time.sleep(0.5)
            except:
                self.__restart()



# Main.__restart()
Main().main()



