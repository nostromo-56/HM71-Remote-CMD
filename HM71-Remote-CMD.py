#!/usr/bin/env python

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import font
import telnetlib
from heapq import merge
import time
import functools
import configparser
import os
import platform
import subprocess

# Parameters
#MyDebug = True  #False #
HOST            = ""
BoxLine         = 1000
myVOL           = ""
tn              = ""
fp              = functools.partial
RowsTally       = 0
NextStartFrom   =""
selNEWpage      = 0
Ini_File        = os.path.dirname(os.path.realpath(__file__))+"/HM71-Remote-CMD.ini"
BotElSize       = 80
Space01         = 46
VolWidth        = 8
MsgSspace       = 0
Vol_Bar_Color_f = "green"
Vol_Bar_Color_b = "#f0f0f0"


# =================================================== SOUBROUTINES ========================================= * START

def clicked():
    label3.configure(text="Function not yet implemented",fg="white",bg='red')

def CallBack():
   msg=messagebox.showinfo( "Warning", "If the configuration file was updated, restart the program")

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

def _on_mousewheel(event, scroll=None):            ######### Mousewheel
    os = platform.system()
    if os == 'Windows':
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    elif os == 'Darwin':
        canvas.yview_scroll(int(-1 * event.delta), "units")
    else:
        canvas.yview_scroll(int(scroll), "units")

def _bind_to_mousewheel(event):
    os = platform.system()
    if os == 'Windows':
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    elif os == 'Darwin':
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    else:
        canvas.bind_all("<Button-4>", fp(_on_mousewheel, scroll=-1))
        canvas.bind_all("<Button-5>", fp(_on_mousewheel, scroll=1))

def _unbind_from_mousewheel(event):
    os = platform.system()
    if os == 'Windows':
        canvas.unbind_all("<MouseWheel>")
    elif os == 'Darwin':
        canvas.unbind_all("<MouseWheel>")
    else:
        canvas.unbind_all("<Button-4>")
        canvas.unbind_all("<Button-5>")


def Selected(myX, myY, selNEWpage):                        ######### Select Line of Box
    def wrapper(x=myX, y=myY):
        global selNEWpage
        if MyDebug:
            print("Selected",myX, myY, selNEWpage)
        if myX == 0 or myX > RowsTally:
            pass
        elif myX == 999:                                ############# More than 1000 element in list
            Diplay_GT999()
            return x+y
        elif  IPT_Selected [:4] == "FN02":               ############# Turner
            LineSel = QueryCMD(str(myX).zfill(2)+"PR")
            Diplay()
            return x+y
        else:                                            #############  Music_srv Int_Radio USB Ipod Favorites
            LineSel = QueryCMD(str(myX+selNEWpage).zfill(5)+"GHP")
            Diplay()
            return x+y
    return wrapper

################################################### Display Box management

def Box_on_top():
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

def progressbar():
    progress_bar.step(30)
    root.update()
    
def progressbar_end():
    progress_bar.stop()
    progress_bar['value'] = 100
    progress_bar.update()
    time.sleep(0.5)
    progress_bar['value'] = 0

def TurnerRows():
    global RowsTally
    TurnerRows_list = ["Turner Preselect"]
    buttons[0][0].configure(text="[Turner Preset]")
    RowsTally = 30
    for i in range(1,31):
        buttons[i][0].configure(text="Preselect "+str(i).zfill(2) + Turner_PRE_lst[i-1])
    label3.configure(text=MsgSspace*" "+"")
def CDRows():
    global RowsTally
    Clean_Box()
    #TurnerRows_list = ["CD"]
    buttons[0][0].configure(text="[CD]")
    buttons[2][0].configure(text="To play CD use Botton:")
    buttons[3][0].configure(text="[Stop]  [Play]  [Pause]  [Prev]  [Next]")
    RowsTally = 0
    progressbar_end()

def AudioINRows():
    global RowsTally
    Clean_Box()
    buttons[0][0].configure(text="[Audio IN]")
    RowsTally = 0

def LineRows():
    global RowsTally
    Clean_Box()
    buttons[0][0].configure(text="[Line]")
    RowsTally = 0

