import tkinter as tk
import dataloader

def show_text(value):
    print(value)
    dataloader.display_vacc_covid_graph(value)

# Create the root window
root = tk.Tk()

# Create a variable to hold the selected value
selected_value = tk.StringVar(root)

# Create the picklist
picklist = tk.OptionMenu(root, selected_value, "United States", "France", "Brazil", "Japan", "Cameroon", "China")
picklist.pack()

# Bind the show_text function to the picklist
selected_value.trace("w", lambda *args: show_text(selected_value.get()))

# Start the main event loop
root.mainloop()