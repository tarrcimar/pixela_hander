import requests
import datetime
import sys
from tkinter import *
from PIL import ImageTk, Image
import webbrowser
import time

USERNAME = ""
TOKEN = ""
GRAPHID = ""

ARGS = sys.argv
LENGTH = len(ARGS)

ORIGINAL_ENDPOINT = 'https://pixe.la/v1/users'

COLORS = {
    "shibafu":"green",
    "momiji":"red",
    "sora":"purple",
    "ichou":"yellow",
    "ajisai":"purple",
    "kuro":"orange"
}

FONT = ("Corbel", 12, "bold")
color = ""
OPTIONS = ['Update','New', 'Delete']

headers = {
    "X-USER-TOKEN":"skljfva8a4wrm283"
}


date = datetime.datetime.now()
TODAY = date.strftime(r"%Y%m%d")

commit_time = TODAY

BG = "#ffffff"
FG = "#000000"
BG_ALT = "#276722"
SUCCESS = "#42f557"
FAILURE = "#e85423"

def get_logo_color():
    graph_endpoint = f"{ORIGINAL_ENDPOINT}/{USERNAME}/graphs"
    print(USERNAME, TOKEN)
    response = requests.get(url=graph_endpoint, headers=headers)
    response = response.json()
    color = COLORS[response["graphs"][0]["color"]]

    return color

def submit():
    if(list.get() == "New"):
        add()
    elif(list.get() == "Update"):
        update()
    elif(list.get() == "Delete"):
        delete()

def increment():
    graph_endpoint = f"{ORIGINAL_ENDPOINT}/{USERNAME}/graphs/{GRAPHID}/increment"

    response = requests.put(url=graph_endpoint, headers=headers)
    if(response.status_code != 200):
        status_label.config(state=NORMAL, text="Increment failed")
    else:
        status_label.config(state=NORMAL, text="Pixel incremented")
    window.after(3000, func=resetlabel)
    print(response.text)

def decrement():
    graph_endpoint = f"{ORIGINAL_ENDPOINT}/{USERNAME}/graphs/{GRAPHID}/decrement"

    response = requests.put(url=graph_endpoint, headers=headers)
    if(response.status_code != 200):
        status_label.config(state=NORMAL, text="Decrement failed")
    else:
        status_label.config(state=NORMAL, text="Pixel decremented")
    window.after(3000, func=resetlabel)
    print(response.text)

def resetlabel():
    status_label.config(state=DISABLED)
    
#NEW USER
def new_user(username, token):
    user_params = {
        "token":token,
        "username":username,
        "agreeTermsOfService":"yes",
        "notMinor":"yes"
    }

    response = requests.post(url=ORIGINAL_ENDPOINT, json=user_params) #--> user created, don't need it anymore
    print(response.text)
    with open("user.txt", "x") as file:
        file.write(f"{USERNAME},{TOKEN}")


## CREATE GRAPH
def create(graph_id, graph_name, graph_unit, graph_type, graph_color):
    graph_endpoint = f"{ORIGINAL_ENDPOINT}/{USERNAME}/graphs"
    
    create_params = {
        "id":graph_id,
        "name":graph_name,
        "unit":graph_unit,
        "type":graph_type,
        "color":graph_color
    }

    print(create_params)

    response = requests.post(url=graph_endpoint, json=create_params, headers=headers)
    with open("user.txt", "a") as file:
        file.write(f",{graph_id}")

retek = []

def read_user():
    global retek
    global USERNAME
    global TOKEN
    global GRAPHID

    with open("user.txt", "r") as file:
        retek = file.readlines()
    retek = retek[0].split(",")
    USERNAME = retek[0]
    TOKEN = retek[1]
    GRAPHID = retek[2]
    print(USERNAME,TOKEN,GRAPHID)


##ADD PIXEL
def add():
    pixeladd_endpoint = f"{ORIGINAL_ENDPOINT}/{USERNAME}/graphs/{GRAPHID}"

    if(len(date_input.get()) >= 1):
        commit_time = date_input.get()
    else:
        commit_time = TODAY

    pixel_config = {
        "date":commit_time,
        "quantity":f"{counter_input.get()}"
    }

    response = requests.post(url=pixeladd_endpoint, json=pixel_config, headers=headers)
    if(response.status_code != 200):
        status_label.config(state=NORMAL, text="Adding failed")
    else:
        status_label.config(state=NORMAL, text="Pixel added")
    print(response.text)
    window.after(3000, func=resetlabel)