def Music_srv_song(MY_list):
    global RowsTally
    EmptyToRemove = ['GEP01020""\r\n', 'GEP02021""\r\n', 'GEP03022""\r\n', \
                     'GEP04026""\r\n', 'GEP04026"----"\r\n', 'GEP06029"--kbps"\r\n', \
                     'GEP05028""\r\n', 'GEP07023"0:00"\r\n']
    for ToRemove in EmptyToRemove:
        if ToRemove in MY_list:
            MY_list.remove(ToRemove)
    Info_Song    = ExtractLine(new_response_list, 'GEP01020')
    Info_Artist  = ExtractLine(new_response_list, 'GEP02021')
    Info_Album   = ExtractLine(new_response_list, 'GEP03022')
    Info_Format  = ExtractLine(new_response_list, 'GEP04026')
    Info_Speed   = ExtractLine(new_response_list, 'GEP06029')
    Info_Speed01 = ExtractLine(new_response_list, 'GEP05028')
    Info_Speed02 = ExtractLine(new_response_list, 'GEP06027')
    Info_Timer   = ExtractLine(new_response_list, 'GEP07023')
    Clean_Box()
    buttons[1][0].configure(text=(Info_Song.strip()[9:-1]))
    buttons[3][0].configure(text=(Info_Artist.strip()[9:-1]))
    buttons[5][0].configure(text=(Info_Album.strip()[9:-1]))
    buttons[7][0].configure(text=(Info_Format.strip()[9:-1]     \
                            + " " + Info_Speed.strip()[9:-1]    \
                            + " " + Info_Speed01.strip()[9:-1]  \
                            + " " + Info_Speed02.strip()[9:-1] ))
    buttons[8][0].configure(text=(Info_Timer.strip()[9:-1]))
    RowsTally = 9

def Int_Radio_song(MY_list):
    global RowsTally
    EmptyToRemove = ['GEP02020""\r\n', 'GEP01032""\r\n', 'GEP06029"--kbps"\r\n']
    for ToRemove in EmptyToRemove:
        if ToRemove in MY_list:
            MY_list.remove(ToRemove)
    Info_Song    = ExtractLine(new_response_list, 'GEP01032')
    Info_Station = ExtractLine(new_response_list, 'GEP02020')
    Info_Speed   = ExtractLine(new_response_list, 'GEP06029')
    Clean_Box()
    buttons[1][0].configure(text=(Info_Song.strip()[9:-1]))
    buttons[3][0].configure(text=(Info_Station.strip()[9:-1]))
    buttons[6][0].configure(text=(Info_Speed.strip()[9:-1]))
    RowsTally = 7

def Diplay_GT999(): #
    global NextStartFrom, selNEWpage
    progressbar()
    response_list = QueryCMD("?GAP")
    ele2start  = NextStartFrom [:8][3:]
    ListNEle   = ExtractLine(response_list, 'GDP')[13:-2]
    progressbar()
    response_list_All = QueryCMD(ele2start+ListNEle+"GIA")
    Menu_range = len(response_list_All)
    Clean_Box()
    RowsTally=0                          #### load box buttons
    Box_on_top()
    selNEWpage = int(ele2start)-1
    buttons[0][0].configure(text=("[ continuation... ]"))
    if Menu_range > 1000:
        buttons[999][0].configure(text="[Select for the next entries]")
        NextStartFrom = response_list_All[998]
    for i in range(0,Menu_range):
        if  response_list_All [i] [:3]   == 'GIB':
            RowsTally=RowsTally+1
            if RowsTally < 999:
                buttons[RowsTally][0].configure(text=(response_list_All[i].strip()[16:-1] ))
    progressbar_end()

