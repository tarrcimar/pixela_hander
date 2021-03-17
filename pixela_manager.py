import requests
import datetime
import sys
import webbrowser
import time
import os
import random

from tkinter import *
from PIL import ImageTk, Image

USERNAME = ""
TOKEN = ""
GRAPHID = ""

ARGS = sys.argv
LENGTH = len(ARGS)

ORIGINAL_ENDPOINT = 'https://pixe.la/v1/users' # api endpoint

COLORS = { # different colors and their representation in the parameters
    "shibafu":"green",
    "momiji":"red",
    "sora":"purple",
    "ichou":"yellow",
    "ajisai":"purple",
    "kuro":"orange"
}

FONT = ("Corbel", 12, "bold")
color = ""
OPTIONS = ['update_pixel','New', 'delete_pixel']

headers = {
    "X-USER-TOKEN":TOKEN
}

date = datetime.datetime.now()
TODAY = date.strftime(r"%Y%m%d")

commit_time = TODAY

BG = "#ffffff"
FG = "#000000"
BG_ALT = "#276722"
SUCCESS = "#42f557"
FAILURE = "#e85423"

def submit():
    if(list.get() == "New"):
        add_pixel()
    elif(list.get() == "update_pixel"):
        update_pixel()
    elif(list.get() == "delete_pixel"):
        delete_pixel()


def resetlabel():
    status_label.config(state=DISABLED, fg="#000000")


def get_logo_color(graph_no): # get the logo color according to the graph color
    graph_endpoint = f"{ORIGINAL_ENDPOINT}/{USERNAME}/graphs"
    print(USERNAME, TOKEN)
    response = requests.get(url=graph_endpoint, headers=headers)
    response = response.json()
    color = COLORS[response["graphs"][graph_no]["color"]]

    return color


def increment_pixel(): # add_pixel +1 or +0.1 to the pixel
    graph_endpoint = f"{ORIGINAL_ENDPOINT}/{USERNAME}/graphs/{GRAPHID}/increment"

    response = requests.put(url=graph_endpoint, headers=headers)
    if(response.status_code != 200):
        status_label.config(state=NORMAL, text="Increment failed")
    else:
        status_label.config(state=NORMAL, text="Pixel incremented")
    window.after(3000, func=resetlabel)
    print(response.text)


def decrement_pixel(): # subtract +1 or -0.1 from the pixel
    graph_endpoint = f"{ORIGINAL_ENDPOINT}/{USERNAME}/graphs/{GRAPHID}/decrement"

    response = requests.put(url=graph_endpoint, headers=headers)
    if(response.status_code != 200):
        status_label.config(state=NORMAL, text="Decrement failed")
    else:
        status_label.config(state=NORMAL, text="Pixel decremented")
    window.after(3000, func=resetlabel)
    print(response.text)

    
#NEW USER
def new_user(username, token): # create_graph the new user, delete_pixel the old text
    try:
        os.remove("user.txt")
    except FileNotFoundError:
        print("User not in file. Creating...")
    
    user_params = {
        "token":token,
        "username":username,
        "agreeTermsOfService":"yes",
        "notMinor":"yes"
    }

    response = requests.post(url=ORIGINAL_ENDPOINT, json=user_params)
    print(response.text)
    with open("user.txt", "w") as file:
        file.write(f"{username},{token}")

def delete_user():
    print("This action will delete the user")
    username = input("Username: ")
    token = input("Token: ")

    delete_endpoint = graph_endpoint = f"{ORIGINAL_ENDPOINT}/{username}"
    headers['X-USER-TOKEN'] = token

    response = requests.delete(url=delete_endpoint, headers=headers)
    print(response.text)

def create_graph(): # create a new graph
    global TOKEN

    print("Please specify your new graph.") #Name of the graph: Unit of graph: Type of graph: Color of pixels:
    graph_id = input("ID of the graph: ")
    graph_name = input("Graph Name: ")
    graph_unit = input("Unit of graph: ")
    graph_type = input("Type of graph (int/float): ")
    print("Available colors: shibafu (green), momiji (red), sora (blue), ichou (yellow), ajisai (purple) and kuro (black)")
    graph_color = input("Color of pixels: ")
    read_user()
    headers["X-USER-TOKEN"] = TOKEN
    print(USERNAME, headers)

    graph_endpoint = f"{ORIGINAL_ENDPOINT}/{USERNAME}/graphs"
    
    create_graph_params = {
        "id":graph_id,
        "name":graph_name,
        "unit":graph_unit,
        "type":graph_type,
        "color":graph_color
    }

    response = requests.post(url=graph_endpoint, json=create_graph_params, headers=headers)
    print(response.text)
    print(response.status_code)
    with open("user.txt", "a") as file:
        file.write(f",{graph_id}")


