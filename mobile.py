# Python 3.12.3 - used in this project
# Kivy                      2.3.0
# kivymd                    1.2.0
#--------------------------------------
import kivy
kivy.require('2.1.0')

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
# from kivymd.uix.screenmanager import MDScreenManager
# from kivymd.uix.textfield import MDTextField
from kivymd.uix.circularlayout import MDCircularLayout
# from kivymd.uix.floatlayout import MDFloatLayout
# from kivymd.uix.relativelayout import MDRelativeLayout
# from kivymd.uix.boxlayout import MDBoxLayout
# from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDFillRoundFlatIconButton, MDRectangleFlatIconButton, MDFloatingActionButton
from kivymd.uix.label import MDLabel

from kivy.uix.image import Image
# from kivy.uix.camera import Camera

# from kivy.clock import Clock
# from kivy.graphics.texture import Texture
# from kivymd.uix.fitimage import FitImage

from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.swiper import MDSwiper, MDSwiperItem

from kivy.core.window import Window
Window.size = (2560/2, 1600/2)#(2560, 1600) #glxy tab s7fe
#(393, 650)

#cyteps on ly for windows
# import ctypes
# user32 = ctypes.windll.user32
# screen_width = user32.GetSystemMetrics(0)
# screen_height = user32.GetSystemMetrics(1)

# from kivy.network.urlrequest import UrlRequest

# from PIL import Image as PILImage
# from PIL import ImageTk
# import os

from threading import Timer as timer

import random
# , time

# from hotreload import Loader as hotreloader
# from kaki.app import App as KakiApp

from dbmanager import DatabaseCommands as DBComms

"""
Map the Network Drive on computer , Steps explained in ReadMe.MD
"""

database = "databases/home_control.db"

# timeout_bool = False
# timeout_var = 0
# command = True

# conn = DBComms.init_connection(database)

# try:
#     os.system("del /s /q temps")
# except Exception as e:
#     print(e)

# try:
#     os.system("mkdir temps")
# except:
#     pass

# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler

# class MyEventHandler(FileSystemEventHandler):
#     def on_modified(self, event):

#         if event.is_directory:
#             return
#         if event.src_path == "mobile.py":  # Check for specific file name
#             print("mobile.py modified:", event.src_path)
#             # Trigger a reload of your Kivy application
#             App.get_running_app().reload()

"""
#appliances-------------------

compound_lights
outside_lights
SOS_alarm_systems
irrigation_systems
garage_gate
normal_gate
car_entrance gate

general_fire_systems
rooms_fire_systems

house_main_lights(dining, living)
rgb_tapelights(dining, living, hallway)
house_kitchen lights
general_windows
general_curtains
house_back door
house_front door

#locations ----------------

# livin

general
compound
outside
rooms

#suite
# compound-quintal
"""

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