def Diplay(): #
    global IPT_Selected, new_response_list, RowsTally, NextStartFrom, selNEWpage

    progressbar()
    #root.update()
    label3.configure(text="",fg="black",bg='gray')
    selNEWpage = 0
    response_list   = QueryCMD("?F")
    IPT_Selected    = ExtractLine(response_list, 'FN')
    Select_Bottons()
    if  IPT_Selected [:4] == "FN02":    # Turner
        TurnerRows()
        Box_on_top()
        progressbar_end()
        return
    if  IPT_Selected [:4] == "FN01":    # CD
        CDRows()
        Box_on_top()
        return
    if  IPT_Selected [:4] == "FN51":    # AudioIN
        AudioINRows()
        Box_on_top()
        return
    if  IPT_Selected [:4] == "FN52":    # Line
        LineRows()
        Box_on_top()
        return
    response_list   = QueryCMD("?GAP")
    new_response_list = list(set(response_list))
    Box_on_top()
    if 'GEP01000' in ExtractLine(new_response_list, 'GEP01000') :
        #Return()
        response_list   = QueryCMD("?GAP")
    progressbar()
    if 'GEP01032' in ExtractLine(new_response_list, 'GEP01032') or \
       'GEP04026' in ExtractLine(new_response_list, 'GEP04026') :      ## Int_Radio  & Music_srv     ##### Found song detail
        label3.configure(text=MsgSspace*" "+"Click on info rows to refresh the screen")
        if  IPT_Selected [:4] in "FN44,FN17,FN50":  # Media Server , USB , Ipod
            Music_srv_song(new_response_list)
        elif IPT_Selected [:4] in "FN38,FN45":      # Netradio , Favorites
            Int_Radio_song(new_response_list)
            while True:
                if len([l_row for l_row in new_response_list if 'GEP01032' in l_row]) + \
                    len([l_row for l_row in new_response_list if 'GEP02020' in l_row]) == 0 :
                    response_list = QueryCMD("?GAP")
                    new_response_list = list(set(response_list))
                    Int_Radio_song(new_response_list)
                else:
                    break
    else:                                                   ########## Found menu #########
        response_list_All = QueryCMD("?GAP")                      #### List Info
        Menu_title = ExtractLine(response_list_All, 'GCP01').strip()[11:-1]
        ListNEle   = ExtractLine(response_list_All, 'GDP')[13:-2]
        response_list_All = QueryCMD("00001"+ListNEle+"GIA")      #### List Info
        Clean_Box()                                               #### arrange box buttons
        Menu_range = len(response_list_All)
        if len(Menu_title) == 0:
            Menu_title = "Top Menu"
        buttons[0][0].configure(text=("["+Menu_title+"]"))

        RowsTally=0                          #### load box buttons
        if Menu_range > 1000:
            buttons[999][0].configure(text="[Select for the next entries]")
            NextStartFrom = response_list_All[998]
        for i in range(0,Menu_range):
            if  response_list_All [i] [:3]   == 'GIB':
                RowsTally=RowsTally+1
                if RowsTally < 999:
                    buttons[RowsTally][0].configure(text=(response_list_All[i].strip()[16:-1] ))
    progressbar_end()

def Clean_Box(): #
    for i in range(BoxLine):
        buttons[i][0].configure(text=(""))

def Start_Display():
    #progress_bar.step(30)
    Volume("STATUS")
    root.update()
    On_OffSwitch("STATUS")
    root.update()
    MuteStatus()
    root.update()
    label2.configure(text=HOST + " is connected")
    root.update()
    Diplay()

################################################### NET management

def Connect(): # Net connect
    progressbar()
    Connect.configure(fg="white",bg='black')
    Disconnect.configure(fg="black",bg='#f0f0f0')
    global myVOL, tn #, HOST
    try:
       tn = telnetlib.Telnet(HOST,PORT,120)
    except:
        if MyDebug:
            print("EOFerror: telnet not connected")
            is_connected()
            Connect.configure(fg="black",bg='#f0f0f0')
            Disconnect.configure(fg="white",bg='red')
            #root.mainloop()
            return
    # if MyDebug:
    #     tn.set_debuglevel(9)
    Start_Display()

def Disconnect(): # Net disconnect
    if not is_connected():
        return
    Connect.configure(fg="black",bg='#f0f0f0')
    Disconnect.configure(fg="white",bg='red')
    tn.close()
    label2.configure(text="")
    label3.configure(text=MsgSspace*" "+HOST + " disconnected")
    Clean_Box()
    Clean_All_Bottons()
    label_volume.config(text="")

