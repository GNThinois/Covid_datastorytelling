import tkinter as tk

def show_text(value):
    if value == "Option 1":
        print("You selected option 1")
    elif value == "Option 2":
        print("You selected option 2")
    else:
        print("Invalid option selected")

# Create the root window
root = tk.Tk()

# Create a variable to hold the selected value
selected_value = tk.StringVar(root)

# Create the picklist
picklist = tk.OptionMenu(root, selected_value, "Option 1", "Option 2")
picklist.pack()

# Bind the show_text function to the picklist
selected_value.trace("w", lambda *args: show_text(selected_value.get()))

# Start the main event loop
root.mainloop()