class Home_Automation(MDApp):

    # KV_FILES = {
    #     os.path.join(os.getcwd(),"mobile.kv")
    # }
    # CLASSES = {
    #     "Myapp":"view.mobile"
    # }

    # AUTORELOADER_PATHS = [
    #     (".", {"recursive": True})

    # ]

    #action handling functions--------------------------
    #pass


    #to be used in buttons & others
    text_colors = [
        (.1, .7, .1, 1), #green
        (1, 1, .7, 1), #yellowish white
    ]
    universal_text_color = text_colors[1]

    

    # timeout_bool = False
    # timeout_var = 0
    # command = True
    # timeout_default = 5

    def timeout_manager(self): #change timeout to 45
            
        if self.timeout_var >= self.timeout_default:
            # DBComms.close_connection(self.conn)
            # del self.conn
            print("Conn Timed out..")
            self.command = False
            self.timeout_bool = True
        else:
            self.timeout_var += 1
            print(self.timeout_var)

        # if self.command == True:
        #     # self.timeout_var = 0
        #     self.timeout_bool = False
        print(f"Timeout: {self.timeout_var}: {self.timeout_default}")
        print("Timeout bool: %s" % self.timeout_bool)
        print("Command: %s" % self.command)
        # print(timeout_default)
        print("-------------------------------------")

        if self.timeout_bool == False and self.timeout_var <= self.timeout_default:
            x = timer(1, self.timeout_manager)
            x.start()
            # print("recursion")
            
        # else:
        #     timeout_var = 0
        #     timer(timeout, conn.close).start()
        #     timeout_bool = True
        #     print("connection timed out")
    
    def manage_states(self, widget_variable, appliance, location):
        # state = DBComms.get_icon(conn, "general_rgb_tapelights", "general"),
        
        if self.timeout_bool == True:
            #reestabilish connection for the next timoeout
            self.conn = DBComms.init_connection(database)
            self.timeout_bool = False

        self.command = True
        self.timeout_var = 0
        self.timeout_manager()

        state = DBComms.get_state(self.conn, appliance, location)
        # print(state)
        # print(location)

        if state == 0:
            if appliance == "cut_all":
                DBComms.update_all_states(self.conn, 1)
                # DBComms.update_appliance_state(self.conn, appliance, 1, location)
            else:
                DBComms.update_appliance_state(self.conn, appliance, 1, location)
        elif state == 1:
            if appliance == "cut_all":
                DBComms.update_all_states(self.conn, 0)
                # DBComms.update_appliance_state(self.conn, appliance, 1, location)
            else:
                DBComms.update_appliance_state(self.conn, appliance, 1, location)
        if appliance == "cut_all":
            for i in self.all_buttons_list:
                i.icon = DBComms.get_icon(self.conn, appliance, location)
        
        widget_variable.icon = DBComms.get_icon(self.conn, appliance, location)

    def load_appliances_widgets(self):

        self.general_screen = MDScreen()

        self.general_circular_layout = MDCircularLayout(
            #orientation='vertical', 
            # radius='5dp'
            # pos_hint={'top': 1},
            # circular_padding = "50dp",
            # circular+radius = '5dp',    
            # pos_hint={'center_y': .8, 'center_x':.5},
            # background="#1e1e1e"
            )

        # aspect_ratio = 1/1 #4/1 16/9

        #temporarily disable camera

        # self.camera = Camera( 
        #     index = 0,
        #     play=True, #initialize camera
        #     # size_hint=(1, 0.5),
        #     # angle=45,
        #     allow_stretch=True,
        #     fit_mode = 'fill', #['scale-down', 'fill', 'contain', 'cover']
        #     # pos_hint={'center_y': .5},
        #     # width=screen_width,
        #     # height=screen_height,
        #     size_hint_x = aspect_ratio,
        #     size_hint_y = 1,
        #     # resolution=Window.size,
        #     #(self.main_swiper.width, self.main_swiper.height), #(640, 480),
        #     #self.general_screen.size
        #     )

        # print(screen_width, screen_height)

        # self.general_screen.add_widget(self.camera)

        """
        # implement living room image feed,
        # we can use cctv later on.

        # supported video formats: avi, mpg
        # """

        self.general_screen.add_widget(Image( #FitImage
            source = "images/home.png", #"images/home.png",
            fit_mode = 'fill', #['scale-down', 'fill', 'contain', 'cover']
            # angle=45,
            opacity = .3,
            # allow_stretch=True,
            ))
        """
        cant integratte opencv camera footage into the screen,
        make a separate code/class to launch another application
        """

        self.general_label = MDLabel(
            text="General",
            halign="center",
            # valign="center",
            font_style="H1",
            # font_size="50px",
            pos_hint={'center_x': .5, 'center_y': .6},
            opacity=0.3,
            text_color=self.universal_text_color  # Set a non-transparent color for the text
        )

        self.show_living_room_feed_button = MDRectangleFlatIconButton( #MDFillRoundFlatIconButton
            text="Show Feed",
            icon_size="35dp",
            # width="40dp",
            # font_style='H5',
            # icon="toggle-switch",
            pos_hint={'center_x': .5, 'center_y': .4},
            #valign="center", #['top', 'center', 'bottom']
            # on_release= None
            text_color=self.universal_text_color  # Set a non-transparent color for the text
        )
        self.general_screen.add_widget(self.show_living_room_feed_button)
        
        self.cut_all_button = MDRectangleFlatIconButton(
            text="Cut All",
            icon_size="56dp",
            # width="40dp",
            font_style='H4',
            icon=DBComms.get_icon(self.conn, "cut_all", "general"),
            pos_hint={'center_x': .5, 'center_y': .5},
            #valign="center", #['top', 'center', 'bottom']
            text_color=self.universal_text_color  # Set a non-transparent color for the text
        )
        self.cut_all_button.on_release=lambda: self.manage_states(self.cut_all_button, "cut_all", "general")

        self.general_screen.add_widget(self.cut_all_button)


        #TODO IMPLEMENT ON RELEASE ON ALL OTHER BUTTONS
        
        #circular layout widgets

        self.SOS_alarm_systems_button = MDRectangleFlatIconButton( #MDFillRoundFlatIconButton
            text="SOS Alarm System",
            icon_size="35dp",
            # width="35dp",
            # font_style='H6',
            icon=DBComms.get_icon(self.conn, "SOS_alarm_systems", "compound"),
            # pos_hint={'center_x': .5, 'center_y': .5},
            #valign="center", #['top', 'center', 'bottom']
            #on_release=self.switch_state,
            text_color=self.universal_text_color  # Set a non-transparent color for the text
        )
        self.SOS_alarm_systems_button.on_release=lambda: self.manage_states(self.SOS_alarm_systems_button, "SOS_alarm_systems", "compound")
        self.general_circular_layout.add_widget(self.SOS_alarm_systems_button)
        
        self.all_buttons_list.append(self.SOS_alarm_systems_button)

        self.compound_lights_button = MDRectangleFlatIconButton( #MDFillRoundFlatIconButton
            text="Compound lights",
            icon_size="35dp",
            # width="35dp",
            # font_style='H6',
            # icon="toggle-switch-off-outline",
            # pos_hint={'center_x': .5, 'center_y': .5},
            #valign="center", #['top', 'center', 'bottom']
            #on_release=self.switch_state,
            text_color=self.universal_text_color  # Set a non-transparent color for the text
        )
        # self.compound_lights_button.on_release=lambda: self.manage_states(self.compound_lights_button, "compound_lights", "outside")
        self.general_circular_layout.add_widget(self.compound_lights_button)
        
        # self.all_buttons_list.append(self.compound_lights_button)

        self.garage_gate_button = MDRectangleFlatIconButton( #MDFillRoundFlatIconButton
            text="Garage Gate",
            icon_size="35dp",
            # width="35dp",
            # font_style='H6',
            icon=DBComms.get_icon(self.conn, "garage_gate", "compound"),
            # pos_hint={'center_x': .5, 'center_y': .5},
            #valign="center", #['top', 'center', 'bottom']
            #on_release=self.switch_state,
            text_color=self.universal_text_color  # Set a non-transparent color for the text
        )
        self.garage_gate_button.on_release=lambda: self.manage_states(self.garage_gate_button, "garage_gate", "compound")
        self.general_circular_layout.add_widget(self.garage_gate_button)
        
        self.all_buttons_list.append(self.garage_gate_button)

        self.small_gate_button = MDRectangleFlatIconButton( #MDFillRoundFlatIconButton
            text="Small Gate",
            icon_size="35dp",
            # width="35dp",
            # font_style='H6',
            icon=DBComms.get_icon(self.conn, "small_gate", "compound"),
            # pos_hint={'center_x': .5, 'center_y': .5},
            #valign="center", #['top', 'center', 'bottom']
            #on_release=self.switch_state,
            text_color=self.universal_text_color  # Set a non-transparent color for the text
        )
        self.small_gate_button.on_release=lambda: self.manage_states(self.small_gate_button, "small_gate", "compound")
        self.general_circular_layout.add_widget(self.small_gate_button)
        
        self.all_buttons_list.append(self.small_gate_button)

        self.rooms_fire_systems_button = MDRectangleFlatIconButton( #MDFillRoundFlatIconButton
            text="Rooms Fire System",
            icon_size="35dp",
            # width="35dp",
            # font_style='H6',
            icon=DBComms.get_icon(self.conn, "rooms_fire_systems", "general"),
            # pos_hint={'center_x': .5, 'center_y': .5},
            #valign="center", #['top', 'center', 'bottom']
            #on_release=self.switch_state,
            text_color=self.universal_text_color  # Set a non-transparent color for the text
        )
        self.rooms_fire_systems_button.on_release=lambda: self.manage_states(self.rooms_fire_systems_button, "rooms_fire_systems", "general")
        self.general_circular_layout.add_widget(self.rooms_fire_systems_button)

        self.all_buttons_list.append(self.rooms_fire_systems_button)

        self.general_fire_systems_button = MDRectangleFlatIconButton( #MDFillRoundFlatIconButton
            text="General fire systems",
            icon_size="35dp",
            # width="35dp",
            # font_style='H6',
            icon=DBComms.get_icon(self.conn, "general_fire_systems", "general"),
            # pos_hint={'center_x': .5, 'center_y': .5},
            #valign="center", #['top', 'center', 'bottom']
            #on_release=self.switch_state,
            text_color=self.universal_text_color  # Set a non-transparent color for the text
        )
        self.general_fire_systems_button.on_release=lambda: self.manage_states(self.general_fire_systems_button, "general_fire_systems", "general")
        self.general_circular_layout.add_widget(self.general_fire_systems_button)

        self.all_buttons_list.append(self.general_fire_systems_button)

        self.general_main_lights_button = MDRectangleFlatIconButton( #MDFillRoundFlatIconButton
            text="house main lights",
            icon_size="35dp",
            # width="35dp",
            # font_style='H6',
            icon=DBComms.get_icon(self.conn, "general_main_lights", "general"),
            # pos_hint={'center_x': .5, 'center_y': .5},
            #valign="center", #['top', 'center', 'bottom']
            #on_release=self.switch_state,
            text_color=self.universal_text_color  # Set a non-transparent color for the text
        )
        self.general_main_lights_button.on_release=lambda: self.manage_states(self.general_main_lights_button, "general_main_lights", "general")
        self.general_circular_layout.add_widget(self.general_main_lights_button)

        self.all_buttons_list.append(self.general_main_lights_button)

        self.general_rgb_tapelights_button = MDRectangleFlatIconButton( #MDFillRoundFlatIconButton
            text="rgb tapelights",
            icon_size="35dp",
            # width="35dp",
            # font_style='H6',
            icon=DBComms.get_icon(self.conn, "general_rgb_tapelights", "general"),
            # pos_hint={'center_x': .5, 'center_y': .5},
            #valign="center", #['top', 'center', 'bottom']
            #on_release=self.switch_state,
            text_color=self.universal_text_color  # Set a non-transparent color for the text
        )
        self.general_rgb_tapelights_button.on_release=lambda: self.manage_states(self.general_rgb_tapelights_button, "general_rgb_tapelights", "general")
        self.general_circular_layout.add_widget(self.general_rgb_tapelights_button)

        self.all_buttons_list.append(self.general_rgb_tapelights_button)

        self.house_kitchen_lights_button = MDRectangleFlatIconButton( #MDFillRoundFlatIconButton
            text="house kitchen lights",
            icon_size="35dp",
            # width="35dp",
            # font_style='H6',
            icon=str(DBComms.get_icon(self.conn, "house_kitchen_lights", "general")),
            # icon="toggle-switch-on",
            # pos_hint={'center_x': .5, 'center_y': .5},
            #valign="center", #['top', 'center', 'bottom']
            #on_release=self.switch_state,
            text_color=self.universal_text_color  # Set a non-transparent color for the text
        )
        self.house_kitchen_lights_button.on_release=lambda: self.manage_states(self.house_kitchen_lights_button, "house_kitchen_lights", "general")
        self.general_circular_layout.add_widget(self.house_kitchen_lights_button)

        self.all_buttons_list.append(self.house_kitchen_lights_button)

        self.general_windows_curtains_button = MDRectangleFlatIconButton( #MDFillRoundFlatIconButton
            text="Windows / Curtains",
            icon_size="35dp",
            # width="35dp",
            # font_style='H6',
            # icon=DBComms.get_icon(self.conn, "general_windows_curtains", "general"),
            # pos_hint={'center_x': .5, 'center_y': .5},
            #valign="center", #['top', 'center', 'bottom']
            #on_release=self.switch_state,
            text_color=self.universal_text_color  # Set a non-transparent color for the text
        )
        # self.general_windows_curtains_button.on_release=lambda: self.manage_states(self.general_windows_curtains_button, "general_windows_curtains", "general")
        self.general_circular_layout.add_widget(self.general_windows_curtains_button)

        # self.all_buttons_list.append(self.general_windows_curtains_button)

        self.house_backdoor_button = MDRectangleFlatIconButton( #MDFillRoundFlatIconButton
            text="Backdoor",
            icon_size="35dp",
            # width="35dp",
            # font_style='H6',
            icon=DBComms.get_icon(self.conn, "house_backdoor", "general"),
            # pos_hint={'center_x': .5, 'center_y': .5},
            #valign="center", #['top', 'center', 'bottom']
            #on_release=self.switch_state,
            text_color=self.universal_text_color  # Set a non-transparent color for the text
        )
        self.house_backdoor_button.on_release=lambda: self.manage_states(self.house_backdoor_button, "house_backdoor", "general")
        self.general_circular_layout.add_widget(self.house_backdoor_button)

        self.all_buttons_list.append(self.house_backdoor_button)

        self.house_frontdoor_button = MDRectangleFlatIconButton( #MDFillRoundFlatIconButton
            text="Frontdoor",
            icon_size="35dp",
            # width="35dp",
            # font_style='H6',
            icon=DBComms.get_icon(self.conn, "house_frontdoor", "general"),
            # pos_hint={'center_x': .5, 'center_y': .5},
            #valign="center", #['top', 'center', 'bottom']
            #on_release=self.switch_state,
            text_color=self.universal_text_color  # Set a non-transparent color for the text
        )
        self.house_frontdoor_button.on_release=lambda: self.manage_states(self.house_frontdoor_button, "house_frontdoor", "general")
        self.general_circular_layout.add_widget(self.house_frontdoor_button)

        self.all_buttons_list.append(self.house_frontdoor_button)

        self.general_screen.add_widget(
            self.general_label
        )

        self.general_screen.add_widget(self.general_circular_layout)

        self.main_swiper.add_widget(
            MDSwiperItem(self.general_screen)
        )

    #seting widgets
    def settings_widgets(self):

        self.settings_screen = MDScreen()

        self.settings_screen.add_widget(
            MDTopAppBar(
                title="Settings",
                anchor_title= "left",
                right_action_items = [["chevron-double-up", #"dots-vertical"
                    #lambda x: app.callback()
                    ]],
                pos_hint={'center_x': .5, 'center_y': .95},
                )
        )

        self.settings_screen.add_widget(MDLabel(
            text="Settings",
            halign="center",
            # valign="center",
            font_style="H1",
            # font_size="50px",
            pos_hint={'center_x': .5, 'center_y': .6},
            opacity=0.3,
            text_color=self.universal_text_color  # Set a non-transparent color for the text
        ))

        self.main_swiper.add_widget(
            MDSwiperItem(self.settings_screen)
        )

        



        
    #main build func------------------------
    def build(self):


        self.all_buttons_list = []

        self.conn = DBComms.init_connection(database)

        self.timeout_bool = False
        self.timeout_var = 0
        self.command = True
        self.timeout_default = 5

        self.theme_palletes = ['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 
        'Blue', 'LightBlue', 'Cyan', 'Teal',
        'Green', 'LightGreen', 'Lime', 'Yellow', 
        'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']


        self.theme_cls.theme_style = "Dark"
        # self.theme_cls.theme_style = "Dark"
        # self.theme_cls.primary_palette = "Blue"
        # self.theme_cls.accent_palette = "Amber"

        self.random_theme = random.choice(self.theme_palletes)
        print(f"using primary pallete theme: {self.random_theme}")
        self.theme_cls.primary_palette = self.random_theme
        
        self.random_theme = random.choice(self.theme_palletes)
        print(f"using accent pallete theme: {self.random_theme}")
        self.theme_cls.accent_palette = self.random_theme

        self.icon = "images/logo25.png"

         
    

        #main swipper, to hold screens
        self.main_swiper = MDSwiper(
            #fit_mode = 'fill', #['scale-down', 'fill', 'contain', 'cover']
            #bar_margin = 0,
            # allow_stretch = True,w
            # always_overscroll = True,
            # size_hint_y = 1,
            size_hint_x = .96,
            # bar_color = (1, 1, .7, 1),
            # viewport_size = (.97, .5),
            # bar_inactive_color = (.1, .7, .1, 1),
        )



        self.load_appliances_widgets()

        

        self.settings_widgets()

        #self.screen_manager = MDScreenManager()
        """
        for gridlayout the orientation must be 
         ['lr-tb', 'tb-lr', 'rl-tb', 'tb-rl', 'lr-bt', 'bt-lr', 'rl-bt', 'bt-rl']
        """
        


        return self.main_swiper
        # return self.screen_manager
if __name__ == "__main__":
    # observer = Observer()
    # event_handler = MyEventHandler()
    # observer.schedule(event_handler, ".", recursive=True)  # Watch current directory
    # observer.start()
    Home_Automation().run()
    # observer.join()

# Home_Automation().run()
# hotreloader(Home_Automation())