def QueryCMD(MyCMD):           # Send command to XM* Telnet server and receive response
    if not is_connected():
        return([])
    if "GIA" in MyCMD:
        myTimeout = 3
    else:
        myTimeout = 1
    MyToDo = MyCMD + "\r\n"
    tn.write(MyToDo.encode('ascii'))
    responseX = " "
    responseX_list = []
    while len(responseX) > 0 :
        responseX = (tn.read_until(b'\n', timeout = myTimeout))
        responseX_list.append(responseX.decode("utf-8",errors='replace')) #
    if MyDebug:
        print("QueryCMD", MyCMD, myTimeout, responseX_list)
    return(responseX_list)

def ExtractLine(responseY_list, MyString):
    if not is_connected():
        return("")
    Str_Return = ""
    for i in range(len(responseY_list)):
            try:
                responseY_list[i].index(MyString)
                Str_Return = responseY_list [i]
                if MyDebug:
                    print("ExtractLine",i,Str_Return)
                break
            except ValueError:
                pass
    return(Str_Return)

def is_connected():
    try:
        tn.read_very_eager()
        return True
    except: # EOFError:
        label3.configure(text=MsgSspace*" "+"ERROR : Pioneer DEVICE is NOT connected, or impossible connect to it !!!!!", fg="white" ,bg='red')
        if MyDebug:
            if MyDebug:
                print("EOFerror: telnet connection is closed")
        return False

###################################################  Volume and Audio management
def VolUp():
    Volume("UP")

def VolDown():
    Volume("DOWN")

def Volume(MYcmd):
    MyToDo = ""
    if MYcmd   == "UP":
         MyToDo = "VU"
    elif MYcmd == "DOWN":
         MyToDo = "VD"
    elif MYcmd == "STATUS":
         MyToDo = "?V"
    response_list = QueryCMD(MyToDo)
    if len(response_list) > 0:
       myVOL = int(ExtractLine(response_list, 'VOL') [3:])
       label_volume.config(text=str(myVOL))

def Mute():
    MuteSwitch("OnOff")

def MuteStatus():
    MuteSwitch("STATUS")

def MuteSwitch(MYcmd): # Mute ON OFF
    response_list = QueryCMD("?M")
    myMUTE = ExtractLine(response_list, 'MUT')
    if MYcmd == "STATUS":
        if myMUTE [:4] == "MUT0":
            Mute.configure(fg="white",bg='black')
        else: # MUT0
            Mute.configure(fg="black",bg='#f0f0f0')
    elif myMUTE [:4] == "MUT1":
        Mute.configure(fg="white",bg='black')
        QueryCMD("MO")
    else: # MUT0
        Mute.configure(fg="black",bg='#f0f0f0')
        QueryCMD("MF")

###################################################  POWER management
def On_Off():
    On_OffSwitch("OnOff")

def On_OffStatus():
    On_OffSwitch("STATUS")

def On_OffSwitch(MYcmd): # standbay ON OFF
    response_list = QueryCMD("?P")
    myOn_Off = ExtractLine(response_list, 'PWR')
    if MYcmd == "STATUS":
        if myOn_Off [:4] == "PWR0":
            On_Off.configure(fg="black",bg='#f0f0f0')
        else: # PWR2
            On_Off.configure(fg="white",bg='red')
    elif myOn_Off [:4] == "PWR0":
        On_Off.configure(fg="white",bg='red')
        QueryCMD("PF")     #POWER OFF
    else: # PWR2
        On_Off.configure(fg="black",bg='#f0f0f0')
        QueryCMD("PO")     #POWER ON
        Start_Display()

###################################################  Button management

def Option(): # Option
    subprocess.run([Ini_editor, Ini_File])
    CallBack()

def Prev(): # Skip Prev
    if IPT_Selected [:4] == "FN01":
        QueryCMD("12CDP")
        QueryCMD("12CDP")
    else:
        QueryCMD("12PB")
        QueryCMD("12PB")
        Diplay()

def Next(): # Skip Next
    if IPT_Selected [:4] == "FN01":
        QueryCMD("13CDP")
    else:
        QueryCMD("13PB")
        time.sleep(3)
        Diplay()

def Return(): # Return
    response_list_All = QueryCMD("?GAP")
    if len(ExtractLine(response_list_All, 'GEP06029') + \
           ExtractLine(response_list_All, 'GEP04026') ) > 0 : # is playing
        label3.configure(text=MsgSspace*" "+"To return to the previous list press the [Stop] button",fg="white",bg='red')
        return
    QueryCMD("31PB")
    Diplay()

