import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Main Window")

# Information to display on the faq page
faq_text = """Frequently Asked Questions:

1. RUBEN, what does your name stand for?
   My name stands for Remote Utility Bot for Education and Navigation

2. What is your mission?
   Welcome! My mission is to help mitigate the complexity students may deal with when first entering the university. I will provide clear directions to specific locations.

3. Who created you? 
   Jeff Acevedo, Abid Azad, Carina Manek, Samuel Fabian, and Sampat Pachade for their senior design project"""

# Add a label to the main window
label_faq = tk.Label(root, text = faq_text, padx = 20, pady = 20)
label_faq.pack(pady = 20)

# Start the Tkinter event loop
root.mainloop()
