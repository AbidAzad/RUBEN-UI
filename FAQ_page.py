import tkinter as tk
from tkinter import ttk
from tkintermapview import TkinterMapView
import csv
import os
from PIL import Image, ImageTk
from fuzzywuzzy import process

class FAQPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        header_frame = tk.Frame(self, bg="#990000", height=80)
        header_frame.pack(fill="x")

        back_button = tk.Button(header_frame, text="Back", command=lambda: master.switch_frame(StartPage), bg="#990000", fg="white", font=("Arial", 16, "bold"), padx=10)
        back_button.pack(side="left", padx=20)
        
        header_label = tk.Label(header_frame, text="Frequently Asked Questions", bg="#990000", fg="white", font=("Arial", 24, "bold"), pady=20)
        header_label.pack()

        image_path = "robot.jpg"
        image = Image.open(image_path)
        image = image.resize((300, 300))
        photo = ImageTk.PhotoImage(image)

        label_image = tk.Label(self, image=photo)
        label_image.image = photo  
        label_image.pack(pady=20)

        faq_text = """Frequently Asked Questions:

1. RUBEN, what does your name stand for?
   My name stands for Remote Utility Bot for Education and Navigation

2. What is your mission?
   Welcome! My mission is to help mitigate the complexity students may deal with when first entering the university. I will provide clear directions to specific locations.

3. Who created you? 
   Jeff Acevedo, Abid Azad, Carina Manek, Samuel Fabian, and Sampat Pachade for their senior design project"""

        label_faq = tk.Label(self, text=faq_text, padx=20, pady=20)
        label_faq.pack(pady=20)

if __name__ == "__main__":

    
    #app = SampleApp()
    #app.mainloop()
