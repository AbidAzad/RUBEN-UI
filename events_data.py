import tkinter
from tkinter import ttk
from tkinter import messagebox
import sqlite3

def enter_data():
    event_name = event_name_entry.get()
    event_location = event_location_entry.get()
    
    if event_name and event_location:
        print("Event Name:", event_name)
        print("Event Location:", event_location)
        print("------------------------------------------")
        
        # Create Table
        conn = sqlite3.connect('data2.db')
        table_create_query = '''CREATE TABLE IF NOT EXISTS Event_Data 
                (event_name TEXT, event_location TEXT)
        '''
        conn.execute(table_create_query)
        
        # Insert Data
        data_insert_query = '''INSERT INTO Event_Data (event_name, event_location) VALUES (?, ?)'''
        data_insert_tuple = (event_name, event_location)
        cursor = conn.cursor()
        cursor.execute(data_insert_query, data_insert_tuple)
        conn.commit()
        conn.close()
    else:
        tkinter.messagebox.showwarning(title="Error", message="Event name and event location are required.")

window = tkinter.Tk()
window.title("Event Entry Form")

frame = tkinter.Frame(window)
frame.pack()

# Event Info
event_info_frame = tkinter.LabelFrame(frame, text="Event Information")
event_info_frame.grid(row=0, column=0, padx=20, pady=10)

event_name_label = tkinter.Label(event_info_frame, text="Event Name")
event_name_label.grid(row=0, column=0)
event_location_label = tkinter.Label(event_info_frame, text="Event Location")
event_location_label.grid(row=1, column=0)

event_name_entry = tkinter.Entry(event_info_frame)
event_location_entry = tkinter.Entry(event_info_frame)
event_name_entry.grid(row=0, column=1)
event_location_entry.grid(row=1, column=1)

for widget in event_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Button
button = tkinter.Button(frame, text="Enter data", command=enter_data)
button.grid(row=1, column=0, sticky="news", padx=20, pady=10)

window.mainloop()
