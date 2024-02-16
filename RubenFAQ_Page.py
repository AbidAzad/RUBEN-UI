import tkinter as tk

def main():
    root = tk.Tk()
    root.title("FAQPage")

    # Set window size and position
    root.geometry("1024x600")

    # Create a canvas
    canvas = tk.Canvas(root, width=1024, height=600)
    canvas.pack()

    # Load the background image
    background_image = tk.PhotoImage(file="icons/FAQBackground.png")  # Replace "background.png" with your image file path
    canvas.create_image(0, 0, anchor=tk.NW, image=background_image)

    # Add a text box with a filled-in color
    text_box = tk.Text(root, width=97, height=12, bg="white", font=("Arial", 14))
    text_box.place(x=512, y=300, anchor = "center")  # Adjust the position as needed

    # Add text to the text box
    text_box.insert(tk.END, """
1. RUBEN, what does your name stand for?
   My name stands for Remote Utility Bot for Education and Navigation

2. What is your mission?
   Welcome! My mission is to help mitigate the complexity students may deal with when first entering the university. I will provide clear directions to specific locations.

3. Who created you? 
   Jeff Acevedo, Abid Azad, Carina Manek, Samuel Fabian, and Sampat Pachade for their senior design project""", "color"

                    )
    
    text_box.tag_config("color", foreground="black")


    root.mainloop()

if __name__ == "__main__":
    main()
