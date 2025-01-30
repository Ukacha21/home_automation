#Python 3.12.3 - used in this project
#--------------------------------------

#API to manage connection and values 
#input from the GUI to the DB

import sqlite3

# conn = sqlite3.connect('home_control.db')
# c = conn.cursor()
#--------------------------------
"""
living room
kitchen
suite
boys room
girls room
front balcony
back balcony
compound-quintal
"""
# increment  = 0

class DatabaseCommands:

    def init_connection(database, *args):
        #database = home_control.db
        conn = sqlite3.connect(database)
        # self.c = self.conn.cursor()
        return conn
    
    
    
    def get_icon(conn, appliance, location):
        cursor = conn.cursor()

        cursor.execute("SELECT state FROM appliances WHERE appliance = ? AND location = ?", (appliance,location))
        state = cursor.fetchone()[0]
        # global increment
        # increment += 1
        print("state: ", state)

        if state == 0:
            return "toggle-switch-off-outline"
        elif state == 1:
            return "toggle-switch"
        else:
            print("something went wrong")
        # print(state)



    # @classmethod
    def close_connection(conn):
        conn.close()
    
    def __del__(self):
        self.conn.close()

    def create_table(conn, appliances, table_name="appliances"):
        # con = self.conn
        cursor = conn.cursor()
        # Create a table to store the appliances and their states
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            appliance TEXT,
            state INTEGER,
            location TEXT
            )''', #; at the end of the statement
            
            )
        cursor.executemany("INSERT INTO appliances (appliance, state, location) VALUES (?, ?, ?)", appliances)
        conn.commit()
        res = """
            table ccreated succcessfully
            appliances inserted into database
            committing
            success
            """
        print(res)
        # cursor.close()
    
    def add_appliance(conn, appliance, state=0, location=None):
        # self.conn = sqlite3.connect('home_control.db')
        # self.c = self.conn.cursor()

        #add the listed appliances
        c = conn.cursor()
        c.execute("INSERT INTO appliances (appliance, state, location) VALUES (?, ?, ?)", (appliance, state, location))
        conn.commit()
        # c.close()

    #switch appliances on/off
    def update_appliance_state(conn, appliance, state, location=None):
        c = conn.cursor()
        # Update the state of the specified appliance
        c.execute("UPDATE appliances SET state = ? WHERE appliance = ? AND location = ?", (state, appliance, location))
        conn.commit()
        print(f"{appliance} set to {state}")
        # c.close()

    def update_all_states(conn, state):
        c = conn.cursor()
        # Update the state of the specified appliance
        c.execute("UPDATE appliances SET state = ?", (state,)) #WHERE NOT appliance <> ? | "cut_all"
        conn.commit()
        print("all updated")
        c.execute("SELECT * FROM appliances")
        appliances = c.fetchall()
        
        for id, appliance, state, location in appliances:
            print(f"{id}| {appliance}: {state}: {location}")
        # c.close()

    def get_appliance_info(conn, appliance, location):
        # conn = sqlite3.connect('home_control.db')
        c = conn.cursor()

        # Fetch the state of the specified appliance
        c.execute("SELECT * FROM appliances WHERE appliance = ? AND location = ?", (appliance,location))
        info = c.fetchone()

        # conn.close()

        if info:
            return info#[0]
        else:
            return None
    def get_state(conn, appliance, location="*"):
        cursor = conn.cursor()

        cursor.execute("SELECT state FROM appliances WHERE appliance = ? AND location = ?", (appliance,location))
        state = cursor.fetchone()[0]
        # print("state: ", state)

        return state
        # print(state)
    def list_available_appliances(conn):
        # conn = sqlite3.connect('home_control.db')
        c = conn.cursor()

        # Fetch all appliances and their states
        c.execute("SELECT * FROM appliances")
        appliances = c.fetchall()

        # c.close()

        # Print the list of appliances
        for id, appliance, state, location in appliances:
            print(f"{id}| {appliance}: {state}: {location}")
        