#add_pixel PIXEL
def add_pixel():
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
        status_label.config(state=NORMAL, text="add_pixeling failed. Check date and value.", fg="#ff0000")
    else:
        status_label.config(state=NORMAL, text="Pixel add_pixeled", fg="#000000")
    print(response.text)
    window.after(3000, func=resetlabel)


def update_pixel(): # update_pixel a pixels value
    if(len(date_input.get()) >= 1):
        commit_time = date_input.get()
    else:
        commit_time = TODAY
    
    print(commit_time)

    update_pixel_endpoint = f"{ORIGINAL_ENDPOINT}/{USERNAME}/graphs/{GRAPHID}/{commit_time}"

    update_pixel_config = {
        "quantity":f"{counter_input.get()}"
    }

    response = requests.put(url=update_pixel_endpoint, json=update_pixel_config, headers=headers)
    if(response.status_code != 200):
        status_label.config(state=NORMAL, text="update_pixel unsuccessful. Check date format.", fg="#ff0000")
    else:
        status_label.config(state=NORMAL, text="update_pixel successful", fg="#000000")
    window.after(3000, func=resetlabel)
    print(response.text)


def delete_pixel(): # delete_pixel a pixel
    if(len(date_input.get()) >= 1): # check if there's a date specified
        commit_time = date_input.get()
    else:
        commit_time = TODAY
    graph_endpoint = f"{ORIGINAL_ENDPOINT}/{USERNAME}/graphs/{GRAPHID}/{commit_time}"

    response = requests.delete_pixel(url=graph_endpoint, headers=headers)
    if(response.status_code != 200):
        status_label.config(state=NORMAL, text="delete_pixel unsuccessful. Check date format.", fg="#ff0000")
    else:
        status_label.config(state=NORMAL, text="Pixel delete_pixeld", fg="#000000")
    window.after(3000, func=resetlabel)
    print(response.text)


userdata = []

def read_user():
    global userdata
    global USERNAME
    global TOKEN
    global GRAPHID

    with open("user.txt", "r") as file:
        userdata = file.readlines()
    userdata = userdata[0].split(",")
    USERNAME = userdata[0]
    TOKEN = userdata[1]
    print(USERNAME, TOKEN)
    if(len(userdata)>2):
        GRAPHID = userdata[2]


answer = ""

#chech cl arguments
if(LENGTH>1):
    if(ARGS[1] == "register"): # register username token
        username = input("Enter a username: ")
        token = input("Enter a token (8 characters minimum): ")
        new_user(username, token)

        answer = input("Do you want to create a graph? Y/N: ")
        if(answer == 'Y'):
            create_graph()
    elif(ARGS[1] == "create_graph"):
        create_graph()
    elif(ARGS[1] == "delete"):
        delete_user()
else:
    read_user()
    headers["X-USER-TOKEN"] = TOKEN

    # get the available graphs from the textfile
    print(f"Available graphs: {userdata[2:]}")
    graph = input("Choose a graph to display: ")
    GRAPHID = graph

    # open the web interface
    openstring = f'{ORIGINAL_ENDPOINT}/{USERNAME}/graphs/{GRAPHID}.html'
    webbrowser.open(openstring)

    # set the logo color
    color = get_logo_color(userdata.index(graph) -2)
    png_path = f".//images//{color}.png"


    # create_graph the Tkinter window and the widgets
    window = Tk()
    window.config(padx = 20, pady = 20, bg=BG)
    window.title("Pixela Manager")

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

    increment_button = Button(text="+", command=increment_pixel, fg=FG, font=FONT)
    increment_button.grid(column=1, row = 5, pady = 10, ipadx=5, sticky = "w", padx = 30)
    decrement_button = Button(text="-", command=decrement_pixel, fg=FG, font=FONT)
    decrement_button.grid(column=1, row=5, pady=10, ipadx=5,sticky="e", padx = 30)

    status_label = Label(text="", bg=BG, fg=FG, font=FONT, disabledforeground=BG, state=DISABLED)
    status_label.grid(column=1, row = 7)


    window.mainloop()