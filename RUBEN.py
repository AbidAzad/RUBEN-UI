import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from tkintermapview import TkinterMapView
import csv
import os
from PIL import Image, ImageTk
from fuzzywuzzy import process

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

location_coordinates = {
    "BSC": (40.52346671364952, -74.45821773128102),
    "LSC": (40.52361937958186, -74.43697999874263),
    "ARC": (40.523776007542665, -74.4648874666412),
    "RWH": (40.52484567146845, -74.4594846000904),
    "SEC": (40.52264886068991, -74.46291943815686),
    "HILL": (40.52219869380479, -74.46269730376937),
    "ARC": (40.523875826670384, -74.46490827123226),
    "EE": (40.521919361103436, -74.4608464326052),
    "COR": (40.521425135381364, -74.46139955251431),
    "CCB": (40.52471158885787, -74.46215078958433),
    "PHY-LH": (40.522463226834915, -74.46342747105683),
    "BME": (40.52425650913521, -74.46090857718987),
    "SRN" : (40.52301253291932, -74.4647242045775), 
    "CABM" : (40.52425101367686, -74.46993589110723)
}

def button_click(button_number):
    print(f"Button {button_number} clicked!")

def find_midpoint(lat1, lon1, lat2, lon2):
    mid_lat = (lat1 + lat2) / 2
    mid_lon = (lon1 + lon2) / 2
    return mid_lat, mid_lon

def generate_path(marker_start, marker_end, map_widget):
    if(marker_start.data == "NULL" or marker_end.data == "NULL"):
        map_widget.delete_all_path()
        if(marker_start.data == "NULL" and marker_end.data == "NULL"):
            map_widget.set_position(40.52346671364952, -74.45821773128102)
        elif(not marker_start.data == "NULL"):
            map_widget.set_position(location_coordinates[marker_start.data][0], location_coordinates[marker_start.data][1])
        else:
            map_widget.set_position(location_coordinates[marker_end.data][0], location_coordinates[marker_end.data][1])
    else:
        csv_file_path = f"mapPaths/{marker_start.data}to{marker_end.data}.csv"
        if(not os.path.isfile(csv_file_path)):
            csv_file_path = f"mapPaths/{marker_end.data}to{marker_start.data}.csv"
            if(not os.path.isfile(csv_file_path)):
                map_widget.delete_all_path()
                x, y = find_midpoint(location_coordinates[marker_start.data][0], location_coordinates[marker_start.data][1], location_coordinates[marker_end.data][0], location_coordinates[marker_end.data][1])
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
        marker.set_position(location_coordinates[selected_location][0], location_coordinates[selected_location][1])
        marker.set_text(selected_location)
        marker.data = selected_location

    other_dropdown_value = other_dropdown.get()
    if other_dropdown_value == selected_location:
        other_dropdown.set("")  
        other_marker.set_position(0, 0)
        other_marker.data = "NULL"

    generate_path(marker, other_marker, map_widget)

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("RUBEN")
        self.geometry("1280x800")  
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

        self.icon_map = tk.PhotoImage(file="icons/map_marker_white.png")
        self.icon_database = tk.PhotoImage(file="icons/database_icon_white.png")
        self.icon_faq = tk.PhotoImage(file="icons/Question_mark_white.png")

        self.icon_map = self.icon_map.subsample(50)
        self.icon_database = self.icon_database.subsample(50)
        self.icon_faq = self.icon_faq.subsample(50)

        button_map = tk.Button(button_frame, text="Where to?", command=lambda: master.switch_frame(MapPage), bg="#990000", fg="white", font=("Arial", 32), bd=3, image=self.icon_map, compound='left', borderwidth=3, relief="groove", highlightthickness=0)
        button_database = tk.Button(button_frame, text="Rutgers Database", command=lambda: master.switch_frame(SearchPage), bg="#990000", fg="white", font=("Arial", 32), bd=3, image=self.icon_database, compound='left', borderwidth=3, relief="groove", highlightthickness=0)
        button_faq = tk.Button(button_frame, text="FAQ", command=lambda: master.switch_frame(FAQPage), bg="#990000", fg="white", font=("Arial", 32), bd=3, image=self.icon_faq, compound='left', borderwidth=3, relief="groove", highlightthickness=0)

        button_map.pack(side=tk.LEFT, padx=50, pady=200)
        button_database.pack(side=tk.LEFT, padx=50, pady=200)
        button_faq.pack(side=tk.LEFT, padx=50, pady=200)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.rowconfigure(1, weight=1)
class MapPage(tk.Frame):
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

        marker_start = map_widget.set_marker(40.52346671364952, -74.45821773128102, text="BSC")
        marker_start.data = "BSC"
        marker_end = map_widget.set_marker(0, 0, text="NULL")
        marker_end.data = "NULL"

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

        label_start = ttk.Label(left_frame, text="Starting Location")
        label_start.grid(row=0, column=0, padx=5, pady=5)
        dropdown_start = ttk.Combobox(left_frame, values=[""] + list(location_coordinates.keys()))
        dropdown_start.grid(row=1, column=0, padx=5, pady=5)
        dropdown_start.bind("<<ComboboxSelected>>", lambda event: on_select(marker_start, event, dropdown_end, marker_end, map_widget))
        dropdown_start.set("BSC")

        label_end = ttk.Label(left_frame, text="Destination")
        label_end.grid(row=2, column=0, padx=5, pady=5)
        dropdown_end = ttk.Combobox(left_frame, values=[""] + list(location_coordinates.keys()))
        dropdown_end.grid(row=3, column=0, padx=5, pady=5)
        dropdown_end.bind("<<ComboboxSelected>>", lambda event: on_select(marker_end, event, dropdown_start, marker_start, map_widget))

        map_widget.set_position(40.52346671364952, -74.45821773128102)
        map_widget.set_zoom(15)
        map_widget.max_zoom = 15

