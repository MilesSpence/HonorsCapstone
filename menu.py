#!/usr/bin/env python

# The main program/file.

def printPrompt():
    print("Welcome!")
    print("Select a menu option from below:")
    print("(a) View most recent COVID-19 data")
    print("(b) Run a simulation")
    print("(c) Run a simulation with your input")
    print("(h) Return to this menu")
    print("(q) Quit\n")
    
printPrompt()

var = input("Please enter your selection: ")

# Loop
while(var.lower() != "q" and var.lower() != "exit"):
	if(var.lower() == "a"):
		import webscraper
	elif(var.lower() ==  "b"):
            sub = input("Enter your choice: \n(a) Check accuracy \n(b) 100 person sim \n(c) COVID-19 sim\n")
            if(sub.lower() == "a"):
                import accuracyCheck
            elif(sub.lower() == "b"):
                import smallPopSim
            else:
                import noInputSim
	elif(var.lower() ==  "c"):
		import userInputSim
	elif(var.lower() ==  "h"):
		print()
		printPrompt()
	else:
		print("Invalid input, try again please")

	var = input("Please enter a new selection: ")

print("Goodbye!")
