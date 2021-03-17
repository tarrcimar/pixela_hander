import requests
import datetime
import sys
from tkinter import *
import webbrowser

USERNAME = "tmarton"
TOKEN = "skljfva8a4wrm283"
GRAPHID = "graph1"

ORIGINAL_ENDPOINT = 'https://pixe.la/v1/users'

openstring = f'{ORIGINAL_ENDPOINT}/{USERNAME}/graphs/{GRAPHID}.html'
webbrowser.open(openstring)

headers = {
    "X-USER-TOKEN":TOKEN
}

BG = "#a67068"
FG = "#f5f5dc"
BG_ALT = "#a05a4e"
SUCCESS = "#42f557"
FAILURE = "#e85423"

date = datetime.datetime.now()
TODAY = date.strftime(r"%Y%m%d")

FONT = ("Corbel", 12, "bold")

OPTIONS = ['Update','New']


class Create(Tk):
    def __init__(self):
        super().__init__()
        self.config(padx = 20, pady = 20, bg=BG)
        self.title("Pixela Poster")

        canvas = Canvas(width = 200, height = 224, bg = BG, highlightthickness = 0)
        logo_png = PhotoImage(file = "logo.png")
        canvas.create_image(100,112,image = logo_png)

        self.date_input = Entry(width = 30, justify = CENTER)
        self.date_input.grid(column = 1, row = 1)

        self.date_label = Label(text = "Date (YYYYMMDD)", bg=BG, fg=FG, font=FONT)
        self.date_label.grid(column = 1, row = 0, pady = 10)

        self.counter_input = Entry(width = 30, justify=CENTER)
        self.counter_input.grid(column = 1, row = 3)

        self.counter_label = Label(text = "Value", bg=BG, fg=FG, font=FONT)
        self.counter_label.grid(column = 1, row = 2, pady = 10)

        self.list = StringVar()
        self.list.set("Choose action")
        self.menu = OptionMenu(self, self.list, *OPTIONS)
        self.menu.grid(column = 1, row = 4, pady = 10)
        self.menu.config(bg=BG_ALT, fg = FG)
        self.menu["menu"].config(bg=BG_ALT, fg=FG, borderwidth=0)
        self.menu["highlightthickness"] = 0

        self.button = Button(text="Submit", command = self.submit, bg=BG_ALT, fg=FG, font=FONT)
        self.button.grid(column = 1, row = 5, pady = 10)

    def submit(self):
        self.button.config(bg=BG_ALT)
        if(self.list.get() == "New"):
            add()
        elif(self.list.get() == "Update"):
            update()


gui = Create()

#NEW USER
def new_user():
    user_params = {
        "token":TOKEN,
        "username":USERNAME,
        "agreeTermsOfService":"yes",
        "notMinor":"yes"
    }

    response = requests.post(url=ORIGINAL_ENDPOINT, json=user_params) #--> user created, don't need it anymore
    print(response.text)

#new_user()

## CREATE GRAPH
def create():
    graph_endpoint = f"{ORIGINAL_ENDPOINT}/{USERNAME}/graphs"

    graph_config = {
        "id":GRAPHID,
        "name":"Daily Activity Level",
        "unit":"commit",
        "type":"int",
        "color":"ichou"
    }

    response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
    print(response.text)
    
#create()

commit_time = ""


##ADD PIXEL
def add():
    pixeladd_endpoint = f"{ORIGINAL_ENDPOINT}/{USERNAME}/graphs/{GRAPHID}"

    if(len(gui.date_input.get()) >= 1):
        commit_time = gui.date_input.get()
    else:
        commit_time = TODAY

    pixel_config = {
        "date":commit_time,
        "quantity":f"{gui.counter_input.get()}"
    }

    response = requests.post(url=pixeladd_endpoint, json=pixel_config, headers=headers)
    code = response.status_code
    if(code == 200):
        gui.button.config(bg=SUCCESS)
    else:
        gui.button.config(bg=FAILURE)

pixeladd_endpoint = f"{ORIGINAL_ENDPOINT}/{USERNAME}/graphs/{GRAPHID}"
pixel_config = {
        "unit":"units"
    }
response = requests.put(url=pixeladd_endpoint, json=pixel_config, headers=headers)
print(response.text)



##UPDATE A PIXEL
def update():
    if(len(gui.date_input.get()) >= 1):
        commit_time = gui.date_input.get()
    else:
        commit_time = TODAY
    
    print(commit_time)

    update_endpoint = f"{ORIGINAL_ENDPOINT}/{USERNAME}/graphs/{GRAPHID}/{commit_time}"

    update_config = {
        "quantity":f"{gui.counter_input.get()}"
    }

    response = requests.put(url=update_endpoint, json=update_config, headers=headers)
    code = response.status_code
    if(code == 200):
        gui.button.config(bg=SUCCESS)
    else:
        gui.button.config(bg=FAILURE)
    print(response.text)

gui.mainloop()