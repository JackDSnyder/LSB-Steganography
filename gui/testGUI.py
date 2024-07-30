import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from utils.textEncodingDecoding import encodeText, decodeText

class TestWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.geometry("800x500")
        self.root.title("Test Window")
        
        self.setupUi()

    def setupUi(self):

        # # Button frame, similar to creating a grid in HTML/CSS
        # self.buttonFrame = tk.Frame(self.root)
        # self.buttonFrame.columnconfigure(0, weight=8)
        # self.buttonFrame.columnconfigure(1, weight=1)
        # self.buttonFrame.columnconfigure(2, weight=1)

        # self.b1 = tk.Button(self.buttonFrame, text="1", font=("Arial", 18))
        # self.b1.grid(row=0, column=0, sticky=tk.W+tk.E)
        # self.b2 = tk.Button(self.buttonFrame, text="2", font=("Arial", 18))
        # self.b2.grid(row=0, column=1, sticky=tk.W+tk.E)
        # self.b3 = tk.Button(self.buttonFrame, text="3", font=("Arial", 18))
        # self.b3.grid(row=0, column=2, sticky=tk.W+tk.E)
        # self.b4 = tk.Button(self.buttonFrame, text="4", font=("Arial", 18))
        # self.b4.grid(row=1, column=0, sticky=tk.W+tk.E)
        # self.b5 = tk.Button(self.buttonFrame, text="5", font=("Arial", 18))
        # self.b5.grid(row=1, column=1, sticky=tk.W+tk.E)
        # self.b6 = tk.Button(self.buttonFrame, text="6", font=("Arial", 18))
        # self.b6.grid(row=1, column=2, sticky=tk.W+tk.E)

        # self.buttonFrame.pack(fill='x')

        self.mb1 = tk.Menu(self.root)

        self.fileMenu = tk.Menu(self.mb1, tearoff=0)
        self.fileMenu.add_command(label="Close", command=self.onClose)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Close Without Question", command=exit)

        self.actionMenu = tk.Menu(self.mb1, tearoff=0)
        self.actionMenu.add_command(label="Show Message", command=self.showMessage)

        self.mb1.add_cascade(menu=self.fileMenu, label="File")
        self.mb1.add_cascade(menu=self.actionMenu, label="Action")

        self.root.config(menu=self.mb1)


        self.l1 = tk.Label(self.root, text="Your Message")
        self.l1.pack(padx=10, pady=10)

        self.t1 = tk.Text(self.root, height=5)
        self.t1.bind("<KeyPress>", self.shortcut)
        self.t1.pack(padx=10, pady=10)  

        self.c1State = tk.IntVar()

        self.c1 = tk.Checkbutton(self.root, text="Show Message Box", variable=self.c1State)
        self.c1.pack(padx=10,pady=10)

        self.b1 = tk.Button(self.root, text="Show Message", command=self.showMessage)
        self.b1.pack(padx=10, pady=10)

        self.clearB = tk.Button(self.root, text="Clear", command=self.clear)
        self.clearB.pack(padx=10,pady=10)

        self.selectB = tk.Button(self.root, text="Select File", command=self.selectFile)
        self.selectB.pack(padx=10, pady=10)


        self.root.protocol("WM_DELETE_WINDOW", self.onClose)



    def showMessage(self):
        if self.c1State.get():
            messagebox.showinfo(title="Message", message=self.t1.get('1.0', 'end'))
        else:
            print(self.t1.get('1.0', 'end-1c'))

    def shortcut(self, event):
        # If control + space is pressed
        if event.keysym == "space" and event.state == 4:
            self.showMessage()

    def onClose(self):
        if messagebox.askyesno(title="Quit?", message="Do you really want to quit?"):
            self.root.destroy()

    def clear(self):
        self.t1.delete('1.0', 'end')

    def selectFile(self):
        path = filedialog.askopenfilename()
        encodeText(path, "./encodedText.png", "The big bad man won't see this")
        print(path)

if __name__ == "__main__":
    root = tk.Tk()
    app = TestWindow(root)
    root.mainloop()