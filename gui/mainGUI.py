import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, filedialog, ttk
from gui.tabs import textEncodingGui, textDecodingGui, imageEncodingGui, imageDecodingGui

class MainWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.geometry("800x500")
        self.root.title("LSB Steganography")
        
        self.setupUi()

    def setupUi(self):
        self.notebook = ttk.Notebook(self.root)

        # Create the various tabs for the notebook
        textEncodingGui.createTextEncodingTab(self.notebook)
        textDecodingGui.createTextDecodingTab(self.notebook)
        imageEncodingGui.createImageEncodingTab(self.notebook)
        imageDecodingGui.createImageDecodingTab(self.notebook)
        self.notebook.pack(fill='x')
