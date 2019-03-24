#def NewFile():
#    print("New File!")
#def OpenFile():
#    name = askopenfilename()
#    print(name)
#def About():
#    print("This is a simple example of a menu")
    

#menu = Menu(root)
#root.config(menu=menu)
#filemenu = Menu(menu)
#menu.add_cascade(label="File", menu=filemenu)
#filemenu.add_command(label="New", command=NewFile)
#filemenu.add_command(label="Open...", command=OpenFile)
#filemenu.add_separator()
#filemenu.add_command(label="Exit", command=root.quit)

#helpmenu = Menu(menu)
#menu.add_cascade(label="Help", menu=helpmenu)
#helpmenu.add_command(label="About...", command=About)



print(__name__)
import tkinter as tk

class Device_GUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        items = {"one": ["a","b","c"],
                 "two": ["d","e","f"],
                 "three": ["g","h","i"]}

        self.the_value = tk.StringVar()
        self.the_value.set("a")

        self.menubutton = tk.Menubutton(self, textvariable=self.the_value, indicatoron=True)
        self.topMenu = tk.Menu(self.menubutton, tearoff=False)
        self.menubutton.configure(menu=self.topMenu)

        for key in sorted(items.keys()):
            menu = tk.Menu(self.topMenu)
            self.topMenu.add_cascade(label=key, menu=menu)
            for value in items[key]:
                menu.add_radiobutton(label=value, variable = self.the_value, value=value)

        self.menubutton.pack()


if __name__ == "__main__":
    root = tk.Tk()

    # Title root
    root.title("Moses Group Devices")
    
    Device_GUI(root).pack(fill="both", expand=True)
    
    # Move root to top
    root.attributes("-topmost", True)
    root.mainloop()