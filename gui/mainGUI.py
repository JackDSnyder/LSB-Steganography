import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, filedialog, ttk
from gui.tabs import textEncodingGui, textDecodingGui, imageEncodingGui, imageDecodingGui

class MainWindow:
    def __init__(self, root: ctk.CTk):
        self.root = root
        self.root.title("LSB Steganography")
        self.root.geometry("800x500")
        self.root._set_appearance_mode('dark')
        
        self.setupUi()

    def setupUi(self):

        self.tabview = ctk.CTkTabview(master=self.root)
        self.tabview.pack(fill = 'x')
        self.tabview.add("Encode Text")
        textEncodingGui.createTextEncodingTab(self.tabview)
        self.tabview.add("Decode Text")
        textDecodingGui.createTextDecodingTab(self.tabview)
        self.tabview.add("Encode Image")
        imageEncodingGui.createImageEncodingTab(self.tabview)
        self.tabview.add("Decode Image")
        imageDecodingGui.createImageDecodingTab(self.tabview)