##UPDATE A PIXEL
def update():
    if(len(date_input.get()) >= 1):
        commit_time = date_input.get()
    else:
        commit_time = TODAY
    
    print(commit_time)

    update_endpoint = f"{ORIGINAL_ENDPOINT}/{USERNAME}/graphs/{GRAPHID}/{commit_time}"

    update_config = {
        "quantity":f"{counter_input.get()}"
    }

    response = requests.put(url=update_endpoint, json=update_config, headers=headers)
    if(response.status_code != 200):
        status_label.config(state=NORMAL, text="Update unsuccessful")
    else:
        status_label.config(state=NORMAL, text="Update successful")
    window.after(3000, func=resetlabel)
    print(response.text)

#DELETE PIXEL
def delete():
    graph_endpoint = f"{ORIGINAL_ENDPOINT}/{USERNAME}/graphs/{GRAPHID}/{commit_time}"

    response = requests.delete(url=graph_endpoint, headers=headers)
    if(response.status_code != 200):
        status_label.config(state=NORMAL, text="Delete unsuccessful")
    else:
        status_label.config(state=NORMAL, text="Pixel deleted")
    window.after(3000, func=resetlabel)
    print(response.text)

answer = ""

if(LENGTH>1):
    if(ARGS[1] == "register"): # register username token
        username = input("Enter a username: ")
        token = input("Enter a token: ")
        read_user()

        answer = input("Do you want to create a graph? Y/N: ")
        if(answer == 'Y'):
            create()
    elif(ARGS[1] == "create"):
        print("Please specify your new graph.") #Name of the graph: Unit of graph: Type of graph: Color of pixels:
        graph_id = input("ID of the graph: ")
        graph_name = input("Graph Name:")
        graph_unit = input("Unit of graph: ")
        graph_type = input("Type of graph (int/float): ")
        print("Available colors: shibafu (green), momiji (red), sora (blue), ichou (yellow), ajisai (purple) and kuro (black)")
        graph_color = input("Color of pixels: ")
        print(USERNAME)
        create(graph_id, graph_name, graph_unit, graph_type, graph_color)
else:
    read_user()
    headers["X-USER-TOKEN"] = TOKEN

    print(f"Available graphs: {retek[2:]}")
    graph = input("Which graph?")
    GRAPHID = graph

    openstring = f'{ORIGINAL_ENDPOINT}/{USERNAME}/graphs/{GRAPHID}.html'
    webbrowser.open(openstring)

    color = get_logo_color()
    png_path = f".//images//{color}.png"

    window = Tk()
    window.config(padx = 20, pady = 20, bg=BG)
    window.title("Pixela Poster")

    logo = Image.open(png_path)
    logo = ImageTk.PhotoImage(logo)
    logolabel = Label(image=logo, height=100, width = 300, bg=BG)
    logolabel.image = logo
    logolabel.grid(column=1, row = 0)

    date_label = Label(text = "Date (YYYYMMDD)", bg=BG, fg=FG, font=FONT)
    date_label.grid(column = 1, row = 1, pady = 10)

    date_input = Entry(width = 30, justify = CENTER)
    date_input.grid(column = 1, row = 2)

    counter_label = Label(text = "Value", bg=BG, fg=FG, font=FONT)
    counter_label.grid(column = 1, row = 3, pady = 10)

    counter_input = Entry(width = 30, justify=CENTER)
    counter_input.grid(column = 1, row = 4)


    list = StringVar()
    list.set("Choose action")
    menu = OptionMenu(window, list, *OPTIONS)
    menu.grid(column = 1, row = 5, pady = 10)
    menu.config( fg = FG)
    menu["menu"].config(fg=FG, borderwidth=0)
    menu["highlightthickness"] = 0

    button = Button(text="Submit", command = submit, fg=FG, font=FONT)
    button.grid(column = 1, row = 6, pady = 10)

    increment_button = Button(text="+", command=increment, fg=FG, font=FONT)
    increment_button.grid(column=1, row = 5, pady = 10, ipadx=5, sticky = "w", padx = 30)
    decrement_button = Button(text="-", command=decrement, fg=FG, font=FONT)
    decrement_button.grid(column=1, row=5, pady=10, ipadx=5,sticky="e", padx = 30)

    status_label = Label(text="Something", bg=BG, fg=FG, font=FONT, disabledforeground=BG, state=DISABLED)
    status_label.grid(column=1, row = 7)


    window.mainloop()