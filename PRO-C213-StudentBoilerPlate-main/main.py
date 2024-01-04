from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

import socket
from  threading import Thread
import json


SERVER = None
PORT  = 8000
IP_ADDRESS  = None
remote_mouse = None
sm = None

class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(FirstWindow(name='first'))
        self.add_widget(SecondWindow(name='second'))



class FirstWindow(Screen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            self.layout = FloatLayout()

            self.isConnected  = False

            #-------------------- Label-----------------
            self.ipLabel = Label(
                text="REMOTE MOUSE",
                font_size=60,
                pos_hint={ "x" : 0.03, "y":0.4},
                color=(255, 165, 0))

            self.add_widget(self.ipLabel)

            #---------------------------------------------


            #----------------------textinput------------------

            self.ipInput = TextInput(
                    text="",
                    size_hint=(0.65, 0.15),
                    font_size=50,
                    pos_hint={ "x" : 0.2, "y" : 0.65},
                    multiline=False,
                    halign= 'center',
                    hint_text = "IP Address",
                    padding_y= (13, 0))

            self.add_widget(self.ipInput)

            #-------------------------------------------------


            # ------------------Submit Button----------

            self.submitBttn = Button(
                text="Connect With PC",
                size_hint = (0.35, 0.15),
                font_size = 30,
                pos_hint = { "x" : 0.35, "y" : 0.45},
                background_color= (255,112,67),
                background_down= "#ffcc80")

            self.submitBttn.bind(on_press=self.onSubmitPress)

            self.add_widget(self.submitBttn)

            # -------------------------------------------


            #----------------------- Popup ---------

            self.popupButton = Button(
                text="",
                halign="center",
                font_size=18,
                background_color=(251,140,0),
                background_down= "#ffcc80")

            self.submitPopup = Popup(
                title='Remote Mouse',
                content= self.popupButton,
                size_hint=(None, None), size=(400, 400))

            self.popupButton.bind(on_press=self.changeScreen)

            #--------------------------------

        # ------------------- Handling Onpress --------------

        def onSubmitPress(self, elem):

            global IP_ADDRESS

            IP_ADDRESS = self.ipInput.text.strip()

            connection = setup()

            if(connection):
                self.isConnected = True
                self.submitPopup.content.text = f"Successfully connected with \n{self.ipInput.text}\nclick to continue."
                self.submitPopup.open()
            else:
                self.isConnected = False
                self.submitPopup.content.text = f"Oops!!!\nEnter Valid IP Address"
                self.submitPopup.open()

        def changeScreen(self, elem):
            if(self.isConnected ):
                global sm
                self.submitPopup.dismiss()
                screens = sm.screens
                sm.switch_to(screens[1])
            else:
                self.submitPopup.dismiss()

        #--------------------------------





class SecondWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout  = FloatLayout()

        self.lb1 = Label(text="REMOTE MOUSE", font_size=60, color=(255, 165, 0), pos_hint = {"x":0, "y":0.4})
        self.add_widget(self.lb1)

        self.leftClick = Button(text="LEFT CLICK", size_hint=(0.5,0.2), background_color=(255, 165, 0),bold=100)
        self.add_widget(self.leftClick)

        self.rightClick = Button(
            text="RIGHT CLICK",
            size_hint=(0.5,0.2),
            background_color=(255, 165, 0),
            pos_hint={"x":0.5, "y":0}, bold=100)
        self.add_widget(self.rightClick)

        self.trackPad = Button(
            text="TRACKPAD",
            size_hint =(1, 0.6),
            background_color=(255, 165, 0),
            pos_hint= {"x":0, "y":0.2}
        )

        self.add_widget(self.trackPad)

    def on_touch_down(self, touch):
        global SERVER
        # Clicking Left Button
        if((touch.spos[0] > 0 and touch.spos[0] <=0.5)  and (touch.spos[1] > 0 and touch.spos[1] <=0.20) ):
            self.leftClick.opacity = 0.5
            data = json.dumps({ "data"  : "left_click", "type" : "click"})
            SERVER.send(data.encode())

        # Clicking Right Button
        if((touch.spos[0] > 0.5 and touch.spos[0] <=1)  and (touch.spos[1] > 0 and touch.spos[1] <=0.20) ):
            self.rightClick.opacity = 0.5
            data = json.dumps({ "data"  : "right_click", "type" : "click"})
            SERVER.send(data.encode())



    def on_touch_move(self, touch):
        global SERVER
        if((touch.spos[0] > 0 and touch.spos[0] <=1)  and (touch.spos[1] > 0.20 and touch.spos[1] <=0.80) ):
            data = json.dumps({ "data"  : touch.spos, "type" : "move"})
            SERVER.send(data.encode())





    def on_touch_up(self, touch):
        # Clicking Left Button
        if((touch.spos[0] > 0 and touch.spos[0] <=0.5) and (touch.spos[1] > 0 and touch.spos[1] <=0.20)):
            self.leftClick.opacity = 1



        # Clicking Right Button
        if((touch.spos[0] > 0.5 and touch.spos[0] <=1)  and (touch.spos[1] > 0 and touch.spos[1] <=0.20) ):
            self.rightClick.opacity = 1


class RemoteMouse(App):
    def build(self):
        global sm
        sm =  ScreenManager()
        sm.add_widget(FirstWindow(name='first'))
        sm.add_widget(SecondWindow(name='second'))
        return sm




def setup():
    global SERVER
    global PORT
    global IP_ADDRESS
    global remote_mouse

    try:
        SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SERVER.connect((IP_ADDRESS, PORT))
        return True
    except:
        return False



def main():
    remote_mouse = RemoteMouse().run()

if __name__ == '__main__':
    main()
