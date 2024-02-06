import tkinter as tk
from tkinter import ttk
from tkintermapview import TkinterMapView
import csv
import os
from PIL import Image, ImageTk
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
    "ARC": (40.523776007542665, -74.4648874666412),
    "RWH": (40.52484567146845, -74.4594846000904),
    "SEC": (40.52264886068991, -74.46291943815686),
    "HILL": (40.52219869380479, -74.46269730376937),
    "EE": (40.521919361103436, -74.4608464326052),
    "COR": (40.521425135381364, -74.46139955251431),
    "CCB": (40.52471158885787, -74.46215078958433),
    "PHY-LH": (40.522463226834915, -74.46342747105683),
    "BME": (40.52425650913521, -74.46090857718987),
    "SRN" : (40.52301253291932, -74.4647242045775), #Physics and Astrinomy Building
    "CABM" : (40.52425101367686, -74.46993589110723),
    "Woody's Cafe": (40.52461800211061, -74.46863770197551),
    "Busch Sweets": (40.525294, -74.459073)


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
        button2 = tk.Button(button_frame, text="Rutgers Database", command=lambda: master.switch_frame(PageTwo), bg="#990000", fg="white", font=("Arial", 32), bd=3, image=self.icon2, compound='left')
        button3 = tk.Button(button_frame, text="FAQ", command=lambda: master.switch_frame(PageThree), bg="#990000", fg="white", font=("Arial", 32), bd=3, image=self.icon3, compound='left')

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
        dropdown_1 = ttk.Combobox(left_frame, values=[""] + list(listOfLocations.keys()))
        dropdown_1.grid(row=1, column=0, padx=5, pady=5)
        dropdown_1.bind("<<ComboboxSelected>>", lambda event: on_select(marker_2, event, dropdown_2, marker_3, map_widget))
        dropdown_1.set("BSC")

        label_2 = ttk.Label(left_frame, text="Destination")
        label_2.grid(row=2, column=0, padx=5, pady=5)
        dropdown_2 = ttk.Combobox(left_frame, values=[""] + list(listOfLocations.keys()))
        dropdown_2.grid(row=3, column=0, padx=5, pady=5)
        dropdown_2.bind("<<ComboboxSelected>>", lambda event: on_select(marker_3, event, dropdown_1, marker_2, map_widget))

        map_widget.set_position(40.52346671364952, -74.45821773128102)
        map_widget.set_zoom(15)
        map_widget.max_zoom = 15
class PageTwo(tk.Frame):
     def __init__(self, master):
        tk.Frame.__init__(self, master)
        sample_qa_data = {
            "What is the largest mammal on Earth?": "The blue whale is the largest mammal on Earth.",
            "How many continents are there?": "There are seven continents: Africa, Antarctica, Asia, Europe, North America, Australia (Oceania), and South America.",
            "Who wrote 'Romeo and Juliet'?": "William Shakespeare wrote 'Romeo and Juliet'.",
            "What is the capital of Japan?": "The capital of Japan is Tokyo.",
            "What is the boiling point of water in Celsius?": "The boiling point of water in Celsius is 100 degrees.",
            "Who discovered penicillin?": "Alexander Fleming discovered penicillin.",
            "What is the currency of Brazil?": "The currency of Brazil is the Brazilian Real (BRL).",
            "What is the speed of light?": "The speed of light in a vacuum is approximately 299,792 kilometers per second.",
            "Who painted the Mona Lisa?": "Leonardo da Vinci painted the Mona Lisa.",
            "What is the meaning of life, the universe, and everything?": "According to Douglas Adams' 'The Hitchhiker's Guide to the Galaxy,' the answer is 42.",
        }        
        header_frame = tk.Frame(self, bg="#990000", height=80)
        header_frame.pack(fill="x")

        back_button = tk.Button(header_frame, text="Back", command=lambda: master.switch_frame(StartPage), bg="#990000", fg="white", font=("Arial", 16, "bold"), padx=10)
        back_button.pack(side="left", padx=20)
        
        header_label = tk.Label(header_frame, text="What do you want to Know?", bg="#990000", fg="white", font=("Arial", 24, "bold"), pady=20)
        header_label.pack()
        
        # Create the search bar frame on the left side
        search_frame = tk.Frame(self, bg="#CCCCCC", width=200)  # Adjust the width as needed
        search_frame.pack(side="left", fill="y")

        # Create the search label
        search_label = tk.Label(search_frame, text="Search:", bg="#CCCCCC", font=("Arial", 16, "bold"), pady=10)
        search_label.pack()

        # Create the entry widget for the search bar
        search_entry = tk.Entry(search_frame, font=("Arial", 14))
        search_entry.pack(pady=10)
        
        # Create the search button
        search_button = tk.Button(search_frame, text="Search", command=button_click(3), bg="#990000", fg="white", font=("Arial", 14, "bold"), padx=10)
        search_button.pack()
class PageThree(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        header_frame = tk.Frame(self, bg="#990000", height=80)
        header_frame.pack(fill="x")

        back_button = tk.Button(header_frame, text="Back", command=lambda: master.switch_frame(StartPage), bg="#990000", fg="white", font=("Arial", 16, "bold"), padx=10)
        back_button.pack(side="left", padx=20)
        
        header_label = tk.Label(header_frame, text="Frequently Asked Questions", bg="#990000", fg="white", font=("Arial", 24, "bold"), pady=20)
        header_label.pack()

        # Load the image
        image_path = "robot.jpg"
        image = Image.open(image_path)
        image = image.resize((300, 300))
        photo = ImageTk.PhotoImage(image)

        # Create a label widget to display the image
        label_image = tk.Label(self, image=photo)
        label_image.image = photo  # Keep a reference to the image to prevent garbage collection
        label_image.pack(pady=20)

        # Information to display on the FAQ page
        faq_text = """Frequently Asked Questions:

1. RUBEN, what does your name stand for?
   My name stands for Remote Utility Bot for Education and Navigation

2. What is your mission?
   Welcome! My mission is to help mitigate the complexity students may deal with when first entering the university. I will provide clear directions to specific locations.

3. Who created you? 
   Jeff Acevedo, Abid Azad, Carina Manek, Samuel Fabian, and Sampat Pachade for their senior design project"""

        # Add a label to the FAQ page
        label_faq = tk.Label(self, text=faq_text, padx=20, pady=20)
        label_faq.pack(pady=20)
         
if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
