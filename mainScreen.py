import tkinter as tk
from tkinter import ttk
from tkintermapview import TkinterMapView
import csv
import os

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
listOfLocations = {
    "BSC": (40.52346671364952, -74.45821773128102),
    "LSC": (40.52361937958186, -74.43697999874263),
    "ARC": (40.523776007542665, -74.4648874666412)
}
def button_click(button_number):
    print(f"Button {button_number} clicked!")
def find_midpoint(lat1, lon1, lat2, lon2):
    mid_lat = (lat1 + lat2) / 2
    mid_lon = (lon1 + lon2) / 2
    return mid_lat, mid_lon

def generatePath(markerA, markerB, map_widget):
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
                map_widget.delete_all_path()
                x, y = find_midpoint(listOfLocations[markerA.data][0], listOfLocations[markerA.data][1], listOfLocations[markerB.data][0], listOfLocations[markerB.data][1])
                map_widget.set_position(x, y)
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

def on_select(marker, event, other_dropdown, other_marker, map_widget):
    selected_location = event.widget.get()
    if selected_location == "":
        marker.set_position(0, 0)
        marker.data = "NULL"
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
    generatePath(marker, other_marker, map_widget)

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("1280x800")  # Set the initial size of the window
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill="both", expand=True)

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        header_label = tk.Label(self, text="Hi, I'm RUBEN!", bg="#990000", fg="white", font=("Arial", 24, "bold"), pady=20)
        header_label.pack(side="top", fill="x")

        button_frame = tk.Frame(self)
        button_frame.pack(side="top", pady=20)

        self.icon1 = tk.PhotoImage(file="icons/map_marker_white.png")
        self.icon2 = tk.PhotoImage(file="icons/database_icon_white.png")
        self.icon3 = tk.PhotoImage(file="icons/Question_mark_white.png")

        self.icon1 = self.icon1.subsample(50)  # Adjust the subsample value according to your needs
        self.icon2 = self.icon2.subsample(50)
        self.icon3 = self.icon3.subsample(50)

        button1 = tk.Button(button_frame, text="Where to?", command=lambda: master.switch_frame(PageOne), bg="#990000", fg="white", font=("Arial", 32), bd=3, image=self.icon1, compound='left')
        button2 = tk.Button(button_frame, text="Rutgers Database", command=lambda: button_click(2), bg="#990000", fg="white", font=("Arial", 32), bd=3, image=self.icon2, compound='left')
        button3 = tk.Button(button_frame, text="FAQ", command=lambda: button_click(3), bg="#990000", fg="white", font=("Arial", 32), bd=3, image=self.icon3, compound='left')

        button1.pack(side=tk.LEFT, padx=50, pady= 200)
        button2.pack(side=tk.LEFT, padx=50, pady= 200)
        button3.pack(side=tk.LEFT, padx=50, pady= 200)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.rowconfigure(1, weight=1)

class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        header_frame = tk.Frame(self, bg="#990000", height=80)
        header_frame.pack(fill="x")

        back_button = tk.Button(header_frame, text="Back", command=lambda: master.switch_frame(StartPage), bg="#990000", fg="white", font=("Arial", 16, "bold"), padx=10)
        back_button.pack(side="left", padx=20)

        header_label = tk.Label(header_frame, text="Where Would You Like to Go?", bg="#990000", fg="white", font=("Arial", 24, "bold"), pady=20)
        header_label.pack()

        left_frame = tk.Frame(self)
        left_frame.pack(side="left", fill="y")

        right_frame = tk.Frame(self)
        right_frame.pack(side="right", fill="both", expand=True)

        map_widget = CustomTkinterMapView(right_frame, width=960, height=600, corner_radius=0)
        map_widget.pack(fill="both", expand=True)

        marker_2 = map_widget.set_marker(40.52346671364952, -74.45821773128102, text="BSC")
        marker_2.data = "BSC"
        marker_3 = map_widget.set_marker(0, 0, text="NULL")
        marker_3.data = "NULL"

        csv_file_path = "mapPaths/BSCtoLSC.csv"

        with open(csv_file_path, 'r') as file:
            csv_reader = csv.reader(file)

            coordinates = []

            for row in csv_reader:
                if len(row) >= 2 and row[0].strip() and row[1].strip():
                    try:
                        latitude, longitude = map(float, (row[0].strip(), row[1].strip()))
                        coordinates.append((latitude, longitude))
                    except ValueError as e:
                        print(f"Skipping invalid row: {row}. Error: {e}")

        path_1 = None

        label_1 = ttk.Label(left_frame, text="Starting Location")
        label_1.grid(row=0, column=0, padx=5, pady=5)
        dropdown_1 = ttk.Combobox(left_frame, values=["", "BSC", "LSC", "ARC"])
        dropdown_1.grid(row=1, column=0, padx=5, pady=5)
        dropdown_1.bind("<<ComboboxSelected>>", lambda event: on_select(marker_2, event, dropdown_2, marker_3, map_widget))
        dropdown_1.set("BSC")

        label_2 = ttk.Label(left_frame, text="Destination")
        label_2.grid(row=2, column=0, padx=5, pady=5)
        dropdown_2 = ttk.Combobox(left_frame, values=["", "BSC", "LSC", "ARC"])
        dropdown_2.grid(row=3, column=0, padx=5, pady=5)
        dropdown_2.bind("<<ComboboxSelected>>", lambda event: on_select(marker_3, event, dropdown_1, marker_2, map_widget))

        map_widget.set_position(40.52346671364952, -74.45821773128102)
        map_widget.set_zoom(15)
        map_widget.max_zoom = 15
class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is page two").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
