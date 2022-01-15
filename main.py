# import module
from email.mime import audio
import time
from tkinter import END
from tkinter.constants import N
from tkinter.messagebox import showinfo
from tkinter.simpledialog import askstring
from winsound import PlaySound
import requests
from bs4 import BeautifulSoup
from playsound import playsound
from datetime import datetime
import tkinter as tk

SLEEPTIME = 60000  # milliseconds
server_id = "1495246"
server = "https://refactor.jp/chivalry/?serverId="
searching = True
name = "Sandclusterfck 1.X in Finland"


def check_players():
    global players
    htmldata = get_data(server+server_id)
    soup = BeautifulSoup(htmldata, 'html.parser')
    get_server_name(soup)
    for data in soup.find_all("tt"):
        players = data.get_text()[1:3]
        if players[1:2] == "/":
            players = players[0:1]
    return int(players)


def get_server_name(soup):
    global name
    for data in soup.find_all("h2"):        
        name = data.get_text()


def restart_server():
    global searching
    searching = True
    txt_edit.delete(1.0, END)
    check_server()


def check_server():
    while searching:
        try:
            update()
            return
            # To handle exceptions
        except:
            return txt_edit.insert(tk.END, get_time() + " " + "Wrong ID or connection issues \n")

def get_time():
    now = datetime.now()
    return now.strftime("%H:%M:%S")


# link for extract html data
def get_data(url):
    r = requests.get(url)
    return r.text


def stop():
    global searching
    searching = False
    window.title("Check Chiv Server: " + server_id)
    btn_open.config(text="Run Search", command=restart_server)
    txt_edit.insert(tk.END, get_time() + " " + "Stopped search \n")
    txt_edit.see(tk.END)


def update():
    window.title("Searching: " + server_id + " " + name)
    btn_open.config(text="Stop", command=stop)
    if check_players() > 1:
        txt_edit.insert(tk.END, get_time() + " " + players + " players online\n")
        playsound('audio.mp3', False)
    elif check_players() == 1:
        txt_edit.insert(tk.END, get_time() + " " + players + " player online\n")
        playsound('audio.mp3', False)
    else:
        txt_edit.insert(tk.END, get_time() + " Nobody is playing on this server" + "\n")  
    txt_edit.see(tk.END) #keep scolling to END in window
    window.after(SLEEPTIME, check_server)  # run  again after xxx ms


def showinfo():
    global server_id
    server_id = askstring('serverId', 'Change Id here')
    if server_id:
        window.title("Check Chiv Server: " + server_id)


window = tk.Tk()
window.title("Check Chiv Server: " + server_id)

window.geometry("450x100")
window.rowconfigure(0, minsize=200, weight=1)
window.columnconfigure(1, minsize=300, weight=1)

scrollbar = tk.Scrollbar(window)
label = tk.Label(window)
txt_edit = tk.Text(window)
fr_buttons = tk.Frame(window)
btn_open = tk.Button(fr_buttons, text="Run Search", command=check_server)
btn_save = tk.Button(fr_buttons, text="Change Server", command=showinfo)

window.rowconfigure(0, minsize=100, weight=1)
btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5)
fr_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")
scrollbar.grid(row=0, column=3, rowspan=2,  sticky="nsew")
label.grid(row=2, column=1, sticky="nsew")

txt_edit.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=txt_edit.yview)

window.mainloop()