def Pause(): # Pause
    if IPT_Selected [:4] in "FN02,FN38,FN45":      # Netradio , Favorites, Turner
        return
    Pause.configure(fg="white",bg='black')
    if IPT_Selected [:4] == "FN01":
        QueryCMD("11CDP")
    else:
        QueryCMD("11PB")
        Diplay()

def Play(): # Play
    if IPT_Selected [:4] in "FN02,FN38,FN45":      # Netradio , Favorites, Turner
        return
    Pause.configure(fg="black",bg='#f0f0f0')
    if IPT_Selected [:4] == "FN01":
        QueryCMD("10CDP")
    else:
        QueryCMD("10PB")
        Diplay()

def Stop(): # Stop
    if IPT_Selected [:4] == "FN01":
        QueryCMD("20CDP")
    else:
        QueryCMD("20PB")
        Diplay()

def Music_srv(): # Music Sever
    QueryCMD("44FN")
    Clean_All_Bottons()
    Music_srv.configure(fg="white",bg='black')
    Diplay()

def Int_Radio(): # Web Radio
    QueryCMD("38FN")
    Clean_All_Bottons()
    Int_Radio.configure(fg="white",bg='black')
    Diplay()

def Turner(): # Turner
    QueryCMD("02FN")
    Clean_All_Bottons()
    Turner.configure(fg="white",bg='black')
    TurnerRows()

def CD(): # CD
    QueryCMD("01FN")
    Clean_All_Bottons()
    CD.configure(fg="white",bg='black')
    CDRows()

def USB(): # USB
    QueryCMD("17FN")
    Clean_All_Bottons()
    USB.configure(fg="white",bg='black')
    Diplay()

def Ipod(): # Ipod
    QueryCMD("50FN")
    Clean_All_Bottons()
    Ipod.configure(fg="white",bg='black')
    Diplay()

def Favorites(): # Favorites
    QueryCMD("45FN")
    Clean_All_Bottons()
    Favorites.configure(fg="white",bg='black')
    Diplay()

def AudioIN(): # AudioIN
    QueryCMD("51FN")
    Clean_All_Bottons()
    AudioIN.configure(fg="white",bg='black')
    AudioINRows()

def Line(): # Line
    QueryCMD("52FN")
    Clean_All_Bottons()
    Line.configure(fg="white",bg='black')
    LineRows()

def Clean_All_Bottons(): #
    Ipod.configure(fg="black",bg='#f0f0f0')
    USB.configure(fg="black",bg='#f0f0f0')
    CD.configure(fg="black",bg='#f0f0f0')
    Music_srv.configure(fg="black",bg='#f0f0f0')
    Int_Radio.configure(fg="black",bg='#f0f0f0')
    Favorites.configure(fg="black",bg='#f0f0f0')
    Turner.configure(fg="black",bg='#f0f0f0')
    AudioIN.configure(fg="black",bg='#f0f0f0')
    Line.configure(fg="black",bg='#f0f0f0')
    On_Off.configure(fg="black",bg='#f0f0f0')

def Select_Bottons(): # set reverse color  input selected botton
    global IPT_Selected
    input_srv = IPT_Selected
    if  input_srv [:4] == "FN02": # Turner
        Turner.configure(fg="white",bg='black')
    elif  input_srv [:4] == "FN44": # Media Server
        Music_srv.configure(fg="white",bg='black')
    elif input_srv [:4] == "FN38": # Netradio
        Int_Radio.configure(fg="white",bg='black')
    elif input_srv [:4] == "FN01": # Netradio
        CD.configure(fg="white",bg='black')
    elif input_srv [:4] == "FN51": # AudioIN
        AudioIN.configure(fg="white",bg='black')
    elif input_srv [:4] == "FN52": # Line
        Line.configure(fg="white",bg='black')
    elif input_srv [:4] == "FN17": # USB
        USB.configure(fg="white",bg='black')
    elif input_srv [:4] == "FN50": # Ipod
        Ipod.configure(fg="white",bg='black')
    elif input_srv [:4] == "FN45": # Favorites
        Favorites.configure(fg="white",bg='black')

