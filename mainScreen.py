# Multi-frame tkinter application v2.3
import tkinter as tk

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
def button_click(button_number):
    print(f"Button {button_number} clicked!")
class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Additional code from the second snippet
        header_label = tk.Label(self, text="Hi, I'm RUBEN!", bg="#990000", fg="white", font=("Arial", 24, "bold"), pady=20)
        header_label.pack(side="top", fill="x")

        button_frame = tk.Frame(self, bg="white")
        button_frame.pack(side="top", pady=20)

        button1 = tk.Button(button_frame, text="Where to?", command=lambda: master.switch_frame(PageOne), bg="#990000", fg="white", font=("Arial", 18), bd=3)
        button2 = tk.Button(button_frame, text="Rutgers Database", command=lambda: button_click(2), bg="#990000", fg="white", font=("Arial", 18), bd=3)
        button3 = tk.Button(button_frame, text="FAQ", command=lambda: button_click(3), bg="#990000", fg="white", font=("Arial", 18), bd=3)

        button1.pack(side=tk.LEFT, padx=20)
        button2.pack(side=tk.LEFT, padx=20)
        button3.pack(side=tk.LEFT, padx=20)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.rowconfigure(1, weight=1)

class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is page one").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()

class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is page two").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()