# Pixela Manager

This is a tool for easily managing the pixe.la API with a GUI and Command Line Arguments

## How to run

Just run the main.py in the command line:
```
python main.py
```

## Usage

The usage of this tool can be separated into two parts:

1. Command Line Arguments

	If nothing is specified, it will take you through the registration, and graph creation.
	Running the program with these arguments will complete the task and exit.


	- register
		- will call new_user(), that takes you through the process of creating an "account"
		- will delete the user.txt file (multiple user option in progress)
	- create_graph
		- calls create_graph(), which creates a new graph with the specified parameters
		- Requirements : user database not perfect by any means, don't use a graph name that's has any relation to the username or token eg.: username: activitytracker graphid: activity OR tracker (fix in progress)
	- delete_user
		- calls delete_user(), which deletes the user
	- delete_graph
		- calls delete_graph(), which deletes the specified graph

2. Using the UI

	- Clicking the pixela logo will take you to the main dashboard
	- Not specifying a date will create or update today's pixel. Specifying a date (YYYYMMDD format) will create/update a pixel on the given date
	- A value has to be given when creating or updating a pixel
	- The "+" button will increment the day's pixel by 1-if the graph's type attribute is "int" or by 0.1-if the attribute is "float"
		- The buttons will execute increment/decrement without any additional input

	- The submit button will execute the chosen method from the drop-down menu

	- Drop down menu options:
		- New : creates a pixel on the specified date, or on the current date if date field is empty
		- Update : creates a pixel on the specified date, or on the current date if date field is empty
		- Delete : deletes a pixel on the specified date, or on the current date if date field is empty

## Dependencies

- Packages : requests, datetime, sys, webbrowser, os, random, tkinter, PIL