class SearchPage(tk.Frame):
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

        back_button = tk.Button(header_frame, text="Back", command=lambda: master.switch_frame(StartPage),
                                bg="#990000", fg="white", font=("Arial", 16, "bold"), padx=10)
        back_button.pack(side="left", padx=20)

        header_label = tk.Label(header_frame, text="What do you want to Know?", bg="#990000", fg="white",
                                font=("Arial", 24, "bold"), pady=20)
        header_label.pack()

        search_frame = tk.Frame(self, bg="#CCCCCC", width=200) 
        search_frame.pack(side="left", fill="y")

        search_label = tk.Label(search_frame, text="Search:", bg="#CCCCCC", font=("Arial", 16, "bold"), pady=10)
        search_label.pack()

        search_entry = tk.Entry(search_frame, font=("Arial", 14))
        search_entry.pack(pady=10)

        search_button = tk.Button(search_frame, text="Search", command=lambda: self.search_question(search_entry.get()),
                                  bg="#990000", fg="white", font=("Arial", 14, "bold"), padx=10)
        search_button.pack()

        self.question_listbox = tk.Listbox(self, selectmode=tk.SINGLE, exportselection=False)
        for question in sample_qa_data.keys():
            self.question_listbox.insert(tk.END, question)
        self.question_listbox.pack(side="left", fill="both", expand=True)
        self.question_listbox.bind("<ButtonRelease-1>", lambda event: self.display_answer(event, sample_qa_data))

        self.answer_frame = tk.Frame(self, bg="#CCCCCC", width=500)

    def search_question(self, query):
        self.question_listbox.delete(0, tk.END)
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
        matched_questions = process.extractBests(query, sample_qa_data.keys(), score_cutoff=80)
        matched_questions = sorted(matched_questions, key=lambda x: x[1], reverse=True)

        for question, score in matched_questions:
            self.question_listbox.insert(tk.END, f"{question}")

        if not matched_questions:
            self.question_listbox.insert(tk.END, "No matching questions found.")

    def display_answer(self, event, sample_qa_data):
        selected_index = self.question_listbox.curselection()
        if selected_index:
            selected_question = self.question_listbox.get(selected_index)
            answer = sample_qa_data.get(selected_question, "Answer not available.")
            self.show_answer(answer)

    def show_answer(self, answer):
        self.question_listbox.pack_forget()

        for widget in self.answer_frame.winfo_children():
            widget.destroy()

        answer_label = tk.Label(self.answer_frame, text=answer, bg="#CCCCCC", font=("Arial", 14), pady=10)
        answer_label.pack()

        back_button = tk.Button(self.answer_frame, text="Back to List", command=self.back_to_list,
                                bg="#990000", fg="white", font=("Arial", 14, "bold"), padx=10)
        back_button.pack()

        self.answer_frame.pack(side="right", fill="both", expand=True)

    def back_to_list(self):
        self.answer_frame.pack_forget()
        self.question_listbox.pack(side="left", fill="both", expand=True)

class FAQPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        script_directory = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_directory, "icons\FAQBackground.jpeg")
        # Load the image file using PhotoImage
        image = Image.open(image_path)
        resized_image = image.resize((1450, 700), Image.ANTIALIAS)

        photo = ImageTk.PhotoImage(resized_image)

        # Create the label with the PhotoImage object
        bg_image = tk.Label(self, image=photo, text="Frequently Asked Questions:\n\n"
                                                    "1. RUBEN, what does your name stand for?\n"
                                                    "My name stands for Remote Utility Bot for Education and Navigation</i>\n\n"
                                                    "2. What is your mission?\n"
                                                    "Welcome! My mission is to help mitigate the complexity students \nmay deal with when first entering the university. I will provide clear directions to specific locations.\n\n"
                                                    "3. Who created you? \n"
                                                    "Jeff Acevedo, Abid Azad, Carina Manek, Samuel Fabian, and Sampat Pachade for their senior design project",
                            padx=20, pady=20, compound="center", fg="pink", font=("Helvetica", 20, "bold"), justify="left", wraplength=600)
        bg_image.image = photo  # To prevent garbage collection
        bg_image.place(relheight=1, relwidth=1)

        header_frame = tk.Frame(self, bg="#990000", height=80)
        header_frame.pack(fill="x")

        back_button = tk.Button(header_frame, text="Back", command=lambda: master.switch_frame(StartPage),
                                bg="#990000", fg="white", font=("Arial", 16, "bold"), padx=10)
        back_button.pack(side="left", padx=20)

        header_label = tk.Label(header_frame, text="Frequently Asked Questions", bg="#990000", fg="white",
                                font=("Arial", 24, "bold"), pady=20)
        header_label.pack()
if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
