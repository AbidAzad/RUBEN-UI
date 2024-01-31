import tkinter
from tkinter import ttk
from tkintermapview import TkinterMapView
import csv
import os

listOfLocations = {
    "BSC" : (40.52346671364952, -74.45821773128102),
    "LSC" : (40.52361937958186, -74.43697999874263),
    "ARC" : (40.523776007542665, -74.4648874666412)
}
def generatePath(markerA, markerB):
    if(markerA.data == "NULL" or markerB.data == "NULL"):
        map_widget.delete_all_path()
        if(markerA.data == "NULL" and markerB.data == "NULL"):
            map_widget.set_position(40.52346671364952, -74.45821773128102)
        elif(not markerA.data == "NULL"):
            map_widget.set_position(listOfLocations[markerA.data][0], listOfLocations[markerA.data][1])
        else:
            map_widget.set_position(listOfLocations[markerB.data][0], listOfLocations[markerB.data][1])
    else:
        csv_file_path = f"mapPaths/{markerA.data}to{markerB.data}.csv"
        if(not os.path.isfile(csv_file_path)):
            csv_file_path = f"mapPaths/{markerB.data}to{markerA.data}.csv"
            if(not os.path.isfile(csv_file_path)):
                map_widget.set_position(listOfLocations[markerA.data][0], listOfLocations[markerA.data][1])
                return
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.reader(file)
            
            # Initialize a list to store the coordinates
            coordinates = []
            
            # Iterate through each row in the CSV file
            for row in csv_reader:
                # Check if both latitude and longitude are present and convert to float
                if len(row) >= 2 and row[0].strip() and row[1].strip():
                    try:
                        latitude, longitude = map(float, (row[0].strip(), row[1].strip()))
                        # Append the coordinates tuple to the list
                        coordinates.append((latitude, longitude))
                    except ValueError as e:
                        print(f"Skipping invalid row: {row}. Error: {e}")
        
        map_widget.delete_all_path()
        map_widget.set_path(coordinates)
        if coordinates:
            mid_latitude = sum(coord[0] for coord in coordinates) / len(coordinates)
            mid_longitude = sum(coord[1] for coord in coordinates) / len(coordinates)

            # Set the map position to the middle of the path
            map_widget.set_position(mid_latitude, mid_longitude)
def on_select(marker, event, other_dropdown, other_marker):
    # Example function to handle drop-down selection
    selected_location = event.widget.get()
    
    if(selected_location == ""):
        marker.set_position(0, 0)
        marker.data = "NULL"
    # Update marker coordinates based on the selected location
    else:
        marker.set_position(listOfLocations[selected_location][0], listOfLocations[selected_location][1])
        marker.set_text(selected_location)
        marker.data = selected_location

    other_dropdown_value = other_dropdown.get()
    if other_dropdown_value == selected_location:
        other_dropdown.set("")  # Set the other dropdown to blank
        other_marker.set_position(0, 0)
        other_marker.data = "NULL"
        
    # Update the map
    generatePath(marker, other_marker)
    map_widget.update()

        
class CustomTkinterMapView(TkinterMapView):
    def mouse_move(self, event):
        # Override the mouse_move() method to do nothing
        pass
    
    def mouse_zoom(self, event):
        pass
    
    def button_zoom_in(self):
        pass
    
    def button_zoom_out(self):
        pass

root_tk = tkinter.Tk()
root_tk.geometry(f"{800}x{400}")
root_tk.title("Map Viewing Screen")

# Create a frame for the left side
left_frame = tkinter.Frame(root_tk)
left_frame.pack(side="left", fill="y")



# Create a frame for the map on the right side
right_frame = tkinter.Frame(root_tk)
right_frame.pack(side="right", fill="both", expand=True)

# Create map widget
map_widget = CustomTkinterMapView(right_frame, width=600, height=400, corner_radius=0)
map_widget.pack(fill="both", expand=True)

# Add markers and path to the map
marker_2 = map_widget.set_marker(40.52346671364952, -74.45821773128102, text="BSC")
marker_2.data = "BSC"
marker_3 = map_widget.set_marker(0, 0, text="NULL")
marker_3.data = "NULL"

# Read the CSV file
csv_file_path = "mapPaths/BSCtoLSC.csv"

with open(csv_file_path, 'r') as file:
    csv_reader = csv.reader(file)
    
    # Initialize a list to store the coordinates
    coordinates = []
    
    # Iterate through each row in the CSV file
    for row in csv_reader:
        # Check if both latitude and longitude are present and convert to float
        if len(row) >= 2 and row[0].strip() and row[1].strip():
            try:
                latitude, longitude = map(float, (row[0].strip(), row[1].strip()))
                # Append the coordinates tuple to the list
                coordinates.append((latitude, longitude))
            except ValueError as e:
                print(f"Skipping invalid row: {row}. Error: {e}")

# Set the path for the map_widget
path_1 = None

# Create two drop-down menus
label_1 = ttk.Label(left_frame, text="Dropdown 1")
label_1.grid(row=0, column=0, padx=5, pady=5)
dropdown_1 = ttk.Combobox(left_frame, values=["", "BSC", "LSC", "ARC"])
dropdown_1.grid(row=1, column=0, padx=5, pady=5)
dropdown_1.bind("<<ComboboxSelected>>", lambda event: on_select(marker_2, event, dropdown_2, marker_3))
# Set the default option for the first dropdown as "BSC"
dropdown_1.set("BSC")

label_2 = ttk.Label(left_frame, text="Dropdown 2")
label_2.grid(row=2, column=0, padx=5, pady=5)
dropdown_2 = ttk.Combobox(left_frame, values=["", "BSC", "LSC", "ARC"])
dropdown_2.grid(row=3, column=0, padx=5, pady=5)
dropdown_2.bind("<<ComboboxSelected>>", lambda event: on_select(marker_3, event, dropdown_1, marker_2))

# Set map position
map_widget.set_position(40.52346671364952, -74.45821773128102)

map_widget.set_zoom(15)
map_widget.max_zoom = 15

root_tk.mainloop()