# =================================================== SOUBROUTINES ========================================= * END

Config = configparser.RawConfigParser()                  # Get .ini data
Config.read(os.path.expanduser(Ini_File))
HOST = ConfigSectionMap("HM71")['HM71_HOST'.lower()].strip('"').strip("'")
PORT = ConfigSectionMap("HM71")['HM71_PORT'.lower()].strip('"').strip("'")
MyDebug_str = ConfigSectionMap("HM71")['HM71_DEBUG'.lower()].strip('"').strip("'")
Ini_editor = ConfigSectionMap("HM71_config")['HM71_Ini_editor'.lower()].strip('"').strip("'")

Turner_PRE_00 = Config.items( "HM71_Turner_PRE" )

MyDebug = True if MyDebug_str == "True" else False

Turner_PRE_lst = []                            ##### Turner Preselect Description
for x in range(30):
    Turner_PRE_lst.append("")
t=0
for key, Turn_PRE in Turner_PRE_00:
    Turner_PRE_lst [t] = " - "  + Turner_PRE_00[t][1].strip('"').strip("'")
    t=t+1

root = tk.Tk()
root.title("Pioneer HM71 Remote Commander")
root.grid_rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.resizable(width=False, height=False)

frame_main = tk.Frame(root, bg="gray")
frame_main.grid(sticky='news')

cf = font.Font(family="Liberation Sans", size=14) #, weight="bold"

label1 = tk.Label(frame_main, text="", bg="gray", fg="green",font=cf)
label1.grid(row=0, column=0, pady=(5, 0), sticky='nw', columnspan=10)
label2 = tk.Label(frame_main, text="", bg="gray", fg="white",anchor="center",width=80,font='Helvetica 12 bold')
label2.grid(row=1, column=0, pady=(5, 0), sticky='n', columnspan=10)
label3 = tk.Label(frame_main, text="", bg="gray", fg="white",anchor="center",width=80,font=cf)
label3.grid(row=3, column=0, pady=5, sticky='nw', columnspan=10)
label4 = tk.Label(frame_main, text=Space01*" "+"Run Progress ...", bg="gray",font=cf)
label4.grid(row=5, column=0, pady=8, sticky='nw', columnspan=10)

progress_bar = ttk.Progressbar(frame_main, orient="horizontal", mode="determinate", maximum=100, value=0)
progress_bar.grid(row=5, column=4, pady=8, sticky='nw', columnspan=10)

row00 = 0
Connect = tk.Button(frame_main, text="Connect", font=cf, command=Connect)
Connect.grid(column=1, row=row00, pady=3, sticky='nw', columnspan=10)
Disconnect = tk.Button(frame_main, text="Disconnect", fg="white",bg='red', font=cf, command=Disconnect)
Disconnect.grid(column=3, row=row00, pady=4, sticky='nw', columnspan=10)
Option = tk.Button(frame_main, text="Options", font=cf, command=Option)
Option.grid(column=5, row=row00, pady=5, sticky='nw', columnspan=10)
On_Off = tk.Button(frame_main, text="ON/OFF (NET standbay)", font=cf, command=On_Off)
On_Off.grid(column=6, row=row00, pady=5, sticky='nw', columnspan=10)

row01 = 4
Ipod = tk.Button(frame_main, text=" Ipod  ", font=cf, command=Ipod)
Ipod.grid(column=0, row=row01, sticky='ne')
USB = tk.Button(frame_main, text="USB", font=cf, command=USB)
USB.grid(column=1, row=row01, sticky='ne')
CD = tk.Button(frame_main, text="  CD  ", font=cf, command=CD)
CD.grid(column=2, row=row01, sticky='ne')
Music_srv = tk.Button(frame_main, text="Music Server", font=cf, command=Music_srv)
Music_srv.grid(column=3, row=row01, sticky='ne')
Int_Radio = tk.Button(frame_main, text="Internet Radio", font=cf, command=Int_Radio)
Int_Radio.grid(column=4, row=row01, sticky='ne')
Favorites = tk.Button(frame_main, text="Favorites", font=cf, command=Favorites)
Favorites.grid(column=5, row=row01, sticky='ne')
Turner = tk.Button(frame_main, text="Turner", font=cf, command=Turner)
Turner.grid(column=6, row=row01, sticky='ne')
AudioIN = tk.Button(frame_main, text="Audio IN", font=cf, command=AudioIN)
AudioIN.grid(column=7, row=row01, sticky='ne')
Line = tk.Button(frame_main, text=" Line ", font=cf, command=Line)
Line.grid(column=8, row=row01, sticky='ne')

row02 = 6
label_volume = tk.Label(frame_main, text=myVOL,bg=Vol_Bar_Color_b,fg=Vol_Bar_Color_f,anchor="center",width=VolWidth, font=cf)
label_volume.grid(column=0, row=row02, padx=64, pady=(5, 0), sticky='nw', columnspan=10) # 59
VolDown = tk.Button(frame_main, text="Vol -", font=cf, command=VolDown)
VolDown.grid(column=0, row=row02)
VolUp = tk.Button(frame_main, text="Vol +", font=cf, command=VolUp)
VolUp.grid(column=2, row=row02)
Mute = tk.Button(frame_main, text="Mute", font=cf, command=Mute)
Mute.grid(column=3, row=row02, sticky='nw', padx=3)
Return = tk.Button(frame_main, text="Return", font=cf, command=Return)
Return.grid(column=4, row=row02, sticky='nw')
Stop = tk.Button(frame_main, text="Stop", font=cf, command=Stop)
Stop.grid(column=4, row=row02, columnspan=2)
Play = tk.Button(frame_main, text="Play", font=cf, command=Play)
Play.grid(column=5, row=row02, sticky='ne')
Pause = tk.Button(frame_main, text="Pause", font=cf, command=Pause)
Pause.grid(column=6, row=row02, sticky='nw')
Prev = tk.Button(frame_main, text="Prev", font=cf, command=Prev)
Prev.grid(column=7, row=row02, sticky='ne')
Next = tk.Button(frame_main, text="Next", font=cf, command=Next)
Next.grid(column=8, row=row02, sticky='nw')


# Create a frame for the canvas with non-zero row&column weights
frame_canvas = tk.Frame(frame_main)
frame_canvas.grid(row=2, column=0, pady=(5, 0), sticky='nw', columnspan=10)
frame_canvas.grid_rowconfigure(0, weight=1)
frame_canvas.grid_columnconfigure(0, weight=1)
# Set grid_propagate to False to allow 5-by-5 buttons resizing later
frame_canvas.grid_propagate(False)

# Add a canvas in that frame
canvas = tk.Canvas(frame_canvas, bg="yellow")
canvas.grid(row=0, column=0, sticky="news")

# Link a scrollbar to the canvas
vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
vsb.grid(row=0, column=1, sticky='ns')
canvas.configure(yscrollcommand=vsb.set)

# Create a frame to contain the buttons
frame_buttons = tk.Frame(canvas, bg="blue")
canvas.create_window((0, 0), window=frame_buttons, anchor='nw')

# Add buttons to the frame
rows = BoxLine
columns = 1
boxrows = 10
buttons = [[tk.Button() for j in range(columns)] for i in range(rows)]
for i in range(0, rows):
    for j in range(0, columns):
        #buttons[i][j] = tk.Button(frame_buttons, text=("%d,%d" % (i+1, j+1)), width=80, command=clicked)
        buttons[i][j] = tk.Button(frame_buttons, text=(""), width=BotElSize, font=cf, command=Selected(i,j,selNEWpage)) # "xx" + "22", 'bold'
        buttons[i][j].grid(row=i, column=j, sticky='news')

# Update buttons frames idle tasks to let tkinter calculate buttons sizes
frame_buttons.update_idletasks()

# Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
first5columns_width = sum([buttons[0][j].winfo_width() for j in range(0, columns)])
first5rows_height = sum([buttons[i][0].winfo_height() for i in range(0, boxrows)])
frame_canvas.config(width=first5columns_width + vsb.winfo_width(),
                    height=first5rows_height)

# Set the canvas scrolling region
canvas.config(scrollregion=canvas.bbox("all"))

# Set Mousewheel scrolling region
canvas.bind('<Enter>', _bind_to_mousewheel)
canvas.bind('<Leave>', _unbind_from_mousewheel)

# Launch the GUI
root.mainloop()
